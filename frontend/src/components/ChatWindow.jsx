import React, { useState } from 'react'
import { Send, Bot, User } from 'lucide-react'

const ChatWindow = ({ currentQuestion, onSubmitAnswer, loading, isComplete }) => {
  const [answer, setAnswer] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (answer.trim() && !loading) {
      onSubmitAnswer(answer)
      setAnswer('')
    }
  }

  return (
    <div className="card">
      {/* Current Question */}
      {currentQuestion && (
        <div className="mb-6">
          <div className="flex gap-3">
            <div className="flex-shrink-0">
              <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6 text-primary-600" />
              </div>
            </div>
            <div className="flex-1">
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-900">{currentQuestion}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Answer Form */}
      {!isComplete && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="answer" className="block text-sm font-medium text-gray-700 mb-2">
              Your Answer
            </label>
            <textarea
              id="answer"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here..."
              rows={4}
              className="input resize-none"
              disabled={loading}
              required
            />
          </div>

          <button
            type="submit"
            disabled={!answer.trim() || loading}
            className="btn btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                Processing...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Submit Answer
              </>
            )}
          </button>
        </form>
      )}

      {isComplete && (
        <div className="text-center py-8">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">✓</span>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Interview Complete!
          </h3>
          <p className="text-gray-600">
            We have gathered enough information to generate your application.
          </p>
        </div>
      )}
    </div>
  )
}

export default ChatWindow
