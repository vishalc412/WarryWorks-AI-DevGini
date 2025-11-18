"""
Code Generation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import json

from app.db.session import get_db
from app.models.project import Project, ProjectStatus
from app.models.interview_state import InterviewState
from app.models.artifact import Artifact, ArtifactType
from app.services.spec_generator import SpecificationGenerator
from app.services.code_generator import CodeGenerator
from app.services.devops_generator import DevOpsGenerator

logger = logging.getLogger(__name__)
router = APIRouter()


class GenerateRequest(BaseModel):
    """Request model for generation"""
    project_id: int
    model_provider: str = "openai"
    generate_spec: bool = True
    generate_code: bool = True
    generate_devops: bool = True


class GenerateResponse(BaseModel):
    """Response model for generation"""
    project_id: int
    status: str
    message: str
    artifacts: List[Dict[str, Any]]


@router.post("/spec", response_model=GenerateResponse)
async def generate_specification(
    request: GenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate specification (BRD, HLD, LLD)

    Args:
        request: Generation request
        db: Database session

    Returns:
        Generation response with artifacts
    """
    logger.info(f"Generating specification for project {request.project_id}")

    try:
        # Get project and interview state
        project = db.query(Project).filter(Project.id == request.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        interview_state = db.query(InterviewState).filter(
            InterviewState.project_id == request.project_id
        ).first()

        if not interview_state or not interview_state.is_complete:
            raise HTTPException(
                status_code=400,
                detail="Interview must be completed before generating specification"
            )

        # Prepare interview data
        interview_data = {
            "questions": interview_state.questions_asked,
            "answers": interview_state.answers_given,
            "context": interview_state.context
        }

        # Generate specification
        spec_generator = SpecificationGenerator()
        specification = await spec_generator.generate_complete_specification(
            parsed_requirement=project.parsed_requirement,
            interview_data=interview_data,
            model_provider=request.model_provider
        )

        # Save specification to project
        project.final_specification = specification
        project.brd_document = specification.get('brd')
        project.hld_document = specification.get('hld')
        project.lld_document = specification.get('lld')
        project.api_specifications = specification.get('api_specification')
        project.database_schema = specification.get('database_schema')
        project.tech_stack = specification.get('tech_stack')
        project.status = ProjectStatus.SPECIFICATION_READY

        # Create artifacts
        artifacts = []

        # BRD artifact
        brd_artifact = Artifact(
            project_id=project.id,
            artifact_type=ArtifactType.DOCUMENTATION,
            name="Business Requirements Document",
            content=json.dumps(specification.get('brd'), indent=2),
            generated_by_model=request.model_provider
        )
        db.add(brd_artifact)
        artifacts.append({
            "type": "brd",
            "name": "Business Requirements Document"
        })

        # HLD artifact
        hld_artifact = Artifact(
            project_id=project.id,
            artifact_type=ArtifactType.ARCHITECTURE_DIAGRAM,
            name="High-Level Design",
            content=json.dumps(specification.get('hld'), indent=2),
            generated_by_model=request.model_provider
        )
        db.add(hld_artifact)
        artifacts.append({
            "type": "hld",
            "name": "High-Level Design"
        })

        # LLD artifact
        lld_artifact = Artifact(
            project_id=project.id,
            artifact_type=ArtifactType.DOCUMENTATION,
            name="Low-Level Design",
            content=json.dumps(specification.get('lld'), indent=2),
            generated_by_model=request.model_provider
        )
        db.add(lld_artifact)
        artifacts.append({
            "type": "lld",
            "name": "Low-Level Design"
        })

        db.commit()

        logger.info(f"Generated specification for project {request.project_id}")

        return GenerateResponse(
            project_id=project.id,
            status="success",
            message="Specification generated successfully",
            artifacts=artifacts
        )

    except Exception as e:
        logger.error(f"Error generating specification: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/code", response_model=GenerateResponse)
async def generate_code(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate complete application code

    Args:
        request: Generation request
        background_tasks: Background tasks
        db: Database session

    Returns:
        Generation response
    """
    logger.info(f"Generating code for project {request.project_id}")

    try:
        # Get project
        project = db.query(Project).filter(Project.id == request.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if not project.final_specification:
            raise HTTPException(
                status_code=400,
                detail="Specification must be generated before generating code"
            )

        # Update project status
        project.status = ProjectStatus.GENERATION_IN_PROGRESS
        db.commit()

        # Generate code
        code_generator = CodeGenerator()
        generated_code = await code_generator.generate_complete_application(
            specification=project.final_specification,
            model_provider=request.model_provider
        )

        # Save code artifacts
        artifacts = []

        # Backend code
        for filename, code in generated_code.get('backend', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.BACKEND_CODE,
                name=f"backend/{filename}",
                content=code,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "backend_code",
                "name": f"backend/{filename}"
            })

        # Frontend code
        for filename, code in generated_code.get('frontend', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.FRONTEND_CODE,
                name=f"frontend/{filename}",
                content=code,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "frontend_code",
                "name": f"frontend/{filename}"
            })

        # Database migrations
        for filename, code in generated_code.get('database', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.DATABASE_SCHEMA,
                name=f"database/{filename}",
                content=code,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "database_schema",
                "name": f"database/{filename}"
            })

        # Update project status
        project.status = ProjectStatus.GENERATION_COMPLETE
        db.commit()

        logger.info(f"Generated {len(artifacts)} code artifacts for project {request.project_id}")

        return GenerateResponse(
            project_id=project.id,
            status="success",
            message=f"Generated {len(artifacts)} code files",
            artifacts=artifacts
        )

    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        db.rollback()
        project.status = ProjectStatus.FAILED
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/devops", response_model=GenerateResponse)
async def generate_devops(
    request: GenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate DevOps artifacts"""
    logger.info(f"Generating DevOps artifacts for project {request.project_id}")

    try:
        # Get project
        project = db.query(Project).filter(Project.id == request.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if not project.final_specification:
            raise HTTPException(
                status_code=400,
                detail="Specification must be generated before generating DevOps artifacts"
            )

        # Generate DevOps artifacts
        devops_generator = DevOpsGenerator()
        devops_artifacts = await devops_generator.generate_all_devops(
            specification=project.final_specification,
            tech_stack=project.tech_stack or {},
            model_provider=request.model_provider
        )

        # Save artifacts
        artifacts = []

        # Docker files
        for filename, content in devops_artifacts.get('docker', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.DOCKERFILE,
                name=f"docker/{filename}",
                content=content,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "docker",
                "name": f"docker/{filename}"
            })

        # Kubernetes manifests
        for filename, content in devops_artifacts.get('kubernetes', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.KUBERNETES_MANIFEST,
                name=f"k8s/{filename}",
                content=content,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "kubernetes",
                "name": f"k8s/{filename}"
            })

        # Terraform files
        for filename, content in devops_artifacts.get('terraform', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.TERRAFORM_CONFIG,
                name=f"terraform/{filename}",
                content=content,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "terraform",
                "name": f"terraform/{filename}"
            })

        # CI/CD pipelines
        for filename, content in devops_artifacts.get('ci_cd', {}).items():
            artifact = Artifact(
                project_id=project.id,
                artifact_type=ArtifactType.CI_CD_PIPELINE,
                name=f"ci-cd/{filename}",
                content=content,
                generated_by_model=request.model_provider
            )
            db.add(artifact)
            artifacts.append({
                "type": "ci_cd",
                "name": f"ci-cd/{filename}"
            })

        db.commit()

        logger.info(f"Generated {len(artifacts)} DevOps artifacts for project {request.project_id}")

        return GenerateResponse(
            project_id=project.id,
            status="success",
            message=f"Generated {len(artifacts)} DevOps artifacts",
            artifacts=artifacts
        )

    except Exception as e:
        logger.error(f"Error generating DevOps artifacts: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artifacts/{project_id}")
async def get_artifacts(project_id: int, db: Session = Depends(get_db)):
    """Get all artifacts for a project"""
    artifacts = db.query(Artifact).filter(Artifact.project_id == project_id).all()

    return {
        "project_id": project_id,
        "artifacts": [
            {
                "id": a.id,
                "type": a.artifact_type,
                "name": a.name,
                "created_at": a.created_at,
                "download_url": a.download_url
            }
            for a in artifacts
        ]
    }


@router.get("/artifact/{artifact_id}")
async def get_artifact(artifact_id: int, db: Session = Depends(get_db)):
    """Get specific artifact content"""
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()

    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    return {
        "id": artifact.id,
        "type": artifact.artifact_type,
        "name": artifact.name,
        "content": artifact.content,
        "created_at": artifact.created_at
    }
