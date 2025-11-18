import { configureStore } from '@reduxjs/toolkit'
import projectReducer from './slices/projectSlice'
import interviewReducer from './slices/interviewSlice'
import generationReducer from './slices/generationSlice'

export const store = configureStore({
  reducer: {
    project: projectReducer,
    interview: interviewReducer,
    generation: generationReducer,
  },
})
