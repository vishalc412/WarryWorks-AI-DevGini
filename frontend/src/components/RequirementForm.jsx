import React, { useState } from 'react'
import { Send } from 'lucide-react'

const RequirementForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.title && formData.description) {
      onSubmit(formData)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const isValid = formData.title.length > 3 && formData.description.length > 20

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6 text-center">
        Start Your Project
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            Project Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="e.g., E-commerce Platform for Handmade Crafts"
            className="input"
            required
            disabled={loading}
          />
          <p className="mt-1 text-sm text-gray-500">
            Give your project a descriptive title
          </p>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            Project Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe your project idea in detail. What problem does it solve? Who are the users? What features do you need?"
            rows={8}
            className="input resize-none"
            required
            disabled={loading}
          />
          <p className="mt-1 text-sm text-gray-500">
            {formData.description.length} characters (minimum 20)
          </p>
        </div>

        <button
          type="submit"
          disabled={!isValid || loading}
          className="w-full btn btn-primary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
              Processing...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              Start AI Interview
            </>
          )}
        </button>

        {!isValid && formData.description.length > 0 && (
          <p className="text-sm text-amber-600 text-center">
            Please provide more details (at least 20 characters)
          </p>
        )}
      </form>
    </div>
  )
}

export default RequirementForm
