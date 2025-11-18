"""
Specification Generator Service
Generates BRD, HLD, LLD, and technical specifications from requirements
"""
import logging
from typing import Dict, List, Any
from app.services.model_router import model_router

logger = logging.getLogger(__name__)


class SpecificationGenerator:
    """Generates comprehensive technical specifications"""

    def __init__(self):
        self.logger = logger

    async def generate_complete_specification(
        self,
        parsed_requirement: Dict[str, Any],
        interview_data: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """
        Generate complete specification including BRD, HLD, LLD

        Args:
            parsed_requirement: Parsed requirement data
            interview_data: Interview questions and answers
            model_provider: AI model provider

        Returns:
            Complete specification dictionary
        """
        logger.info("Generating complete specification...")

        # Generate all specification documents
        brd = await self.generate_brd(parsed_requirement, interview_data, model_provider)
        hld = await self.generate_hld(parsed_requirement, interview_data, brd, model_provider)
        lld = await self.generate_lld(parsed_requirement, interview_data, hld, model_provider)
        api_spec = await self.generate_api_specification(lld, model_provider)
        db_schema = await self.generate_database_schema(lld, model_provider)

        return {
            "brd": brd,
            "hld": hld,
            "lld": lld,
            "api_specification": api_spec,
            "database_schema": db_schema,
            "tech_stack": self._determine_tech_stack(parsed_requirement, interview_data)
        }

    async def generate_brd(
        self,
        parsed_requirement: Dict[str, Any],
        interview_data: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """Generate Business Requirements Document"""
        logger.info("Generating BRD...")

        qa_pairs = self._format_qa_pairs(interview_data)

        prompt = f"""Generate a comprehensive Business Requirements Document (BRD) based on the following information:

Domain: {parsed_requirement.get('domain', 'general')}
Features: {', '.join(parsed_requirement.get('features', []))}
Entities: {', '.join(parsed_requirement.get('entities', []))}

Interview Q&A:
{qa_pairs}

Create a structured BRD with the following sections:
1. Executive Summary
2. Business Objectives
3. Stakeholders
4. Scope (In-scope and Out-of-scope)
5. Functional Requirements
6. Non-Functional Requirements
7. Assumptions and Constraints
8. Success Criteria

Format the response as JSON with these sections as keys."""

        try:
            response = await model_router.generate(prompt, provider=model_provider, max_tokens=3000)
            # Parse JSON response
            import json
            import re
            # Try to extract JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                brd = json.loads(json_match.group(0))
            else:
                # Fallback structure
                brd = self._create_fallback_brd(parsed_requirement, interview_data)

            return brd
        except Exception as e:
            logger.error(f"Error generating BRD: {str(e)}")
            return self._create_fallback_brd(parsed_requirement, interview_data)

    async def generate_hld(
        self,
        parsed_requirement: Dict[str, Any],
        interview_data: Dict[str, Any],
        brd: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """Generate High-Level Design document"""
        logger.info("Generating HLD...")

        prompt = f"""Generate a High-Level Design (HLD) document based on this BRD:

Business Objectives: {brd.get('business_objectives', '')}
Functional Requirements: {brd.get('functional_requirements', '')}
Domain: {parsed_requirement.get('domain', 'general')}

Create a structured HLD with:
1. System Architecture Overview
2. Component Diagram (describe components)
3. Data Flow
4. Technology Stack Recommendation
5. Integration Points
6. Security Architecture
7. Deployment Architecture
8. Scalability Considerations

Format as JSON with these sections."""

        try:
            response = await model_router.generate(prompt, provider=model_provider, max_tokens=3000)
            import json
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                hld = json.loads(json_match.group(0))
            else:
                hld = self._create_fallback_hld(parsed_requirement)

            return hld
        except Exception as e:
            logger.error(f"Error generating HLD: {str(e)}")
            return self._create_fallback_hld(parsed_requirement)

    async def generate_lld(
        self,
        parsed_requirement: Dict[str, Any],
        interview_data: Dict[str, Any],
        hld: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """Generate Low-Level Design document"""
        logger.info("Generating LLD...")

        prompt = f"""Generate a Low-Level Design (LLD) document based on this HLD:

Architecture: {hld.get('system_architecture_overview', '')}
Components: {hld.get('component_diagram', '')}
Tech Stack: {hld.get('technology_stack_recommendation', '')}

Create detailed LLD with:
1. Detailed Component Design (classes, modules)
2. Database Schema Design
3. API Endpoints Design
4. Data Models
5. Business Logic Flow
6. Error Handling Strategy
7. Logging and Monitoring
8. Testing Strategy

Format as JSON."""

        try:
            response = await model_router.generate(prompt, provider=model_provider, max_tokens=4000)
            import json
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                lld = json.loads(json_match.group(0))
            else:
                lld = self._create_fallback_lld(parsed_requirement, hld)

            return lld
        except Exception as e:
            logger.error(f"Error generating LLD: {str(e)}")
            return self._create_fallback_lld(parsed_requirement, hld)

    async def generate_api_specification(
        self,
        lld: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """Generate OpenAPI specification"""
        logger.info("Generating API specification...")

        api_design = lld.get('api_endpoints_design', '')

        prompt = f"""Generate an OpenAPI 3.0 specification based on this API design:

{api_design}

Create a valid OpenAPI JSON specification with:
- All endpoints
- Request/Response schemas
- Authentication
- Error responses

Format as valid OpenAPI 3.0 JSON."""

        try:
            response = await model_router.generate(prompt, provider=model_provider, max_tokens=3000)
            import json
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return self._create_fallback_api_spec()
        except Exception as e:
            logger.error(f"Error generating API spec: {str(e)}")
            return self._create_fallback_api_spec()

    async def generate_database_schema(
        self,
        lld: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """Generate database schema"""
        logger.info("Generating database schema...")

        db_design = lld.get('database_schema_design', '')
        data_models = lld.get('data_models', '')

        prompt = f"""Generate a database schema based on:

Schema Design: {db_design}
Data Models: {data_models}

Create a detailed schema with:
- Tables
- Columns with data types
- Primary keys
- Foreign keys
- Indexes
- Constraints

Format as JSON with table definitions."""

        try:
            response = await model_router.generate(prompt, provider=model_provider, max_tokens=2000)
            import json
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return self._create_fallback_db_schema()
        except Exception as e:
            logger.error(f"Error generating DB schema: {str(e)}")
            return self._create_fallback_db_schema()

    def _format_qa_pairs(self, interview_data: Dict[str, Any]) -> str:
        """Format Q&A pairs for prompts"""
        questions = interview_data.get('questions', [])
        answers = interview_data.get('answers', [])

        pairs = []
        for i, (q, a) in enumerate(zip(questions, answers), 1):
            pairs.append(f"Q{i}: {q.get('question', '')}")
            pairs.append(f"A{i}: {a.get('answer', '')}\n")

        return "\n".join(pairs)

    def _determine_tech_stack(
        self,
        parsed_requirement: Dict[str, Any],
        interview_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Determine recommended tech stack"""
        tech_prefs = parsed_requirement.get('tech_preferences', {})

        # Default tech stack
        tech_stack = {
            "frontend": {
                "framework": "React 18",
                "styling": "TailwindCSS",
                "state_management": "Redux Toolkit"
            },
            "backend": {
                "language": "Python 3.12",
                "framework": "FastAPI",
                "orm": "SQLAlchemy"
            },
            "database": {
                "primary": "PostgreSQL",
                "cache": "Redis"
            },
            "infrastructure": {
                "cloud": "AWS",
                "containers": "Docker",
                "orchestration": "Kubernetes"
            },
            "devops": {
                "ci_cd": "GitHub Actions",
                "iac": "Terraform"
            }
        }

        # Override with user preferences
        if tech_prefs:
            if "react" in str(tech_prefs).lower():
                tech_stack["frontend"]["framework"] = "React 18"
            if "angular" in str(tech_prefs).lower():
                tech_stack["frontend"]["framework"] = "Angular"

        return tech_stack

    def _create_fallback_brd(self, parsed_requirement: Dict, interview_data: Dict) -> Dict:
        """Create fallback BRD structure"""
        return {
            "executive_summary": f"Application in {parsed_requirement.get('domain', 'general')} domain",
            "business_objectives": parsed_requirement.get('features', []),
            "stakeholders": ["End Users", "Administrators"],
            "scope": {
                "in_scope": parsed_requirement.get('features', []),
                "out_of_scope": []
            },
            "functional_requirements": parsed_requirement.get('features', []),
            "non_functional_requirements": parsed_requirement.get('nfrs', {}),
            "assumptions": [],
            "success_criteria": []
        }

    def _create_fallback_hld(self, parsed_requirement: Dict) -> Dict:
        """Create fallback HLD structure"""
        return {
            "system_architecture_overview": "Three-tier architecture with frontend, backend, and database",
            "component_diagram": "Frontend App -> API Gateway -> Backend Services -> Database",
            "data_flow": "User -> UI -> API -> Business Logic -> Data Layer",
            "technology_stack_recommendation": self._determine_tech_stack(parsed_requirement, {}),
            "integration_points": [],
            "security_architecture": "JWT-based authentication, HTTPS, encrypted storage",
            "deployment_architecture": "Cloud-native deployment with containers",
            "scalability_considerations": "Horizontal scaling, caching, load balancing"
        }

    def _create_fallback_lld(self, parsed_requirement: Dict, hld: Dict) -> Dict:
        """Create fallback LLD structure"""
        return {
            "detailed_component_design": "Modular architecture with separated concerns",
            "database_schema_design": "Normalized relational schema",
            "api_endpoints_design": "RESTful API endpoints",
            "data_models": parsed_requirement.get('entities', []),
            "business_logic_flow": "Request -> Validation -> Processing -> Response",
            "error_handling_strategy": "Centralized error handling with proper HTTP status codes",
            "logging_and_monitoring": "Structured logging and metrics collection",
            "testing_strategy": "Unit tests, integration tests, E2E tests"
        }

    def _create_fallback_api_spec(self) -> Dict:
        """Create fallback API specification"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Generated API",
                "version": "1.0.0"
            },
            "paths": {}
        }

    def _create_fallback_db_schema(self) -> Dict:
        """Create fallback database schema"""
        return {
            "tables": [],
            "relationships": []
        }
