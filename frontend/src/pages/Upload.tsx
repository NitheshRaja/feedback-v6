import { useState } from 'react'
import {
  Container,
  Typography,
  Paper,
  Button,
  Box,
  Alert,
  LinearProgress,
} from '@mui/material'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import { feedbackService } from '../services/feedback'

const Upload = () => {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setResult(null)
      setError('')
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    setUploading(true)
    setError('')
    setResult(null)

    try {
      const response = await feedbackService.uploadFile(file)
      setResult(response)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <Container maxWidth="md" sx={{ pb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Upload Feedback Data
      </Typography>

      <Paper sx={{ p: 4, mt: 3 }}>
        <Box sx={{ mb: 3 }}>
          <input
            accept=".csv,.xlsx,.xls"
            style={{ display: 'none' }}
            id="file-upload"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="file-upload">
            <Button
              variant="outlined"
              component="span"
              startIcon={<UploadFileIcon />}
              sx={{ mr: 2 }}
            >
              Select File
            </Button>
          </label>
          {file && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              Selected: {file.name}
            </Typography>
          )}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {uploading && <LinearProgress sx={{ mb: 2 }} />}

        <Button
          variant="contained"
          onClick={handleUpload}
          disabled={!file || uploading}
          fullWidth
        >
          {uploading ? 'Uploading...' : 'Upload and Process'}
        </Button>

        {result && (
          <Box sx={{ mt: 3 }}>
            <Alert severity="success">
              File processed successfully!
            </Alert>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2">
                Total Rows: {result.total_rows}
              </Typography>
              <Typography variant="body2">
                Processed Rows: {result.processed_rows}
              </Typography>
              <Typography variant="body2">
                Saved Count: {result.saved_count}
              </Typography>
              {result.errors && result.errors.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" color="error">
                    Errors:
                  </Typography>
                  {result.errors.map((err: string, index: number) => (
                    <Typography key={index} variant="caption" display="block">
                      {err}
                    </Typography>
                  ))}
                </Box>
              )}
            </Box>
          </Box>
        )}

        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            File Format Requirements
          </Typography>
          <Typography variant="body2" component="div">
            <ul>
              <li>File format: CSV or Excel (.xlsx, .xls)</li>
              <li>Required columns: trainee_id, location, training_batch, rating_score, open_text</li>
              <li>Optional columns: category_tags, week_start_date, week_end_date</li>
            </ul>
          </Typography>
        </Box>
      </Paper>
    </Container>
  )
}

export default Upload

