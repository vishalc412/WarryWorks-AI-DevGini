import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { getNextQuestion } from '../store/slices/interviewSlice'
import ChatWindow from '../components/ChatWindow'
import ProgressBar from '../components/ProgressBar'
import { CheckCircle } from 'lucide-react'

const InterviewPage = () => {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const { currentQuestion, coverageScore, isComplete, loading } = useSelector(
    (state) => state.interview
  )
  const { current: project } = useSelector((state) => state.project)
  const [answer, setAnswer] = useState('')

  useEffect(() => {
    // Get the first question
    if (!currentQuestion) {
      handleSubmitAnswer('')
    }
  }, [])

  const handleSubmitAnswer = async (userAnswer) => {
    try {
      await dispatch(
        getNextQuestion({
          sessionId,
          answer: userAnswer,
          modelProvider: 'openai',
        })
      ).unwrap()
      setAnswer('')
    } catch (error) {
      console.error('Failed to get next question:', error)
    }
  }

  const handleComplete = () => {
    if (project?.id) {
      navigate(`/generate/${project.id}`)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            AI Requirements Interview
          </h1>
          <p className="text-gray-600">
            Answer the questions to help us understand your project better
          </p>
        </div>

        {/* Progress */}
        <div className="card mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Requirement Coverage
            </span>
            <span className="text-sm font-bold text-primary-600">
              {coverageScore}%
            </span>
          </div>
          <ProgressBar progress={coverageScore} />
          {isComplete && (
            <div className="mt-4 flex items-center gap-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <span className="font-medium">Interview Complete!</span>
            </div>
          )}
        </div>

        {/* Chat Window */}
        <ChatWindow
          currentQuestion={currentQuestion}
          onSubmitAnswer={handleSubmitAnswer}
          loading={loading}
          isComplete={isComplete}
        />

        {/* Complete Button */}
        {isComplete && (
          <div className="mt-6">
            <button
              onClick={handleComplete}
              className="w-full btn btn-primary"
            >
              Proceed to Code Generation →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default InterviewPage
