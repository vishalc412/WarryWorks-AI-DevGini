"""
Requirements API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import logging
import uuid

from app.db.session import get_db
from app.models.project import Project, ProjectStatus
from app.models.interview_state import InterviewState, InterviewPhase
from app.services.requirement_parser import RequirementParser

logger = logging.getLogger(__name__)
router = APIRouter()


class RequirementInput(BaseModel):
    """Request model for requirement input"""
    title: str
    description: str
    user_id: str = None


class RequirementResponse(BaseModel):
    """Response model for requirement"""
    project_id: int
    session_id: str
    parsed_requirement: Dict[str, Any]
    message: str


@router.post("/ingest", response_model=RequirementResponse)
async def ingest_requirement(
    requirement: RequirementInput,
    db: Session = Depends(get_db)
):
    """
    Ingest a new requirement and create a project

    Args:
        requirement: Requirement input data
        db: Database session

    Returns:
        Parsed requirement and project information
    """
    logger.info(f"Ingesting requirement: {requirement.title}")

    try:
        # Parse the requirement
        parser = RequirementParser()
        parsed_data = parser.parse(requirement.description)

        # Create new project
        project = Project(
            title=requirement.title,
            description=requirement.description,
            user_id=requirement.user_id,
            status=ProjectStatus.REQUIREMENT_INPUT,
            raw_requirement=requirement.description,
            parsed_requirement=parsed_data
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        # Create interview state
        session_id = f"session-{uuid.uuid4().hex[:12]}"
        interview_state = InterviewState(
            project_id=project.id,
            session_id=session_id,
            current_phase=InterviewPhase.APPLICATION_PURPOSE,
            questions_asked=[],
            answers_given=[],
            context=parsed_data
        )

        db.add(interview_state)
        db.commit()

        # Update project status
        project.status = ProjectStatus.INTERVIEW_IN_PROGRESS
        db.commit()

        logger.info(f"Created project {project.id} with session {session_id}")

        return RequirementResponse(
            project_id=project.id,
            session_id=session_id,
            parsed_requirement=parsed_data,
            message="Requirement parsed successfully. Interview session created."
        )

    except Exception as e:
        logger.error(f"Error ingesting requirement: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project/{project_id}")
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project details"""
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "parsed_requirement": project.parsed_requirement,
        "created_at": project.created_at
    }


@router.get("/projects")
async def list_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all projects"""
    projects = db.query(Project).offset(skip).limit(limit).all()

    return {
        "projects": [
            {
                "id": p.id,
                "title": p.title,
                "status": p.status,
                "created_at": p.created_at
            }
            for p in projects
        ]
    }
