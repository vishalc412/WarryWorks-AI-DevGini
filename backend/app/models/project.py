"""
Project model - Stores user projects and their specifications
"""
from sqlalchemy import Column, String, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class ProjectStatus(str, enum.Enum):
    """Project status enumeration"""
    REQUIREMENT_INPUT = "requirement_input"
    INTERVIEW_IN_PROGRESS = "interview_in_progress"
    SPECIFICATION_READY = "specification_ready"
    GENERATION_IN_PROGRESS = "generation_in_progress"
    GENERATION_COMPLETE = "generation_complete"
    FAILED = "failed"


class Project(BaseModel):
    """Project model"""
    __tablename__ = "projects"

    # Basic information
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # User/owner information (simplified for now)
    user_id = Column(String(100), nullable=True)

    # Status tracking
    status = Column(
        SQLEnum(ProjectStatus),
        default=ProjectStatus.REQUIREMENT_INPUT,
        nullable=False
    )

    # Requirements and specifications
    raw_requirement = Column(Text, nullable=True)
    parsed_requirement = Column(JSON, nullable=True)
    final_specification = Column(JSON, nullable=True)

    # BRD, HLD, LLD documents
    brd_document = Column(JSON, nullable=True)
    hld_document = Column(JSON, nullable=True)
    lld_document = Column(JSON, nullable=True)

    # Technical specifications
    tech_stack = Column(JSON, nullable=True)
    api_specifications = Column(JSON, nullable=True)
    database_schema = Column(JSON, nullable=True)

    # AI Model configuration
    selected_models = Column(JSON, nullable=True)  # List of model providers

    # Relationships
    interview_state = relationship("InterviewState", back_populates="project", uselist=False)
    artifacts = relationship("Artifact", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', status='{self.status}')>"
