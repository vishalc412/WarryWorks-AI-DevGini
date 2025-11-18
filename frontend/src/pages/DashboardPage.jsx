import React from 'react'
import { Link } from 'react-router-dom'
import { FolderOpen, Plus } from 'lucide-react'

const DashboardPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Projects</h1>
          <Link to="/" className="btn btn-primary flex items-center gap-2">
            <Plus className="w-5 h-5" />
            New Project
          </Link>
        </div>

        <div className="card text-center py-12">
          <FolderOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            No projects yet
          </h2>
          <p className="text-gray-600 mb-6">
            Create your first project to get started
          </p>
          <Link to="/" className="btn btn-primary inline-flex items-center gap-2">
            <Plus className="w-5 h-5" />
            Create Project
          </Link>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
