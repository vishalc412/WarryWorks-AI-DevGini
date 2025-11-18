"""
Interview State model - Tracks the AI-driven interview process
"""
from sqlalchemy import Column, String, Integer, JSON, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class InterviewPhase(str, enum.Enum):
    """Interview phase enumeration"""
    APPLICATION_PURPOSE = "application_purpose"
    LOGICAL_WORKFLOWS = "logical_workflows"
    DATA_AND_INTEGRATIONS = "data_and_integrations"
    NON_FUNCTIONAL = "non_functional"
    TECH_STACK = "tech_stack"
    COMPLETED = "completed"


class InterviewState(BaseModel):
    """Interview state tracking model"""
    __tablename__ = "interview_states"

    # Foreign key to project
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, unique=True)

    # Session information
    session_id = Column(String(100), nullable=False, unique=True, index=True)

    # Current phase and question
    current_phase = Column(
        SQLEnum(InterviewPhase),
        default=InterviewPhase.APPLICATION_PURPOSE,
        nullable=False
    )
    current_question_index = Column(Integer, default=0, nullable=False)

    # Questions and answers
    questions_asked = Column(JSON, default=list, nullable=False)  # List of question objects
    answers_given = Column(JSON, default=list, nullable=False)   # List of answer objects

    # Coverage and completion
    coverage_score = Column(Integer, default=0)  # 0-100
    is_complete = Column(Boolean, default=False)

    # Context for adaptive questioning
    context = Column(JSON, default=dict, nullable=False)  # Accumulated context

    # Next question cache
    next_question = Column(JSON, nullable=True)

    # Relationship
    project = relationship("Project", back_populates="interview_state")

    def __repr__(self):
        return f"<InterviewState(session_id='{self.session_id}', phase='{self.current_phase}', complete={self.is_complete})>"
