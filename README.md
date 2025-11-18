# Lovable-AI Builder Platform

**Transform your ideas into production-ready applications with AI-powered code generation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)

## 🚀 Overview

Lovable-AI Builder Platform is an end-to-end AI-powered application engineering system that:

- **Captures Requirements** through an intelligent AI-driven interview process
- **Generates Complete Specifications** (BRD, HLD, LLD)
- **Creates Production-Ready Code** (Backend + Frontend + Database)
- **Produces DevOps Assets** (Docker, Kubernetes, Terraform, CI/CD)
- **Supports Multiple AI Models** (OpenAI, Anthropic, Google Gemini)

**Reduce engineering effort by 80-90% and ship faster!**

---

## ✨ Features

### 🎯 AI-Driven Requirements Gathering
- Adaptive questioning based on project domain
- Multi-phase interview (Purpose → Workflows → Data → NFRs → Tech Stack)
- Real-time coverage scoring
- Context-aware follow-up questions

### 📋 Automatic Specification Generation
- **Business Requirements Document (BRD)**
- **High-Level Design (HLD)**
- **Low-Level Design (LLD)**
- **API Specifications (OpenAPI 3.0)**
- **Database Schema Design**

### 💻 Full-Stack Code Generation
- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Frontend**: React 18 with Redux Toolkit & TailwindCSS
- **Database**: PostgreSQL schemas and migrations
- **API**: RESTful endpoints with request/response validation
- **Tests**: Unit and integration test scaffolding

### 🔧 DevOps Automation
- **Docker**: Multi-stage Dockerfiles for optimal builds
- **Kubernetes**: Deployment, Service, Ingress manifests
- **Terraform**: Infrastructure as Code for AWS/Azure/GCP
- **CI/CD**: GitHub Actions workflows
- **Helm**: Kubernetes package management charts

### 🤖 Multi-Model Support
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude (Opus, Sonnet, Haiku)
- Google Gemini
- Easy model switching and comparison

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.12+** (for local development)
- **Node.js 20+** (for frontend development)
- **PostgreSQL 15+** (if not using Docker)
- **Redis** (if not using Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/vishalc412/WarryWorks-AI-DevGini.git
cd WarryWorks-AI-DevGini
```

### 2. Set Up Environment Variables

```bash
# Copy environment examples
cp .env.example .env
cp frontend/.env.example frontend/.env

# Edit .env and add your API keys
```

**Important**: Add your API keys to `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-google-key-here
```

### 3. Run with Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services will be available at:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

---

## 📖 Usage Guide

### 1. Create a New Project

1. Open http://localhost:3000
2. Enter your project title and detailed description
3. Click "Start AI Interview"

### 2. Complete the AI Interview

- Answer questions about your application
- The AI adapts based on your responses
- Monitor the coverage score (aim for 70%+)

### 3. Generate Your Application

1. Once interview is complete, proceed to generation
2. Click "Generate Complete Application"
3. Download generated code artifacts

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Cache**: Redis 7
- **Task Queue**: Celery
- **AI Integration**: OpenAI, Anthropic, Google SDKs

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS 3
- **State Management**: Redux Toolkit
- **HTTP Client**: Axios

### DevOps
- **Containers**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **IaC**: Terraform
- **CI/CD**: GitHub Actions

---

## 📁 Project Structure

```
WarryWorks-AI-DevGini/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI endpoints
│   │   ├── core/             # Configuration
│   │   ├── db/               # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── store/            # Redux store
│   │   └── App.jsx
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## 🔧 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 📝 License

This project is licensed under the MIT License.

---

**Built with ❤️ by the WarryWorks Team**