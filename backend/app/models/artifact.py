"""
Artifact model - Stores generated code and assets
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class ArtifactType(str, enum.Enum):
    """Artifact type enumeration"""
    BACKEND_CODE = "backend_code"
    FRONTEND_CODE = "frontend_code"
    DATABASE_SCHEMA = "database_schema"
    API_SPECIFICATION = "api_specification"
    DOCKERFILE = "dockerfile"
    KUBERNETES_MANIFEST = "kubernetes_manifest"
    TERRAFORM_CONFIG = "terraform_config"
    CI_CD_PIPELINE = "ci_cd_pipeline"
    DOCUMENTATION = "documentation"
    UI_WIREFRAME = "ui_wireframe"
    ARCHITECTURE_DIAGRAM = "architecture_diagram"
    COMPLETE_BUNDLE = "complete_bundle"


class Artifact(BaseModel):
    """Generated artifact model"""
    __tablename__ = "artifacts"

    # Foreign key to project
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Artifact information
    artifact_type = Column(SQLEnum(ArtifactType), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Storage information
    file_path = Column(String(500), nullable=True)  # S3 path or local path
    download_url = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)  # For small artifacts

    # Version tracking
    version = Column(String(50), default="1.0", nullable=False)

    # Model that generated this artifact
    generated_by_model = Column(String(100), nullable=True)

    # Relationship
    project = relationship("Project", back_populates="artifacts")

    def __repr__(self):
        return f"<Artifact(id={self.id}, type='{self.artifact_type}', name='{self.name}')>"
