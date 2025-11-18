import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../../utils/api'

export const createProject = createAsyncThunk(
  'project/create',
  async (requirementData) => {
    const response = await api.post('/requirements/ingest', requirementData)
    return response.data
  }
)

export const fetchProject = createAsyncThunk(
  'project/fetch',
  async (projectId) => {
    const response = await api.get(`/requirements/project/${projectId}`)
    return response.data
  }
)

const projectSlice = createSlice({
  name: 'project',
  initialState: {
    current: null,
    sessionId: null,
    parsedRequirement: null,
    loading: false,
    error: null,
  },
  reducers: {
    clearProject: (state) => {
      state.current = null
      state.sessionId = null
      state.parsedRequirement = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(createProject.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(createProject.fulfilled, (state, action) => {
        state.loading = false
        state.current = { id: action.payload.project_id }
        state.sessionId = action.payload.session_id
        state.parsedRequirement = action.payload.parsed_requirement
      })
      .addCase(createProject.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      .addCase(fetchProject.fulfilled, (state, action) => {
        state.current = action.payload
      })
  },
})

export const { clearProject } = projectSlice.actions
export default projectSlice.reducer
