import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  generateSpecification,
  generateCode,
  generateDevOps,
  fetchArtifacts,
} from '../store/slices/generationSlice'
import CodePreview from '../components/CodePreview'
import { FileCode, Database, Server, CheckCircle, Loader } from 'lucide-react'

const GeneratePage = () => {
  const { projectId } = useParams()
  const dispatch = useDispatch()
  const { progress, artifacts, loading } = useSelector((state) => state.generation)
  const [selectedArtifact, setSelectedArtifact] = useState(null)

  const handleGenerateAll = async () => {
    try {
      await dispatch(
        generateSpecification({ projectId: parseInt(projectId), modelProvider: 'openai' })
      ).unwrap()

      await dispatch(
        generateCode({ projectId: parseInt(projectId), modelProvider: 'openai' })
      ).unwrap()

      await dispatch(
        generateDevOps({ projectId: parseInt(projectId), modelProvider: 'openai' })
      ).unwrap()

      dispatch(fetchArtifacts(projectId))
    } catch (error) {
      console.error('Generation failed:', error)
    }
  }

  const renderStepStatus = (status) => {
    if (status === 'completed') {
      return <CheckCircle className="w-5 h-5 text-green-600" />
    } else if (status === 'in_progress') {
      return <Loader className="w-5 h-5 text-primary-600 animate-spin" />
    }
    return <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Code Generation
          </h1>
          <p className="text-gray-600">
            Generate your complete application with AI
          </p>
        </div>

        {/* Generation Steps */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center gap-3 mb-3">
              {renderStepStatus(progress.spec)}
              <FileCode className="w-6 h-6 text-gray-600" />
              <h3 className="font-semibold">Specifications</h3>
            </div>
            <p className="text-sm text-gray-600">
              BRD, HLD, LLD documents
            </p>
          </div>

          <div className="card">
            <div className="flex items-center gap-3 mb-3">
              {renderStepStatus(progress.code)}
              <Database className="w-6 h-6 text-gray-600" />
              <h3 className="font-semibold">Application Code</h3>
            </div>
            <p className="text-sm text-gray-600">
              Backend, Frontend, Database
            </p>
          </div>

          <div className="card">
            <div className="flex items-center gap-3 mb-3">
              {renderStepStatus(progress.devops)}
              <Server className="w-6 h-6 text-gray-600" />
              <h3 className="font-semibold">DevOps Assets</h3>
            </div>
            <p className="text-sm text-gray-600">
              Docker, K8s, CI/CD pipelines
            </p>
          </div>
        </div>

        {/* Generate Button */}
        {progress.spec === 'pending' && (
          <div className="text-center mb-8">
            <button
              onClick={handleGenerateAll}
              disabled={loading}
              className="btn btn-primary text-lg px-8 py-3 disabled:opacity-50"
            >
              {loading ? 'Generating...' : 'Generate Complete Application'}
            </button>
          </div>
        )}

        {/* Artifacts List */}
        {artifacts.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Generated Artifacts</h2>
            <div className="space-y-2">
              {artifacts.map((artifact, index) => (
                <div
                  key={index}
                  className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
                  onClick={() => setSelectedArtifact(artifact)}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{artifact.name}</span>
                    <span className="text-sm text-gray-500 uppercase">
                      {artifact.type}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Code Preview */}
        {selectedArtifact && (
          <div className="mt-8">
            <CodePreview artifact={selectedArtifact} />
          </div>
        )}
      </div>
    </div>
  )
}

export default GeneratePage
