import api from './api'
import { Feedback, WeeklyReport, TrendData, Insight } from '../types'

export const feedbackService = {
  uploadFile: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/feedback/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getFeedback: async (params?: {
    week_start?: string
    batch?: string
    location?: string
    skip?: number
    limit?: number
  }): Promise<Feedback[]> => {
    const response = await api.get('/feedback/', { params })
    return response.data
  },
}

export const reportService = {
  generateWeeklyReport: async (week_start: string): Promise<WeeklyReport> => {
    // Send week_start as query parameter
    const response = await api.post(`/reports/weekly/generate?week_start=${week_start}`)
    return response.data
  },

  getWeeklyReport: async (week_id: number): Promise<WeeklyReport> => {
    const response = await api.get(`/reports/weekly/${week_id}`)
    return response.data
  },

  listWeeklyReports: async (skip = 0, limit = 10): Promise<WeeklyReport[]> => {
    const response = await api.get('/reports/weekly', { params: { skip, limit } })
    return response.data
  },
}

export const analysisService = {
  getTrends: async (week_start: string): Promise<TrendData> => {
    const response = await api.get('/analysis/trends', {
      params: { week_start },
    })
    return response.data
  },

  getInsights: async (week_start: string): Promise<Insight> => {
    const response = await api.get('/analysis/insights', {
      params: { week_start },
    })
    return response.data
  },

  getLifecycleTrends: async (week_start: string) => {
    const response = await api.get('/analysis/lifecycle', {
      params: { week_start },
    })
    return response.data
  },

  getCategoryTrends: async (week_start: string, weeks_back = 8) => {
    const response = await api.get('/analysis/category-trends', {
      params: { week_start, weeks_back },
    })
    return response.data
  },

  get8WeekTrends: async (week_start: string) => {
    const response = await api.get('/analysis/8-week-trends', {
      params: { week_start },
    })
    return response.data
  },

  getCategoryHeatmap: async (week_start: string) => {
    const response = await api.get('/analysis/category-heatmap', {
      params: { week_start },
    })
    return response.data
  },
}

export const syncService = {
  uploadFeedback: async (file: File, week_start?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    if (week_start) {
      formData.append('week_start', week_start)
    }
    
    const response = await api.post('/sync/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getSyncStatus: async () => {
    const response = await api.get('/sync/status')
    return response.data
  },
}

export const pdfService = {
  exportPDF: async (week_id: number): Promise<Blob> => {
    const response = await api.get(`/reports/export/pdf/${week_id}`, {
      responseType: 'blob',
    })
    return response.data
  },
}

