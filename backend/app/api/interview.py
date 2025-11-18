"""
Interview API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from app.db.session import get_db
from app.models.project import Project, ProjectStatus
from app.models.interview_state import InterviewState, InterviewPhase
from app.services.interview_engine import InterviewEngine

logger = logging.getLogger(__name__)
router = APIRouter()


class AnswerInput(BaseModel):
    """Request model for submitting an answer"""
    session_id: str
    answer: str
    model_provider: str = "openai"


class QuestionResponse(BaseModel):
    """Response model for question"""
    question: str
    phase: str
    question_number: int
    coverage_score: int
    is_complete: bool
    metadata: Dict[str, Any]


@router.post("/next", response_model=QuestionResponse)
async def get_next_question(
    answer_input: AnswerInput,
    db: Session = Depends(get_db)
):
    """
    Get the next interview question

    Args:
        answer_input: Answer to previous question
        db: Database session

    Returns:
        Next question
    """
    logger.info(f"Getting next question for session: {answer_input.session_id}")

    try:
        # Get interview state
        interview_state = db.query(InterviewState).filter(
            InterviewState.session_id == answer_input.session_id
        ).first()

        if not interview_state:
            raise HTTPException(status_code=404, detail="Interview session not found")

        # Get project
        project = db.query(Project).filter(
            Project.id == interview_state.project_id
        ).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Save the answer if provided
        if answer_input.answer:
            # Get the last question
            questions = interview_state.questions_asked or []
            if questions:
                last_question = questions[-1]

                # Add answer
                answers = interview_state.answers_given or []
                answers.append({
                    "answer": answer_input.answer,
                    "question_number": len(questions)
                })
                interview_state.answers_given = answers

        # Generate next question
        interview_engine = InterviewEngine()

        next_question_data = await interview_engine.generate_next_question(
            parsed_requirement=project.parsed_requirement,
            current_phase=interview_state.current_phase,
            questions_asked=interview_state.questions_asked or [],
            answers=interview_state.answers_given or [],
            context=interview_state.context or {},
            model_provider=answer_input.model_provider
        )

        # Save question
        questions = interview_state.questions_asked or []
        questions.append(next_question_data)
        interview_state.questions_asked = questions

        # Update phase if changed
        if next_question_data['phase'] != interview_state.current_phase.value:
            interview_state.current_phase = InterviewPhase(next_question_data['phase'])

        # Calculate coverage score
        coverage_score = interview_engine.calculate_coverage_score(
            questions=interview_state.questions_asked,
            answers=interview_state.answers_given or [],
            parsed_requirement=project.parsed_requirement
        )
        interview_state.coverage_score = coverage_score

        # Check if interview is complete
        is_complete = interview_engine.is_interview_complete(
            questions=interview_state.questions_asked,
            answers=interview_state.answers_given or [],
            coverage_score=coverage_score
        )
        interview_state.is_complete = is_complete

        if is_complete:
            project.status = ProjectStatus.SPECIFICATION_READY
            interview_state.current_phase = InterviewPhase.COMPLETED

        db.commit()

        logger.info(f"Generated question {len(questions)} for session {answer_input.session_id}")

        return QuestionResponse(
            question=next_question_data['question'],
            phase=next_question_data['phase'],
            question_number=next_question_data['question_number'],
            coverage_score=coverage_score,
            is_complete=is_complete,
            metadata=next_question_data['metadata']
        )

    except Exception as e:
        logger.error(f"Error generating next question: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{session_id}")
async def get_interview_status(session_id: str, db: Session = Depends(get_db)):
    """Get interview status"""
    interview_state = db.query(InterviewState).filter(
        InterviewState.session_id == session_id
    ).first()

    if not interview_state:
        raise HTTPException(status_code=404, detail="Interview session not found")

    return {
        "session_id": session_id,
        "current_phase": interview_state.current_phase,
        "questions_count": len(interview_state.questions_asked or []),
        "coverage_score": interview_state.coverage_score,
        "is_complete": interview_state.is_complete,
        "questions": interview_state.questions_asked,
        "answers": interview_state.answers_given
    }


@router.get("/history/{session_id}")
async def get_interview_history(session_id: str, db: Session = Depends(get_db)):
    """Get full interview history"""
    interview_state = db.query(InterviewState).filter(
        InterviewState.session_id == session_id
    ).first()

    if not interview_state:
        raise HTTPException(status_code=404, detail="Interview session not found")

    questions = interview_state.questions_asked or []
    answers = interview_state.answers_given or []

    history = []
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        history.append({
            "number": i,
            "question": q.get('question', ''),
            "answer": a.get('answer', ''),
            "phase": q.get('phase', '')
        })

    return {
        "session_id": session_id,
        "history": history,
        "coverage_score": interview_state.coverage_score,
        "is_complete": interview_state.is_complete
    }
