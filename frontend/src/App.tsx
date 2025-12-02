import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { AuthProvider } from './contexts/AuthContext'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Reports from './pages/Reports'
import ReportDetails from './pages/ReportDetails'
import Upload from './pages/Upload'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'

// Apple-like Dark Glassmorphism Theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#0A84FF', // iOS Blue
    },
    secondary: {
      main: '#BF5AF2', // iOS Purple
    },
    background: {
      default: 'transparent', // Allow body gradient to show
      paper: 'rgba(30, 30, 30, 0.6)', // Glassy background
    },
    text: {
      primary: '#FFFFFF',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
    success: {
      main: '#32D74B', // iOS Green
    },
    error: {
      main: '#FF453A', // iOS Red
    },
    warning: {
      main: '#FFD60A', // iOS Yellow
    },
    info: {
      main: '#64D2FF', // iOS Cyan
    },
  },
  shape: {
    borderRadius: 16, // Rounded corners like iOS
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h4: {
      fontWeight: 700,
      letterSpacing: '-0.02em',
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarColor: "#6b6b6b #2b2b2b",
          "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
            backgroundColor: "transparent",
            width: 8,
          },
          "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
            borderRadius: 8,
            backgroundColor: "#6b6b6b",
            minHeight: 24,
          },
          "&::-webkit-scrollbar-thumb:focus, & *::-webkit-scrollbar-thumb:focus": {
            backgroundColor: "#959595",
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(28, 28, 30, 0.65)', // iOS System Gray 6 (Dark) roughly
          backdropFilter: 'blur(20px) saturate(180%)',
          WebkitBackdropFilter: 'blur(20px) saturate(180%)',
          border: '1px solid rgba(255, 255, 255, 0.125)',
          boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
          transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
          '&:hover': {
            // Subtle lift effect for interactive papers if needed, generally handled by Cards
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(44, 44, 46, 0.6)', // Slightly lighter than paper
          backdropFilter: 'blur(20px)',
          borderRadius: 20,
          border: '1px solid rgba(255, 255, 255, 0.1)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 12px 40px rgba(0, 0, 0, 0.5)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          boxShadow: 'none',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: 'rgba(0, 0, 0, 0.6)',
          backdropFilter: 'blur(20px)',
          borderRight: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 50, // Pill shape
          textTransform: 'none',
          fontWeight: 600,
          padding: '8px 24px',
          backdropFilter: 'blur(4px)',
          transition: 'all 0.2s ease-in-out',
          '&:active': {
             transform: 'scale(0.96)',
          },
        },
        contained: {
          boxShadow: '0 4px 14px 0 rgba(0,0,0,0.39)',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        },
        head: {
          fontWeight: 700,
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
          color: '#A1A1AA', // Muted text for headers
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: 'rgba(0, 0, 0, 0.2)',
            borderRadius: 12,
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.1)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.3)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#0A84FF',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }
      }
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          backdropFilter: 'blur(10px)',
          backgroundColor: 'rgba(20, 20, 20, 0.6)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          '&.MuiAlert-standardSuccess': {
            backgroundColor: 'rgba(50, 215, 75, 0.15)',
            color: '#66ff85',
          },
          '&.MuiAlert-standardError': {
            backgroundColor: 'rgba(255, 69, 58, 0.15)',
            color: '#ff8080',
          },
          '&.MuiAlert-standardWarning': {
            backgroundColor: 'rgba(255, 214, 10, 0.15)',
            color: '#ffd60a',
          },
          '&.MuiAlert-standardInfo': {
            backgroundColor: 'rgba(10, 132, 255, 0.15)',
            color: '#64d2ff',
          },
        },
      },
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Dashboard />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/reports"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Reports />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/reports/:id"
              element={
                <ProtectedRoute>
                  <Layout>
                    <ReportDetails />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/upload"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Upload />
                  </Layout>
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App
