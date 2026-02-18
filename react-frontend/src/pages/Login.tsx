import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Container,
  Alert,
  CircularProgress,
  Tab,
  Tabs,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { Visibility, VisibilityOff, Store as StoreIcon } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const [tab, setTab] = useState(0);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (tab === 0) {
        await login(username, password);
      } else {
        await register(username, password, name, role);
      }
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background pattern */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.1,
          backgroundImage:
            'radial-gradient(circle at 25px 25px, white 2%, transparent 0%), radial-gradient(circle at 75px 75px, white 2%, transparent 0%)',
          backgroundSize: '100px 100px',
        }}
      />
      <Container maxWidth="sm" sx={{ position: 'relative', zIndex: 1 }}>
        <Card
          elevation={10}
          sx={{
            borderRadius: 4,
            overflow: 'hidden',
          }}
        >
          <Box
            sx={{
              p: 4,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              textAlign: 'center',
            }}
          >
            <StoreIcon sx={{ fontSize: 60, mb: 2 }} />
            <Typography variant="h4" fontWeight="bold" gutterBottom>
              Store Opening AI
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9 }}>
              Intelligent Store Management System
            </Typography>
          </Box>
          <CardContent sx={{ p: 4 }}>
            <Tabs
              value={tab}
              onChange={(_, newValue) => setTab(newValue)}
              variant="fullWidth"
              sx={{ mb: 3 }}
            >
              <Tab label="Sign In" />
              <Tab label="Sign Up" />
            </Tabs>
            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Username"
                variant="outlined"
                margin="normal"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={loading}
              />
              {tab === 1 && (
                <>
                  <TextField
                    fullWidth
                    label="Full Name"
                    variant="outlined"
                    margin="normal"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    disabled={loading}
                  />
                  <TextField
                    fullWidth
                    label="Role"
                    variant="outlined"
                    margin="normal"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    placeholder="e.g., Manager, Developer"
                    required
                    disabled={loading}
                  />
                </>
              )}
              <TextField
                fullWidth
                label="Password"
                type={showPassword ? 'text' : 'password'}
                variant="outlined"
                margin="normal"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
              <Button
                fullWidth
                type="submit"
                variant="contained"
                size="large"
                disabled={loading}
                sx={{
                  mt: 3,
                  py: 1.5,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  fontWeight: 600,
                  textTransform: 'none',
                  fontSize: '1.1rem',
                }}
              >
                {loading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : tab === 0 ? (
                  'Sign In'
                ) : (
                  'Create Account'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
        <Typography
          variant="body2"
          align="center"
          sx={{ mt: 3, color: 'white', opacity: 0.9 }}
        >
          © 2026 Store Opening AI. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};

export default Login;
