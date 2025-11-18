"""
Interview Engine Service
Generates adaptive clarifying questions based on requirements
"""
import logging
from typing import Dict, List, Any, Optional
from app.models.interview_state import InterviewPhase
from app.services.model_router import model_router

logger = logging.getLogger(__name__)


class InterviewEngine:
    """AI-driven interview engine for requirement clarification"""

    def __init__(self):
        self.phase_questions = {
            InterviewPhase.APPLICATION_PURPOSE: [
                "What is the primary purpose of this application?",
                "Who are the target users/audience?",
                "What problem does this application solve?",
                "What are the key business objectives?"
            ],
            InterviewPhase.LOGICAL_WORKFLOWS: [
                "What are the main user workflows/journeys?",
                "How should users interact with the system?",
                "What are the key business processes?",
                "Are there any automation requirements?"
            ],
            InterviewPhase.DATA_AND_INTEGRATIONS: [
                "What data will the application manage?",
                "What are the main data entities?",
                "Are there any third-party integrations needed?",
                "What are the data input/output requirements?"
            ],
            InterviewPhase.NON_FUNCTIONAL: [
                "How many concurrent users do you expect?",
                "What are your performance requirements?",
                "What security requirements do you have?",
                "What are your availability/uptime expectations?",
                "Do you need high availability or disaster recovery?"
            ],
            InterviewPhase.TECH_STACK: [
                "Do you have any technology preferences?",
                "What is your preferred cloud platform (AWS/Azure/GCP)?",
                "Do you need mobile support?",
                "What deployment model do you prefer (cloud/on-premise)?"
            ]
        }

    async def generate_next_question(
        self,
        parsed_requirement: Dict[str, Any],
        current_phase: InterviewPhase,
        questions_asked: List[Dict],
        answers: List[Dict],
        context: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """
        Generate the next adaptive question based on context

        Args:
            parsed_requirement: Parsed requirement data
            current_phase: Current interview phase
            questions_asked: List of previously asked questions
            answers: List of answers given
            context: Accumulated context
            model_provider: AI model provider to use

        Returns:
            Next question object with metadata
        """
        logger.info(f"Generating question for phase: {current_phase}")

        # Build context for AI
        conversation_history = self._build_conversation_history(questions_asked, answers)

        # Determine if we should move to next phase
        if self._should_advance_phase(current_phase, questions_asked, answers):
            next_phase = self._get_next_phase(current_phase)
            if next_phase:
                current_phase = next_phase
                logger.info(f"Advancing to phase: {current_phase}")

        # Generate adaptive question using AI
        question = await self._generate_adaptive_question(
            parsed_requirement,
            current_phase,
            conversation_history,
            context,
            model_provider
        )

        return {
            "question": question,
            "phase": current_phase.value,
            "question_number": len(questions_asked) + 1,
            "metadata": {
                "question_type": self._classify_question_type(question),
                "importance": "high"
            }
        }

    async def _generate_adaptive_question(
        self,
        parsed_requirement: Dict[str, Any],
        phase: InterviewPhase,
        conversation_history: str,
        context: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate adaptive question using AI"""

        # Base questions for the phase
        base_questions = self.phase_questions.get(phase, [])

        # Build prompt for AI
        prompt = f"""You are an expert business analyst conducting a requirement clarification interview.

Domain: {parsed_requirement.get('domain', 'general')}
Complexity: {parsed_requirement.get('complexity_score', 50)}/100
Identified Features: {', '.join(parsed_requirement.get('features', [])[:5])}

Current Phase: {phase.value}

Previous Conversation:
{conversation_history}

Context:
{context}

Generate a single, specific, and relevant clarifying question for the {phase.value} phase.
The question should:
1. Be clear and specific
2. Help gather missing information
3. Build on previous answers
4. Not repeat already asked questions
5. Be relevant to the application domain

Question:"""

        try:
            question = await model_router.generate(
                prompt,
                provider=model_provider,
                temperature=0.7,
                max_tokens=200
            )
            return question.strip()
        except Exception as e:
            logger.warning(f"AI generation failed, using fallback: {str(e)}")
            # Fallback to predefined questions
            asked_questions = [q for q in base_questions if q not in conversation_history]
            if asked_questions:
                return asked_questions[0]
            return "What other important details should we consider?"

    def _build_conversation_history(
        self,
        questions: List[Dict],
        answers: List[Dict]
    ) -> str:
        """Build conversation history string"""
        history = []
        for i, (q, a) in enumerate(zip(questions, answers), 1):
            history.append(f"Q{i}: {q.get('question', '')}")
            history.append(f"A{i}: {a.get('answer', '')}")
        return "\n".join(history)

    def _should_advance_phase(
        self,
        current_phase: InterviewPhase,
        questions: List[Dict],
        answers: List[Dict]
    ) -> bool:
        """Determine if we should advance to the next phase"""
        # Count questions in current phase
        phase_questions = [q for q in questions if q.get('phase') == current_phase.value]

        # Advance after 3-5 questions per phase
        min_questions = 3
        max_questions = 5

        if len(phase_questions) < min_questions:
            return False

        # Check if answers are comprehensive enough
        if len(phase_questions) >= max_questions:
            return True

        # Check answer quality (simple heuristic)
        recent_answers = answers[-3:] if len(answers) >= 3 else answers
        avg_answer_length = sum(len(a.get('answer', '')) for a in recent_answers) / max(len(recent_answers), 1)

        # If answers are detailed, we can advance sooner
        if avg_answer_length > 100:
            return len(phase_questions) >= min_questions

        return False

    def _get_next_phase(self, current_phase: InterviewPhase) -> Optional[InterviewPhase]:
        """Get the next interview phase"""
        phases = [
            InterviewPhase.APPLICATION_PURPOSE,
            InterviewPhase.LOGICAL_WORKFLOWS,
            InterviewPhase.DATA_AND_INTEGRATIONS,
            InterviewPhase.NON_FUNCTIONAL,
            InterviewPhase.TECH_STACK,
            InterviewPhase.COMPLETED
        ]

        try:
            current_index = phases.index(current_phase)
            if current_index < len(phases) - 1:
                return phases[current_index + 1]
        except ValueError:
            pass

        return None

    def _classify_question_type(self, question: str) -> str:
        """Classify question type"""
        question_lower = question.lower()

        if any(word in question_lower for word in ["who", "user", "audience"]):
            return "user_focused"
        elif any(word in question_lower for word in ["what", "feature", "functionality"]):
            return "functional"
        elif any(word in question_lower for word in ["how", "process", "workflow"]):
            return "process"
        elif any(word in question_lower for word in ["data", "entity", "information"]):
            return "data"
        elif any(word in question_lower for word in ["performance", "scale", "security"]):
            return "non_functional"
        else:
            return "general"

    def calculate_coverage_score(
        self,
        questions: List[Dict],
        answers: List[Dict],
        parsed_requirement: Dict[str, Any]
    ) -> int:
        """
        Calculate requirement coverage score (0-100)

        Args:
            questions: List of asked questions
            answers: List of answers
            parsed_requirement: Parsed requirement data

        Returns:
            Coverage score (0-100)
        """
        score = 0

        # Base score from number of questions
        score += min(len(questions) * 3, 30)

        # Score from answer quality
        total_answer_length = sum(len(a.get('answer', '')) for a in answers)
        if total_answer_length > 1000:
            score += 20
        elif total_answer_length > 500:
            score += 15
        else:
            score += 10

        # Score from phase coverage
        phases_covered = set(q.get('phase') for q in questions)
        score += len(phases_covered) * 8

        # Score from complexity alignment
        complexity = parsed_requirement.get('complexity_score', 50)
        expected_questions = max(10, int(complexity / 5))
        if len(questions) >= expected_questions:
            score += 20

        return min(score, 100)

    def is_interview_complete(
        self,
        questions: List[Dict],
        answers: List[Dict],
        coverage_score: int
    ) -> bool:
        """Determine if interview is complete"""
        # Minimum 10 questions
        if len(questions) < 10:
            return False

        # Coverage score threshold
        if coverage_score < 70:
            return False

        # All phases covered
        phases_covered = set(q.get('phase') for q in questions)
        required_phases = {
            InterviewPhase.APPLICATION_PURPOSE.value,
            InterviewPhase.LOGICAL_WORKFLOWS.value,
            InterviewPhase.DATA_AND_INTEGRATIONS.value
        }

        return required_phases.issubset(phases_covered)
