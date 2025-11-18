import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../../utils/api'

export const generateSpecification = createAsyncThunk(
  'generation/spec',
  async ({ projectId, modelProvider = 'openai' }) => {
    const response = await api.post('/generate/spec', {
      project_id: projectId,
      model_provider: modelProvider,
    })
    return response.data
  }
)

export const generateCode = createAsyncThunk(
  'generation/code',
  async ({ projectId, modelProvider = 'openai' }) => {
    const response = await api.post('/generate/code', {
      project_id: projectId,
      model_provider: modelProvider,
    })
    return response.data
  }
)

export const generateDevOps = createAsyncThunk(
  'generation/devops',
  async ({ projectId, modelProvider = 'openai' }) => {
    const response = await api.post('/generate/devops', {
      project_id: projectId,
      model_provider: modelProvider,
    })
    return response.data
  }
)

export const fetchArtifacts = createAsyncThunk(
  'generation/artifacts',
  async (projectId) => {
    const response = await api.get(`/generate/artifacts/${projectId}`)
    return response.data
  }
)

const generationSlice = createSlice({
  name: 'generation',
  initialState: {
    artifacts: [],
    loading: false,
    error: null,
    progress: {
      spec: 'pending',
      code: 'pending',
      devops: 'pending',
    },
  },
  reducers: {
    resetGeneration: (state) => {
      state.artifacts = []
      state.progress = {
        spec: 'pending',
        code: 'pending',
        devops: 'pending',
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Specification generation
      .addCase(generateSpecification.pending, (state) => {
        state.loading = true
        state.progress.spec = 'in_progress'
      })
      .addCase(generateSpecification.fulfilled, (state, action) => {
        state.loading = false
        state.progress.spec = 'completed'
        state.artifacts = [...state.artifacts, ...action.payload.artifacts]
      })
      .addCase(generateSpecification.rejected, (state, action) => {
        state.loading = false
        state.progress.spec = 'failed'
        state.error = action.error.message
      })
      // Code generation
      .addCase(generateCode.pending, (state) => {
        state.loading = true
        state.progress.code = 'in_progress'
      })
      .addCase(generateCode.fulfilled, (state, action) => {
        state.loading = false
        state.progress.code = 'completed'
        state.artifacts = [...state.artifacts, ...action.payload.artifacts]
      })
      .addCase(generateCode.rejected, (state, action) => {
        state.loading = false
        state.progress.code = 'failed'
        state.error = action.error.message
      })
      // DevOps generation
      .addCase(generateDevOps.pending, (state) => {
        state.loading = true
        state.progress.devops = 'in_progress'
      })
      .addCase(generateDevOps.fulfilled, (state, action) => {
        state.loading = false
        state.progress.devops = 'completed'
        state.artifacts = [...state.artifacts, ...action.payload.artifacts]
      })
      .addCase(generateDevOps.rejected, (state, action) => {
        state.loading = false
        state.progress.devops = 'failed'
        state.error = action.error.message
      })
      // Fetch artifacts
      .addCase(fetchArtifacts.fulfilled, (state, action) => {
        state.artifacts = action.payload.artifacts
      })
  },
})

export const { resetGeneration } = generationSlice.actions
export default generationSlice.reducer
