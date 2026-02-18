import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  Store,
  TrendingUp,
  Assignment,
  Warning,
  CheckCircle,
  HourglassEmpty,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import api from '../services/api';
import { API_ENDPOINTS } from '../config';

interface DashboardStats {
  total_stores: number;
  completion_rate: number;
  active_tasks: number;
  overdue_tasks: number;
  stores_by_status: Record<string, number>;
  risk_summary: {
    high: number;
    medium: number;
    low: number;
  };
}

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];
const RISK_COLORS = { high: '#f44336', medium: '#ff9800', low: '#4caf50' };

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.ANALYTICS.DASHBOARD);
      setStats(response.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const statusData = stats?.stores_by_status
    ? Object.entries(stats.stores_by_status).map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1).replace('_', ' '),
        value,
      }))
    : [];

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
    subtitle?: string;
    progress?: number;
  }> = ({ title, value, icon, color, subtitle, progress }) => (
    <Card
      elevation={0}
      sx={{
        height: '100%',
        borderRadius: 3,
        border: '1px solid',
        borderColor: 'divider',
        transition: 'all 0.3s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 24px rgba(0,0,0,0.1)',
        },
      }}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box flex={1}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h3" fontWeight="bold" sx={{ mb: 1 }}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
            {progress !== undefined && (
              <LinearProgress
                variant="determinate"
                value={progress}
                sx={{
                  mt: 2,
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: `${color}20`,
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: color,
                    borderRadius: 4,
                  },
                }}
              />
            )}
          </Box>
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: `${color}20`,
              color: color,
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Box mb={4}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Welcome Back! 👋
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's what's happening with your store openings today
        </Typography>
      </Box>

      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Stores"
            value={stats?.total_stores || 0}
            icon={<Store fontSize="large" />}
            color="#667eea"
            subtitle="Active projects"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Completion Rate"
            value={`${stats?.completion_rate?.toFixed(1) || 0}%`}
            icon={<TrendingUp fontSize="large" />}
            color="#4caf50"
            subtitle="Overall progress"
            progress={stats?.completion_rate || 0}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Tasks"
            value={stats?.active_tasks || 0}
            icon={<Assignment fontSize="large" />}
            color="#2196f3"
            subtitle="In progress"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Overdue Tasks"
            value={stats?.overdue_tasks || 0}
            icon={<Warning fontSize="large" />}
            color="#f44336"
            subtitle="Needs attention"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={8}>
          <Card
            elevation={0}
            sx={{
              borderRadius: 3,
              border: '1px solid',
              borderColor: 'divider',
              height: '100%',
            }}
          >
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Stores by Status
              </Typography>
              <Typography variant="body2" color="text.secondary" mb={3}>
                Distribution of store opening stages
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={statusData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#667eea" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            elevation={0}
            sx={{
              borderRadius: 3,
              border: '1px solid',
              borderColor: 'divider',
              height: '100%',
            }}
          >
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Risk Assessment
              </Typography>
              <Typography variant="body2" color="text.secondary" mb={3}>
                Current risk levels
              </Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Box
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: 'rgba(244, 67, 54, 0.1)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1}>
                    <Warning sx={{ color: '#f44336' }} />
                    <Typography fontWeight="600">High Risk</Typography>
                  </Box>
                  <Chip
                    label={stats?.risk_summary?.high || 0}
                    sx={{
                      backgroundColor: '#f44336',
                      color: 'white',
                      fontWeight: 'bold',
                    }}
                  />
                </Box>
                <Box
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: 'rgba(255, 152, 0, 0.1)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1}>
                    <HourglassEmpty sx={{ color: '#ff9800' }} />
                    <Typography fontWeight="600">Medium Risk</Typography>
                  </Box>
                  <Chip
                    label={stats?.risk_summary?.medium || 0}
                    sx={{
                      backgroundColor: '#ff9800',
                      color: 'white',
                      fontWeight: 'bold',
                    }}
                  />
                </Box>
                <Box
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1}>
                    <CheckCircle sx={{ color: '#4caf50' }} />
                    <Typography fontWeight="600">Low Risk</Typography>
                  </Box>
                  <Chip
                    label={stats?.risk_summary?.low || 0}
                    sx={{
                      backgroundColor: '#4caf50',
                      color: 'white',
                      fontWeight: 'bold',
                    }}
                  />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card
        elevation={0}
        sx={{
          borderRadius: 3,
          border: '1px solid',
          borderColor: 'divider',
        }}
      >
        <CardContent>
          <Typography variant="h6" fontWeight="bold" gutterBottom>
            Quick Actions
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Get started with these common tasks
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  border: '2px dashed',
                  borderColor: 'divider',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    backgroundColor: 'rgba(102, 126, 234, 0.05)',
                  },
                }}
              >
                <Store sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="body2" fontWeight="600">
                  Add New Store
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  border: '2px dashed',
                  borderColor: 'divider',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    backgroundColor: 'rgba(102, 126, 234, 0.05)',
                  },
                }}
              >
                <Assignment sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="body2" fontWeight="600">
                  Create Task
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  border: '2px dashed',
                  borderColor: 'divider',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    backgroundColor: 'rgba(102, 126, 234, 0.05)',
                  },
                }}
              >
                <TrendingUp sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="body2" fontWeight="600">
                  View Analytics
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  border: '2px dashed',
                  borderColor: 'divider',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    backgroundColor: 'rgba(102, 126, 234, 0.05)',
                  },
                }}
              >
                <Warning sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="body2" fontWeight="600">
                  Check Risks
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
