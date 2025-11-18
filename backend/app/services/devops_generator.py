"""
DevOps Generator Service
Generates DevOps artifacts: Docker, Kubernetes, Terraform, CI/CD pipelines
"""
import logging
from typing import Dict, Any
from app.services.model_router import model_router

logger = logging.getLogger(__name__)


class DevOpsGenerator:
    """Generates DevOps and infrastructure code"""

    def __init__(self):
        self.logger = logger

    async def generate_all_devops(
        self,
        specification: Dict[str, Any],
        tech_stack: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """
        Generate all DevOps artifacts

        Args:
            specification: Application specification
            tech_stack: Technology stack configuration
            model_provider: AI model provider

        Returns:
            Dictionary containing all DevOps artifacts
        """
        logger.info("Generating DevOps artifacts...")

        devops_artifacts = {
            "docker": await self.generate_docker(tech_stack, model_provider),
            "kubernetes": await self.generate_kubernetes(tech_stack, model_provider),
            "terraform": await self.generate_terraform(tech_stack, model_provider),
            "ci_cd": await self.generate_ci_cd(tech_stack, model_provider),
            "helm": await self.generate_helm_charts(tech_stack, model_provider)
        }

        return devops_artifacts

    async def generate_docker(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate Docker configurations"""
        logger.info("Generating Docker configurations...")

        docker_files = {}

        # Generate backend Dockerfile
        docker_files['backend.Dockerfile'] = await self._generate_backend_dockerfile(
            tech_stack, model_provider
        )

        # Generate frontend Dockerfile
        docker_files['frontend.Dockerfile'] = await self._generate_frontend_dockerfile(
            tech_stack, model_provider
        )

        # Generate docker-compose.yml
        docker_files['docker-compose.yml'] = await self._generate_docker_compose(
            tech_stack, model_provider
        )

        # Generate .dockerignore
        docker_files['.dockerignore'] = self._generate_dockerignore()

        return docker_files

    async def _generate_backend_dockerfile(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate backend Dockerfile"""
        logger.info("Generating backend Dockerfile...")

        prompt = """Generate a production-ready Dockerfile for a Python FastAPI application:

Requirements:
- Use Python 3.12 slim image
- Multi-stage build
- Install dependencies efficiently
- Run as non-root user
- Use uvicorn for production
- Health check
- Optimize layers for caching

Generate complete Dockerfile."""

        try:
            dockerfile = await model_router.generate(prompt, provider=model_provider, max_tokens=800)
            # Extract code if in markdown
            import re
            code_match = re.search(r'```dockerfile\n(.*?)\n```', dockerfile, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return dockerfile
        except Exception as e:
            logger.error(f"Error generating backend Dockerfile: {str(e)}")
            return self._get_fallback_backend_dockerfile()

    async def _generate_frontend_dockerfile(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate frontend Dockerfile"""
        logger.info("Generating frontend Dockerfile...")

        prompt = """Generate a production-ready Dockerfile for a React application:

Requirements:
- Use Node 20 alpine
- Multi-stage build
- Build React app
- Serve with nginx
- Optimize bundle size
- Include nginx config

Generate complete Dockerfile."""

        try:
            dockerfile = await model_router.generate(prompt, provider=model_provider, max_tokens=800)
            import re
            code_match = re.search(r'```dockerfile\n(.*?)\n```', dockerfile, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return dockerfile
        except Exception as e:
            logger.error(f"Error generating frontend Dockerfile: {str(e)}")
            return self._get_fallback_frontend_dockerfile()

    async def _generate_docker_compose(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate docker-compose.yml"""
        logger.info("Generating docker-compose.yml...")

        prompt = """Generate a docker-compose.yml for:
- FastAPI backend
- React frontend
- PostgreSQL database
- Redis cache

Include:
- Networks
- Volumes for persistence
- Environment variables
- Health checks
- Depends on relationships

Generate complete docker-compose YAML."""

        try:
            compose = await model_router.generate(prompt, provider=model_provider, max_tokens=1000)
            import re
            code_match = re.search(r'```yaml\n(.*?)\n```', compose, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return compose
        except Exception as e:
            logger.error(f"Error generating docker-compose: {str(e)}")
            return self._get_fallback_docker_compose()

    async def generate_kubernetes(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate Kubernetes manifests"""
        logger.info("Generating Kubernetes manifests...")

        k8s_files = {}

        # Generate deployment
        k8s_files['deployment.yaml'] = await self._generate_k8s_deployment(
            tech_stack, model_provider
        )

        # Generate service
        k8s_files['service.yaml'] = await self._generate_k8s_service(
            tech_stack, model_provider
        )

        # Generate ingress
        k8s_files['ingress.yaml'] = await self._generate_k8s_ingress(
            tech_stack, model_provider
        )

        # Generate configmap
        k8s_files['configmap.yaml'] = self._generate_k8s_configmap()

        # Generate secrets template
        k8s_files['secrets.yaml.template'] = self._generate_k8s_secrets_template()

        return k8s_files

    async def _generate_k8s_deployment(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate Kubernetes Deployment"""
        prompt = """Generate Kubernetes Deployment manifest for:
- Backend API (3 replicas)
- Frontend app (2 replicas)
- Resource limits and requests
- Liveness and readiness probes
- Rolling update strategy

Generate complete YAML."""

        try:
            deployment = await model_router.generate(prompt, provider=model_provider, max_tokens=1200)
            import re
            code_match = re.search(r'```yaml\n(.*?)\n```', deployment, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return deployment
        except Exception as e:
            return self._get_fallback_k8s_deployment()

    async def _generate_k8s_service(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate Kubernetes Service"""
        prompt = """Generate Kubernetes Service manifest:
- ClusterIP service for backend
- LoadBalancer or ClusterIP for frontend
- Proper port mappings
- Selectors

Generate complete YAML."""

        try:
            service = await model_router.generate(prompt, provider=model_provider, max_tokens=800)
            import re
            code_match = re.search(r'```yaml\n(.*?)\n```', service, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return service
        except Exception as e:
            return self._get_fallback_k8s_service()

    async def _generate_k8s_ingress(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate Kubernetes Ingress"""
        prompt = """Generate Kubernetes Ingress manifest:
- NGINX ingress controller
- TLS configuration
- Path-based routing
- Backend and frontend routes

Generate complete YAML."""

        try:
            ingress = await model_router.generate(prompt, provider=model_provider, max_tokens=800)
            import re
            code_match = re.search(r'```yaml\n(.*?)\n```', ingress, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return ingress
        except Exception as e:
            return self._get_fallback_k8s_ingress()

    async def generate_terraform(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate Terraform configurations"""
        logger.info("Generating Terraform configurations...")

        tf_files = {}

        cloud_provider = tech_stack.get('infrastructure', {}).get('cloud', 'aws').lower()

        if cloud_provider == 'aws':
            tf_files['main.tf'] = await self._generate_terraform_aws(model_provider)
        elif cloud_provider == 'azure':
            tf_files['main.tf'] = await self._generate_terraform_azure(model_provider)
        elif cloud_provider == 'gcp':
            tf_files['main.tf'] = await self._generate_terraform_gcp(model_provider)

        tf_files['variables.tf'] = self._generate_terraform_variables()
        tf_files['outputs.tf'] = self._generate_terraform_outputs()

        return tf_files

    async def _generate_terraform_aws(self, model_provider: str) -> str:
        """Generate Terraform for AWS"""
        prompt = """Generate Terraform configuration for AWS:
- VPC with public/private subnets
- EKS cluster
- RDS PostgreSQL
- ElastiCache Redis
- S3 bucket
- Security groups
- IAM roles

Generate complete Terraform HCL."""

        try:
            tf = await model_router.generate(prompt, provider=model_provider, max_tokens=2000)
            import re
            code_match = re.search(r'```hcl\n(.*?)\n```', tf, re.DOTALL)
            if not code_match:
                code_match = re.search(r'```terraform\n(.*?)\n```', tf, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return tf
        except Exception as e:
            return self._get_fallback_terraform()

    async def _generate_terraform_azure(self, model_provider: str) -> str:
        """Generate Terraform for Azure"""
        return "# Azure Terraform configuration to be implemented"

    async def _generate_terraform_gcp(self, model_provider: str) -> str:
        """Generate Terraform for GCP"""
        return "# GCP Terraform configuration to be implemented"

    async def generate_ci_cd(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate CI/CD pipelines"""
        logger.info("Generating CI/CD pipelines...")

        ci_cd_files = {}

        # GitHub Actions
        ci_cd_files['.github/workflows/ci.yml'] = await self._generate_github_actions(
            tech_stack, model_provider
        )

        # GitLab CI (optional)
        ci_cd_files['.gitlab-ci.yml'] = self._generate_gitlab_ci()

        return ci_cd_files

    async def _generate_github_actions(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate GitHub Actions workflow"""
        logger.info("Generating GitHub Actions workflow...")

        prompt = """Generate GitHub Actions workflow for:
- Build and test backend (Python)
- Build and test frontend (React)
- Build Docker images
- Push to container registry
- Deploy to Kubernetes
- Run linting and formatting

Generate complete YAML workflow."""

        try:
            workflow = await model_router.generate(prompt, provider=model_provider, max_tokens=1500)
            import re
            code_match = re.search(r'```yaml\n(.*?)\n```', workflow, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return workflow
        except Exception as e:
            return self._get_fallback_github_actions()

    async def generate_helm_charts(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate Helm charts"""
        logger.info("Generating Helm charts...")

        helm_files = {}

        helm_files['Chart.yaml'] = self._generate_helm_chart_yaml()
        helm_files['values.yaml'] = await self._generate_helm_values(tech_stack, model_provider)
        helm_files['templates/deployment.yaml'] = "{{/* Helm deployment template */}}"

        return helm_files

    async def _generate_helm_values(
        self,
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate Helm values.yaml"""
        return """# Helm values
replicaCount: 3
image:
  repository: myapp
  tag: latest
  pullPolicy: IfNotPresent
service:
  type: LoadBalancer
  port: 80
"""

    # Fallback methods
    def _get_fallback_backend_dockerfile(self) -> str:
        return '''FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    def _get_fallback_frontend_dockerfile(self) -> str:
        return '''FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''

    def _get_fallback_docker_compose(self) -> str:
        return '''version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
'''

    def _get_fallback_k8s_deployment(self) -> str:
        return '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: backend
        image: myapp-backend:latest
        ports:
        - containerPort: 8000
'''

    def _get_fallback_k8s_service(self) -> str:
        return '''apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
'''

    def _get_fallback_k8s_ingress(self) -> str:
        return '''apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
'''

    def _get_fallback_terraform(self) -> str:
        return '''terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
'''

    def _get_fallback_github_actions(self) -> str:
        return '''name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build
      run: echo "Build step"
    - name: Test
      run: echo "Test step"
'''

    def _generate_dockerignore(self) -> str:
        return '''__pycache__
*.pyc
.env
.git
.gitignore
*.md
.venv
venv/
node_modules/
.pytest_cache
.coverage
'''

    def _generate_k8s_configmap(self) -> str:
        return '''apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
'''

    def _generate_k8s_secrets_template(self) -> str:
        return '''apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DATABASE_URL: <base64-encoded>
  SECRET_KEY: <base64-encoded>
'''

    def _generate_terraform_variables(self) -> str:
        return '''variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}
'''

    def _generate_terraform_outputs(self) -> str:
        return '''output "vpc_id" {
  value = aws_vpc.main.id
}
'''

    def _generate_gitlab_ci(self) -> str:
        return '''stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - echo "Building..."

test:
  stage: test
  script:
    - echo "Testing..."

deploy:
  stage: deploy
  script:
    - echo "Deploying..."
'''

    def _generate_helm_chart_yaml(self) -> str:
        return '''apiVersion: v2
name: myapp
description: Generated Helm chart
version: 1.0.0
appVersion: "1.0"
'''
