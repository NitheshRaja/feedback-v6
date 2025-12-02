import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  CircularProgress,
  Box,
  Alert,
  TextField,
} from '@mui/material'
import { format, startOfWeek, addDays } from 'date-fns'
import { reportService, pdfService } from '../services/feedback'
import { WeeklyReport } from '../types'

const Reports = () => {
  const navigate = useNavigate()
  const [reports, setReports] = useState<WeeklyReport[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [exporting, setExporting] = useState<number | null>(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [weekStart, setWeekStart] = useState(
    format(startOfWeek(new Date(), { weekStartsOn: 1 }), 'yyyy-MM-dd')
  )

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      const data = await reportService.listWeeklyReports(0, 20)
      setReports(data)
    } catch (error) {
      console.error('Error loading reports:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateReport = async () => {
    if (!weekStart) {
      setError('Please select a week start date')
      return
    }

    setGenerating(true)
    setError('')
    setSuccess('')

    try {
      // Convert to ISO string with time
      const weekStartDate = new Date(weekStart + 'T00:00:00')
      const weekStartISO = weekStartDate.toISOString()
      
      const newReport = await reportService.generateWeeklyReport(weekStartISO)
      setSuccess('Report generated successfully!')
      // Reload reports
      await loadReports()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate report')
    } finally {
      setGenerating(false)
    }
  }

  const handleExportPDF = async (reportId: number) => {
    setExporting(reportId)
    try {
      const blob = await pdfService.exportPDF(reportId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report_${reportId}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to export PDF')
    } finally {
      setExporting(null)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ pb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Weekly Reports
      </Typography>

      {/* Generate Report Section */}
      <Paper sx={{ p: 3, mt: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Generate New Report
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mt: 2 }}>
          <TextField
            label="Week Start Date"
            type="date"
            value={weekStart}
            onChange={(e) => setWeekStart(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
            sx={{ minWidth: 200 }}
          />
          <Button
            variant="contained"
            onClick={handleGenerateReport}
            disabled={generating}
          >
            {generating ? 'Generating...' : 'Generate Report'}
          </Button>
        </Box>
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mt: 2 }}>
            {success}
          </Alert>
        )}
      </Paper>

      {/* Reports Table */}
      {reports.length === 0 ? (
        <Paper sx={{ p: 4, mt: 2, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No Reports Found
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Upload feedback data first, then generate a weekly report using the form above.
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper} sx={{ mt: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Week</TableCell>
                <TableCell>Sentiment Score</TableCell>
                <TableCell>Change</TableCell>
                <TableCell>Heat Index</TableCell>
                <TableCell>Feedback Count</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {reports.map((report) => (
                <TableRow key={report.id}>
                  <TableCell>
                    {format(new Date(report.week_start_date), 'MMM dd')} -{' '}
                    {format(new Date(report.week_end_date), 'MMM dd, yyyy')}
                  </TableCell>
                  <TableCell>{report.overall_sentiment_score.toFixed(1)}%</TableCell>
                  <TableCell>
                    {report.sentiment_change !== null && report.sentiment_change !== undefined ? (
                      <Typography
                        variant="body2"
                        color={report.sentiment_change > 0 ? 'success.main' : 'error.main'}
                      >
                        {report.sentiment_change > 0 ? '+' : ''}
                        {report.sentiment_change.toFixed(1)}%
                      </Typography>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        N/A
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell>{report.heat_index.toFixed(1)}</TableCell>
                  <TableCell>{report.total_feedback_count}</TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => navigate(`/reports/${report.id}`)}
                      >
                        View Details
                      </Button>
                      <Button
                        size="small"
                        variant="contained"
                        color="secondary"
                        onClick={() => handleExportPDF(report.id)}
                        disabled={exporting === report.id}
                      >
                        {exporting === report.id ? 'Exporting...' : 'Export PDF'}
                      </Button>
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Container>
  )
}

export default Reports

