export interface User {
  id: number
  email: string
  full_name: string
  role: 'admin' | 'batch_owner' | 'leadership' | 'system_owner'
  is_active: boolean
  batch_access?: string
}

export interface Feedback {
  id: number
  trainee_id: string
  location: string
  training_batch: string
  rating_score?: number
  sentiment_category?: string
  confidence_score?: number
}

export interface WeeklyReport {
  id: number
  week_start_date: string
  week_end_date: string
  overall_sentiment_score: number
  sentiment_change?: number
  heat_index: number
  total_feedback_count: number
  executive_summary?: string
}

export interface TrendData {
  current_week: {
    positive: number
    neutral: number
    negative: number
  }
  previous_week: {
    positive: number
    neutral: number
    negative: number
  }
  changes: {
    positive: number
    neutral: number
    negative: number
  }
  overall_change: number
  current_volume: number
  previous_volume: number
  volume_change: number
}

export interface ActionItem {
  priority: 'low' | 'medium' | 'high' | 'urgent'
  category?: string
  title: string
  description: string
  confidence_score?: number
  assigned_to?: string
}

export interface StrengthConcern {
  category: string
  description: string
  quotes?: string[]
}

export interface AppreciationItem {
  text: string
  location: string
  batch: string
}

export interface Insight {
  action_items: ActionItem[]
  risk_flags: Array<{
    type: string
    severity: string
    message: string
    category: string
    recommendation: string
  }>
  assessment_stress?: {
    detected: boolean
    confidence: number
    message: string
    recommendation: string
  }
  executive_summary: string
  appreciation_tracker?: {
    trainer_recognition: AppreciationItem[]
    mentor_recognition: AppreciationItem[]
    general_appreciation: AppreciationItem[]
    total_positive_feedback: number
  }
  unresolved_loops?: Array<{
    detected: boolean
    weeks_affected: number
    message: string
    details: any[]
    recommendation: string
  }>
  praise_momentum?: {
    trend: string
    change: number
    current_positive_pct: number
    weeks_data: any[]
    trainer_recognition_trend: string
    mentor_recognition_trend: string
  }
}

