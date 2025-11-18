import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../../utils/api'

export const getNextQuestion = createAsyncThunk(
  'interview/nextQuestion',
  async ({ sessionId, answer, modelProvider = 'openai' }) => {
    const response = await api.post('/interview/next', {
      session_id: sessionId,
      answer,
      model_provider: modelProvider,
    })
    return response.data
  }
)

export const fetchInterviewStatus = createAsyncThunk(
  'interview/status',
  async (sessionId) => {
    const response = await api.get(`/interview/status/${sessionId}`)
    return response.data
  }
)

const interviewSlice = createSlice({
  name: 'interview',
  initialState: {
    currentQuestion: null,
    history: [],
    phase: null,
    coverageScore: 0,
    isComplete: false,
    loading: false,
    error: null,
  },
  reducers: {
    addAnswer: (state, action) => {
      state.history.push({
        question: state.currentQuestion,
        answer: action.payload,
      })
    },
    resetInterview: (state) => {
      state.currentQuestion = null
      state.history = []
      state.phase = null
      state.coverageScore = 0
      state.isComplete = false
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getNextQuestion.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(getNextQuestion.fulfilled, (state, action) => {
        state.loading = false
        state.currentQuestion = action.payload.question
        state.phase = action.payload.phase
        state.coverageScore = action.payload.coverage_score
        state.isComplete = action.payload.is_complete
      })
      .addCase(getNextQuestion.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      .addCase(fetchInterviewStatus.fulfilled, (state, action) => {
        state.coverageScore = action.payload.coverage_score
        state.isComplete = action.payload.is_complete
      })
  },
})

export const { addAnswer, resetInterview } = interviewSlice.actions
export default interviewSlice.reducer
