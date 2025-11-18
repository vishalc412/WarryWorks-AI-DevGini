"""
Code Generator Service
Generates Python backend and React frontend code from specifications
"""
import logging
from typing import Dict, List, Any
from jinja2 import Template
from app.services.model_router import model_router

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Generates complete application code"""

    def __init__(self):
        self.logger = logger

    async def generate_complete_application(
        self,
        specification: Dict[str, Any],
        model_provider: str = "openai"
    ) -> Dict[str, Any]:
        """
        Generate complete application code

        Args:
            specification: Complete specification from SpecificationGenerator
            model_provider: AI model provider

        Returns:
            Dictionary containing all generated code
        """
        logger.info("Starting complete application code generation...")

        # Extract specification components
        lld = specification.get('lld', {})
        api_spec = specification.get('api_specification', {})
        db_schema = specification.get('database_schema', {})
        tech_stack = specification.get('tech_stack', {})

        # Generate backend code
        backend_code = await self.generate_backend_code(
            lld, api_spec, db_schema, tech_stack, model_provider
        )

        # Generate frontend code
        frontend_code = await self.generate_frontend_code(
            lld, api_spec, tech_stack, model_provider
        )

        # Generate database migrations
        db_migrations = await self.generate_database_migrations(
            db_schema, model_provider
        )

        # Generate tests
        tests = await self.generate_tests(
            backend_code, frontend_code, model_provider
        )

        return {
            "backend": backend_code,
            "frontend": frontend_code,
            "database": db_migrations,
            "tests": tests,
            "config": self._generate_config_files(tech_stack)
        }

    async def generate_backend_code(
        self,
        lld: Dict[str, Any],
        api_spec: Dict[str, Any],
        db_schema: Dict[str, Any],
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate Python FastAPI backend code"""
        logger.info("Generating backend code...")

        backend_code = {}

        # Generate models
        backend_code['models.py'] = await self._generate_models(db_schema, model_provider)

        # Generate API routes
        backend_code['routes.py'] = await self._generate_routes(api_spec, model_provider)

        # Generate services/business logic
        backend_code['services.py'] = await self._generate_services(lld, model_provider)

        # Generate schemas (Pydantic)
        backend_code['schemas.py'] = await self._generate_schemas(db_schema, model_provider)

        # Generate main app file
        backend_code['main.py'] = self._generate_backend_main()

        # Generate requirements.txt
        backend_code['requirements.txt'] = self._generate_backend_requirements()

        return backend_code

    async def _generate_models(
        self,
        db_schema: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate SQLAlchemy models"""
        logger.info("Generating database models...")

        tables = db_schema.get('tables', [])

        prompt = f"""Generate SQLAlchemy ORM models for these database tables:

{tables}

Requirements:
- Use SQLAlchemy declarative base
- Include all columns with proper types
- Add relationships and foreign keys
- Include timestamps (created_at, updated_at)
- Add __repr__ methods

Generate complete Python code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=2000)
            # Extract code from markdown if present
            import re
            code_match = re.search(r'```python\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            logger.error(f"Error generating models: {str(e)}")
            return self._get_fallback_models()

    async def _generate_routes(
        self,
        api_spec: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate FastAPI routes"""
        logger.info("Generating API routes...")

        paths = api_spec.get('paths', {})

        prompt = f"""Generate FastAPI router with these endpoints:

{paths}

Requirements:
- Use FastAPI APIRouter
- Include proper request/response models
- Add proper HTTP methods (GET, POST, PUT, DELETE)
- Include error handling
- Add dependencies for database session
- Include docstrings

Generate complete Python code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=2500)
            import re
            code_match = re.search(r'```python\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            logger.error(f"Error generating routes: {str(e)}")
            return self._get_fallback_routes()

    async def _generate_services(
        self,
        lld: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate business logic services"""
        logger.info("Generating services...")

        business_logic = lld.get('business_logic_flow', '')

        prompt = f"""Generate service layer with business logic:

{business_logic}

Requirements:
- Create service classes
- Implement CRUD operations
- Add business logic methods
- Include error handling
- Use dependency injection pattern

Generate complete Python code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=2000)
            import re
            code_match = re.search(r'```python\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            logger.error(f"Error generating services: {str(e)}")
            return self._get_fallback_services()

    async def _generate_schemas(
        self,
        db_schema: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate Pydantic schemas"""
        logger.info("Generating Pydantic schemas...")

        tables = db_schema.get('tables', [])

        prompt = f"""Generate Pydantic schemas for API request/response validation:

Tables: {tables}

Requirements:
- Create BaseModel classes
- Include Create, Update, and Response schemas
- Add field validation
- Include examples in Config

Generate complete Python code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1500)
            import re
            code_match = re.search(r'```python\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            logger.error(f"Error generating schemas: {str(e)}")
            return self._get_fallback_schemas()

    async def generate_frontend_code(
        self,
        lld: Dict[str, Any],
        api_spec: Dict[str, Any],
        tech_stack: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate React frontend code"""
        logger.info("Generating frontend code...")

        frontend_code = {}

        # Generate React components
        frontend_code['App.jsx'] = await self._generate_react_app(lld, model_provider)

        # Generate API client
        frontend_code['api/client.js'] = await self._generate_api_client(api_spec, model_provider)

        # Generate Redux store
        frontend_code['store/index.js'] = self._generate_redux_store()

        # Generate main component
        frontend_code['components/MainLayout.jsx'] = await self._generate_main_layout(model_provider)

        # Generate package.json
        frontend_code['package.json'] = self._generate_package_json()

        # Generate tailwind config
        frontend_code['tailwind.config.js'] = self._generate_tailwind_config()

        return frontend_code

    async def _generate_react_app(
        self,
        lld: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate main React App component"""
        logger.info("Generating React App...")

        prompt = """Generate a React 18 App.jsx component with:
- React Router setup
- Redux Provider
- Main routes
- Error boundary
- Loading states

Generate complete React code with hooks."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1500)
            import re
            code_match = re.search(r'```jsx\n(.*?)\n```', code, re.DOTALL)
            if not code_match:
                code_match = re.search(r'```javascript\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            logger.error(f"Error generating React app: {str(e)}")
            return self._get_fallback_react_app()

    async def _generate_api_client(
        self,
        api_spec: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate API client for frontend"""
        logger.info("Generating API client...")

        paths = api_spec.get('paths', {})

        prompt = f"""Generate an Axios-based API client for these endpoints:

{paths}

Requirements:
- Use axios
- Create API client class
- Include all HTTP methods
- Add request/response interceptors
- Handle errors properly

Generate complete JavaScript code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1500)
            import re
            code_match = re.search(r'```javascript\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            logger.error(f"Error generating API client: {str(e)}")
            return self._get_fallback_api_client()

    async def _generate_main_layout(self, model_provider: str) -> str:
        """Generate main layout component"""
        prompt = """Generate a React MainLayout component with:
- Navigation bar
- Sidebar
- Main content area
- Footer
- Responsive design with Tailwind

Generate complete JSX code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1000)
            import re
            code_match = re.search(r'```jsx\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return code
        except Exception as e:
            return self._get_fallback_main_layout()

    async def generate_database_migrations(
        self,
        db_schema: Dict[str, Any],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate Alembic database migrations"""
        logger.info("Generating database migrations...")

        migrations = {}

        # Generate initial migration
        migrations['initial_migration.py'] = await self._generate_initial_migration(
            db_schema, model_provider
        )

        # Generate alembic.ini
        migrations['alembic.ini'] = self._generate_alembic_ini()

        return migrations

    async def _generate_initial_migration(
        self,
        db_schema: Dict[str, Any],
        model_provider: str
    ) -> str:
        """Generate initial Alembic migration"""
        tables = db_schema.get('tables', [])

        prompt = f"""Generate an Alembic migration file to create these tables:

{tables}

Requirements:
- Use Alembic op.create_table
- Include all columns
- Add indexes
- Add foreign keys

Generate complete Python migration code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1500)
            return code
        except Exception as e:
            return self._get_fallback_migration()

    async def generate_tests(
        self,
        backend_code: Dict[str, str],
        frontend_code: Dict[str, str],
        model_provider: str
    ) -> Dict[str, str]:
        """Generate test files"""
        logger.info("Generating tests...")

        tests = {}

        # Backend tests
        tests['test_backend.py'] = await self._generate_backend_tests(backend_code, model_provider)

        # Frontend tests
        tests['test_frontend.jsx'] = await self._generate_frontend_tests(frontend_code, model_provider)

        return tests

    async def _generate_backend_tests(
        self,
        backend_code: Dict[str, str],
        model_provider: str
    ) -> str:
        """Generate pytest tests for backend"""
        prompt = """Generate pytest tests for FastAPI application:
- Test API endpoints
- Test database operations
- Use pytest fixtures
- Include test client

Generate complete Python test code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1500)
            return code
        except Exception as e:
            return "# Backend tests to be implemented"

    async def _generate_frontend_tests(
        self,
        frontend_code: Dict[str, str],
        model_provider: str
    ) -> str:
        """Generate Jest/React Testing Library tests"""
        prompt = """Generate React component tests using Jest and RTL:
- Test component rendering
- Test user interactions
- Mock API calls

Generate complete test code."""

        try:
            code = await model_router.generate(prompt, provider=model_provider, max_tokens=1000)
            return code
        except Exception as e:
            return "// Frontend tests to be implemented"

    def _generate_config_files(self, tech_stack: Dict[str, Any]) -> Dict[str, str]:
        """Generate configuration files"""
        return {
            ".env.example": self._generate_env_example(),
            ".gitignore": self._generate_gitignore(),
            "README.md": self._generate_readme()
        }

    # Fallback methods
    def _get_fallback_models(self) -> str:
        return '''"""Database models"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''

    def _get_fallback_routes(self) -> str:
        return '''"""API routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "API is running"}
'''

    def _get_fallback_services(self) -> str:
        return '''"""Business logic services"""

class BaseService:
    def __init__(self, db):
        self.db = db
'''

    def _get_fallback_schemas(self) -> str:
        return '''"""Pydantic schemas"""
from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
'''

    def _get_fallback_react_app(self) -> str:
        return '''import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Welcome to Generated App</h1>
      </div>
    </Router>
  );
}

export default App;
'''

    def _get_fallback_api_client(self) -> str:
        return '''import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
'''

    def _get_fallback_main_layout(self) -> str:
        return '''import React from 'react';

const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="container mx-auto px-4 py-3">
          <h1 className="text-xl font-bold">Application</h1>
        </div>
      </nav>
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
};

export default MainLayout;
'''

    def _get_fallback_migration(self) -> str:
        return '''"""Initial migration"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
'''

    def _generate_backend_main(self) -> str:
        return '''"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generated API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}
'''

    def _generate_backend_requirements(self) -> str:
        return '''fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
alembic==1.13.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
'''

    def _generate_redux_store(self) -> str:
        return '''import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {},
});
'''

    def _generate_package_json(self) -> str:
        return '''{
  "name": "generated-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
'''

    def _generate_tailwind_config(self) -> str:
        return '''module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
'''

    def _generate_alembic_ini(self) -> str:
        return '''[alembic]
script_location = alembic
sqlalchemy.url = postgresql://postgres:postgres@localhost/dbname
'''

    def _generate_env_example(self) -> str:
        return '''DATABASE_URL=postgresql://postgres:postgres@localhost/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
'''

    def _generate_gitignore(self) -> str:
        return '''__pycache__/
*.py[cod]
.env
.venv
venv/
node_modules/
.DS_Store
*.log
'''

    def _generate_readme(self) -> str:
        return '''# Generated Application

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```
'''
