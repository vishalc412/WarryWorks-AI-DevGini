import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { createProject } from '../store/slices/projectSlice'
import RequirementForm from '../components/RequirementForm'
import { Sparkles } from 'lucide-react'

const HomePage = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const { loading } = useSelector((state) => state.project)

  const handleSubmit = async (requirementData) => {
    try {
      const result = await dispatch(createProject(requirementData)).unwrap()
      navigate(`/interview/${result.session_id}`)
    } catch (error) {
      console.error('Failed to create project:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-12 h-12 text-primary-600 mr-3" />
            <h1 className="text-5xl font-bold text-gray-900">
              Lovable-AI Builder
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform your ideas into production-ready applications with AI.
            Describe your vision, and we'll generate complete software assets.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">💡</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">AI-Driven Requirements</h3>
            <p className="text-gray-600">
              Intelligent questioning to capture complete specifications
            </p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Instant Code Generation</h3>
            <p className="text-gray-600">
              Full-stack code with backend, frontend, and database
            </p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🚀</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Production Ready</h3>
            <p className="text-gray-600">
              Complete with DevOps, CI/CD, and deployment configs
            </p>
          </div>
        </div>

        {/* Requirement Form */}
        <div className="max-w-3xl mx-auto">
          <RequirementForm onSubmit={handleSubmit} loading={loading} />
        </div>

        {/* Tech Stack Info */}
        <div className="mt-16 text-center">
          <p className="text-sm text-gray-500 mb-4">Powered by</p>
          <div className="flex justify-center gap-6 text-sm text-gray-600">
            <span>OpenAI</span>
            <span>•</span>
            <span>Anthropic Claude</span>
            <span>•</span>
            <span>Google Gemini</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage
