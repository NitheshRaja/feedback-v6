import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert,
} from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { format } from 'date-fns'
import { reportService, analysisService } from '../services/feedback'
import { WeeklyReport, Insight } from '../types'

const ReportDetails = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [report, setReport] = useState<WeeklyReport | null>(null)
  const [insights, setInsights] = useState<Insight | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (id) {
      loadReportDetails()
    }
  }, [id])

  const loadReportDetails = async () => {
    try {
      setLoading(true)
      const reportId = parseInt(id || '0')
      const reportData = await reportService.getWeeklyReport(reportId)
      setReport(reportData)
      
      // Load insights after we have the report data
      if (reportData.week_start_date) {
        try {
          const insights = await analysisService.getInsights(reportData.week_start_date)
          setInsights(insights)
        } catch (insightError) {
          // Insights might fail if no previous week data exists, that's okay
          console.warn('Could not load insights:', insightError)
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load report details')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  if (error || !report) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error" sx={{ mt: 3 }}>
          {error || 'Report not found'}
        </Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/reports')}
          sx={{ mt: 2 }}
        >
          Back to Reports
        </Button>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ pb: 4 }}>
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/reports')}
        >
          Back to Reports
        </Button>
        <Typography variant="h4">
          Weekly Report Details
        </Typography>
      </Box>

      {/* Week Overview */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Week Overview
        </Typography>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Week Period
                </Typography>
                <Typography variant="h6">
                  {format(new Date(report.week_start_date), 'MMM dd')} -{' '}
                  {format(new Date(report.week_end_date), 'MMM dd, yyyy')}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Overall Sentiment
                </Typography>
                <Typography variant="h6">
                  {report.overall_sentiment_score.toFixed(1)}%
                </Typography>
                {report.sentiment_change !== null && report.sentiment_change !== undefined && (
                  <Typography
                    variant="body2"
                    color={report.sentiment_change > 0 ? 'success.main' : 'error.main'}
                  >
                    {report.sentiment_change > 0 ? '+' : ''}
                    {report.sentiment_change.toFixed(1)}% from last week
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Heat Index
                </Typography>
                <Typography variant="h6">
                  {report.heat_index.toFixed(1)}
                </Typography>
                <Chip
                  label={
                    report.heat_index >= 80
                      ? 'Excellent'
                      : report.heat_index >= 60
                      ? 'Good'
                      : report.heat_index >= 40
                      ? 'Moderate'
                      : 'Poor'
                  }
                  color={
                    report.heat_index >= 80
                      ? 'success'
                      : report.heat_index >= 60
                      ? 'primary'
                      : report.heat_index >= 40
                      ? 'warning'
                      : 'error'
                  }
                  size="small"
                  sx={{ mt: 1 }}
                />
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Total Feedback
                </Typography>
                <Typography variant="h6">
                  {report.total_feedback_count}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>

      {/* Executive Summary */}
      {report.executive_summary && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Executive Summary
          </Typography>
          <Typography
            variant="body1"
            sx={{ whiteSpace: 'pre-line', mt: 2 }}
          >
            {report.executive_summary}
          </Typography>
        </Paper>
      )}

      {/* Insights and Action Items */}
      {insights && (
        <>
          {insights.action_items && insights.action_items.length > 0 && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom>
                Action Items
              </Typography>
              <Box sx={{ mt: 2 }}>
                {insights.action_items.map((item, index) => (
                  <Card key={index} sx={{ mb: 2 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1 }}>
                        <Typography variant="h6">{item.title}</Typography>
                        <Chip
                          label={item.priority.toUpperCase()}
                          color={
                            item.priority === 'urgent'
                              ? 'error'
                              : item.priority === 'high'
                              ? 'warning'
                              : item.priority === 'medium'
                              ? 'info'
                              : 'default'
                          }
                          size="small"
                        />
                      </Box>
                      {item.category && (
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Category: {item.category.replace('_', ' ').toUpperCase()}
                        </Typography>
                      )}
                      <Typography variant="body2">{item.description}</Typography>
                      {item.confidence_score && (
                        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                          Confidence: {(item.confidence_score * 100).toFixed(0)}%
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </Box>
            </Paper>
          )}

          {insights.risk_flags && insights.risk_flags.length > 0 && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom>
                Risk Flags
              </Typography>
              <Box sx={{ mt: 2 }}>
                {insights.risk_flags.map((flag, index) => (
                  <Alert
                    key={index}
                    severity={flag.severity === 'high' ? 'error' : 'warning'}
                    sx={{ mb: 2 }}
                  >
                    <Typography variant="subtitle2">{flag.message}</Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {flag.recommendation}
                    </Typography>
                  </Alert>
                ))}
              </Box>
            </Paper>
          )}

          {insights.assessment_stress && insights.assessment_stress.detected && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom>
                Assessment Stress Detection
              </Typography>
              <Alert severity="info" sx={{ mt: 2 }}>
                <Typography variant="subtitle2">{insights.assessment_stress.message}</Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {insights.assessment_stress.recommendation}
                </Typography>
                <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
                  Confidence: {(insights.assessment_stress.confidence * 100).toFixed(0)}%
                </Typography>
              </Alert>
            </Paper>
          )}
        </>
      )}
    </Container>
  )
}

export default ReportDetails

