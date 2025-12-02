import { useState, useEffect } from 'react'
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  TextField,
  Chip,
  Alert,
} from '@mui/material'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { format } from 'date-fns'
import { analysisService } from '../services/feedback'
import { TrendData, Insight } from '../types'

const COLORS = ['#32D74B', '#FF9F0A', '#FF453A']

const Dashboard = () => {
  const [trends, setTrends] = useState<TrendData | null>(null)
  const [insights, setInsights] = useState<Insight | null>(null)
  const [eightWeekTrends, setEightWeekTrends] = useState<any>(null)
  const [categoryHeatmap, setCategoryHeatmap] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  
  // Calculate current week start (Monday)
  const getCurrentWeekStart = () => {
    const today = new Date()
    const day = today.getDay()
    const diff = today.getDate() - day + (day === 0 ? -6 : 1) // Adjust to Monday
    const monday = new Date(today.setDate(diff))
    return format(monday, "yyyy-MM-dd")
  }

  const [selectedWeek, setSelectedWeek] = useState(getCurrentWeekStart())
  const [availableWeeks, setAvailableWeeks] = useState<string[]>([])

  useEffect(() => {
    loadAvailableWeeks()
  }, [])

  useEffect(() => {
    loadData()
  }, [selectedWeek])

  const loadAvailableWeeks = async () => {
    try {
      // Get the 8-week trends to find available weeks
      const currentWeekISO = new Date().toISOString()
      const trendsData = await analysisService.get8WeekTrends(currentWeekISO).catch(() => null)
      
      if (trendsData && trendsData.trends && trendsData.trends.length > 0) {
        // Extract available weeks from trends
        const weeks = trendsData.trends
          .filter((t: any) => t.volume > 0)
          .map((t: any) => format(new Date(t.week), 'yyyy-MM-dd'))
        
        if (weeks.length > 0) {
          setAvailableWeeks(weeks)
          // Set the most recent week with data as default
          setSelectedWeek(weeks[weeks.length - 1])
        }
      }
    } catch (error) {
      console.error('Error loading available weeks:', error)
    }
  }

  const loadData = async () => {
    try {
      setLoading(true)
      setError('')
      // Convert date to ISO format for API
      const weekStartISO = new Date(selectedWeek + 'T00:00:00').toISOString()
      
      const [trendsData, insightsData, eightWeekData, heatmapData] = await Promise.all([
        analysisService.getTrends(weekStartISO),
        analysisService.getInsights(weekStartISO),
        analysisService.get8WeekTrends(weekStartISO).catch(() => null),
        analysisService.getCategoryHeatmap(weekStartISO).catch(() => null),
      ])
      setTrends(trendsData)
      setInsights(insightsData)
      setEightWeekTrends(eightWeekData)
      setCategoryHeatmap(heatmapData)
    } catch (error: any) {
      console.error('Error loading dashboard data:', error)
      setError(error.response?.data?.detail || 'Failed to load dashboard data')
      // Set empty data on error
      setTrends(null)
      setInsights(null)
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

  const sentimentData = trends && trends.current_volume > 0
    ? [
        {
          name: 'Positive',
          current: trends.current_week.positive || 0,
          previous: trends.previous_week.positive || 0,
        },
        {
          name: 'Neutral',
          current: trends.current_week.neutral || 0,
          previous: trends.previous_week.neutral || 0,
        },
        {
          name: 'Negative',
          current: trends.current_week.negative || 0,
          previous: trends.previous_week.negative || 0,
        },
      ]
    : []

  const pieData = trends && trends.current_volume > 0
    ? [
        { name: 'Positive', value: trends.current_week.positive || 0 },
        { name: 'Neutral', value: trends.current_week.neutral || 0 },
        { name: 'Negative', value: trends.current_week.negative || 0 },
      ]
    : []

  // Handle empty state
  if (!loading && (!trends || trends.current_volume === 0)) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">
            Weekly Sentiment Dashboard
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            {availableWeeks.length > 0 && (
              <Typography variant="caption" color="text.secondary">
                Available weeks: {availableWeeks.length}
              </Typography>
            )}
            <TextField
              type="date"
              label="Select Week"
              value={selectedWeek}
              onChange={(e) => setSelectedWeek(e.target.value)}
              InputLabelProps={{ shrink: true }}
              sx={{ minWidth: 200 }}
              helperText={availableWeeks.length > 0 ? `Data available from ${availableWeeks[0]} to ${availableWeeks[availableWeeks.length - 1]}` : 'No data uploaded yet'}
            />
          </Box>
        </Box>
        {error && (
          <Box sx={{ mt: 2, mb: 2 }}>
            <Typography color="error">{error}</Typography>
          </Box>
        )}
        <Paper sx={{ p: 4, mt: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No Data Available for Selected Week
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {availableWeeks.length > 0 
              ? `Try selecting a week between ${availableWeeks[0]} and ${availableWeeks[availableWeeks.length - 1]}, or upload more CSV files.`
              : 'Upload a CSV file with feedback data to see the dashboard. Go to the Upload page to get started.'
            }
          </Typography>
        </Paper>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ pb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Weekly Sentiment Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {availableWeeks.length > 0 && (
            <Typography variant="caption" color="text.secondary">
              Available weeks: {availableWeeks.length}
            </Typography>
          )}
          <TextField
            type="date"
            label="Select Week"
            value={selectedWeek}
            onChange={(e) => setSelectedWeek(e.target.value)}
            InputLabelProps={{ shrink: true }}
            sx={{ minWidth: 200 }}
            helperText={availableWeeks.length > 0 ? `Data available from ${availableWeeks[0]} to ${availableWeeks[availableWeeks.length - 1]}` : ''}
          />
        </Box>
      </Box>
      {error && (
        <Box sx={{ mt: 2, mb: 2 }}>
          <Typography color="error">{error}</Typography>
        </Box>
      )}
      
      {/* Unresolved Feedback Loops Alert */}
      {insights?.unresolved_loops && insights.unresolved_loops.length > 0 && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Unresolved Feedback Loop Detected
          </Typography>
          {insights.unresolved_loops[0].message}
          <br />
          <Typography variant="caption">
            {insights.unresolved_loops[0].recommendation}
          </Typography>
        </Alert>
      )}
      
      {/* Praise Momentum Indicator */}
      {insights?.praise_momentum && (
        <Box sx={{ mb: 2 }}>
          <Chip
            label={`Praise Momentum: ${insights.praise_momentum.trend.toUpperCase()} (${insights.praise_momentum.change > 0 ? '+' : ''}${insights.praise_momentum.change.toFixed(1)}%)`}
            color={insights.praise_momentum.trend === 'increasing' ? 'success' : 'default'}
            sx={{ mr: 1 }}
          />
          {insights.praise_momentum.trainer_recognition_trend === 'increasing' && (
            <Chip label="Trainer Recognition ↑" color="success" size="small" sx={{ mr: 1 }} />
          )}
          {insights.praise_momentum.mentor_recognition_trend === 'increasing' && (
            <Chip label="Mentor Recognition ↑" color="success" size="small" />
          )}
        </Box>
      )}

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Key Metrics */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Overall Sentiment
              </Typography>
              <Typography variant="h4">
                {trends?.current_week.positive.toFixed(1) || '0.0'}%
              </Typography>
              <Typography
                variant="body2"
                color={trends && trends.overall_change > 0 ? 'success.main' : trends && trends.overall_change < 0 ? 'error.main' : 'text.secondary'}
              >
                {trends && trends.overall_change !== undefined && trends.overall_change !== null
                  ? `${trends.overall_change > 0 ? '+' : ''}${trends.overall_change.toFixed(1)}% from last week`
                  : 'No previous week data'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Feedback Volume
              </Typography>
              <Typography variant="h4">{trends?.current_volume || 0}</Typography>
              <Typography variant="body2" color="text.secondary">
                {trends && trends.volume_change !== undefined && trends.volume_change !== null
                  ? `${trends.volume_change > 0 ? '+' : ''}${trends.volume_change} from last week`
                  : 'No previous week data'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Positive Sentiment
              </Typography>
              <Typography variant="h4">
                {trends?.current_week.positive.toFixed(1) || '0.0'}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Negative Sentiment
              </Typography>
              <Typography variant="h4" color="error.main">
                {trends?.current_week.negative.toFixed(1) || '0.0'}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Sentiment Comparison Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Sentiment Comparison
            </Typography>
            {sentimentData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={sentimentData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="current" fill="#1976d2" name="Current Week" />
                  <Bar dataKey="previous" fill="#9e9e9e" name="Previous Week" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">No data available for this week</Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Sentiment Distribution */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Sentiment Distribution
            </Typography>
            {pieData.length > 0 && pieData.some(d => d.value > 0) ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">No data available</Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* 8-Week Trend Chart */}
        {eightWeekTrends && eightWeekTrends.trends && eightWeekTrends.trends.length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                8-Week Sentiment Trend
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={eightWeekTrends.trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week_label" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="positive" stroke="#32D74B" name="Positive %" />
                  <Line type="monotone" dataKey="neutral" stroke="#FF9F0A" name="Neutral %" />
                  <Line type="monotone" dataKey="negative" stroke="#FF453A" name="Negative %" />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}

        {/* Category Heatmap */}
        {categoryHeatmap && categoryHeatmap.heatmap && categoryHeatmap.heatmap.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Category Sentiment Heatmap
              </Typography>
              <Box sx={{ mt: 2 }}>
                {categoryHeatmap.heatmap.map((item: any, index: number) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Typography variant="body2">{item.category}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        Heat: {item.heat_score.toFixed(0)}/100
                      </Typography>
                    </Box>
                    <Box
                      sx={{
                        height: 20,
                        borderRadius: 1,
                        background: `linear-gradient(to right, 
                          #FF453A 0%, 
                          #FF453A ${item.negative}%, 
                          #FF9F0A ${item.negative}%, 
                          #FF9F0A ${item.negative + item.neutral}%, 
                          #32D74B ${item.negative + item.neutral}%, 
                          #32D74B 100%)`,
                      }}
                    />
                    <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
                      P: {item.positive.toFixed(1)}% | N: {item.neutral.toFixed(1)}% | Neg: {item.negative.toFixed(1)}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Paper>
          </Grid>
        )}

        {/* Appreciation Tracker */}
        {insights?.appreciation_tracker && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Appreciation Tracker
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Total Positive Feedback: {insights.appreciation_tracker.total_positive_feedback}
              </Typography>
              
              {insights.appreciation_tracker.trainer_recognition.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    Trainer Recognition ({insights.appreciation_tracker.trainer_recognition.length})
                  </Typography>
                  {insights.appreciation_tracker.trainer_recognition.slice(0, 3).map((item: any, index: number) => (
                    <Card key={index} sx={{ mb: 1, bgcolor: 'rgba(50, 215, 75, 0.15)', backdropFilter: 'blur(10px)', border: '1px solid rgba(50, 215, 75, 0.2)' }}>
                      <CardContent sx={{ py: 1 }}>
                        <Typography variant="caption" sx={{ fontStyle: 'italic' }}>
                          "{item.text}"
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5 }}>
                          {item.location} - {item.batch}
                        </Typography>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              )}
              
              {insights.appreciation_tracker.mentor_recognition.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    Mentor Recognition ({insights.appreciation_tracker.mentor_recognition.length})
                  </Typography>
                  {insights.appreciation_tracker.mentor_recognition.slice(0, 3).map((item: any, index: number) => (
                    <Card key={index} sx={{ mb: 1, bgcolor: 'rgba(10, 132, 255, 0.15)', backdropFilter: 'blur(10px)', border: '1px solid rgba(10, 132, 255, 0.2)' }}>
                      <CardContent sx={{ py: 1 }}>
                        <Typography variant="caption" sx={{ fontStyle: 'italic' }}>
                          "{item.text}"
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5 }}>
                          {item.location} - {item.batch}
                        </Typography>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              )}
            </Paper>
          </Grid>
        )}

        {/* Action Items */}
        {insights && insights.action_items.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Action Items
              </Typography>
              <Box sx={{ mt: 2 }}>
                {insights.action_items.slice(0, 5).map((item, index) => (
                  <Card key={index} sx={{ mb: 1 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="subtitle2" color="primary">
                          {item.priority.toUpperCase()} - {item.category || 'General'}
                        </Typography>
                        {item.assigned_to && (
                          <Chip label={item.assigned_to} size="small" color="secondary" />
                        )}
                      </Box>
                      <Typography variant="body2">{item.title}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {item.description}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            </Paper>
          </Grid>
        )}

        {/* Executive Summary */}
        {insights && insights.executive_summary && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Executive Summary
              </Typography>
              <Typography variant="body2" sx={{ whiteSpace: 'pre-line', mt: 2 }}>
                {insights.executive_summary}
              </Typography>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Container>
  )
}

export default Dashboard

