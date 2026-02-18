import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  MenuItem,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
} from '@mui/material';
import {
  Lightbulb,
  TrendingUp,
  Warning,
  CheckCircle,
  Psychology,
  Send,
  SmartToy,
  Timeline,
  Assessment,
  Insights,
} from '@mui/icons-material';
import api from '../services/api';
import { API_ENDPOINTS } from '../config';

interface AIInsight {
  store_id: number;
  store_name: string;
  risk_level: string;
  risk_factors: string[];
  recommendations: string[];
  metrics: {
    completion_rate: number;
    overdue_tasks: number;
    days_until_opening: number | null;
  };
}

interface Store {
  id: number;
  name: string;
  location: string;
}

interface Task {
  id: number;
  title: string;
  description?: string;
  priority: string;
  status: string;
  assigned_to?: {
    name: string;
    phone: string;
  };
}

interface PredictionData {
  store_id: number;
  store_name: string;
  opening_date: string | null;
  predicted_completion: string | null;
  on_track: boolean;
  days_difference: number | null;
  metrics: {
    remaining_tasks: number;
    average_tasks_per_day: number;
    tasks_completed_last_14_days: number;
  };
}

const riskColors: Record<string, string> = {
  low: '#4caf50',
  medium: '#ff9800',
  high: '#f44336',
};

const AIInsights: React.FC = () => {
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [predictions, setPredictions] = useState<Record<number, PredictionData>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedStore, setSelectedStore] = useState<number | null>(null);
  const [prioritizedTasks, setPrioritizedTasks] = useState<any[]>([]);
  const [messageDialogOpen, setMessageDialogOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [generatedMessage, setGeneratedMessage] = useState('');
  const [generatingMessage, setGeneratingMessage] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [insightsRes, storesRes] = await Promise.all([
        api.get(API_ENDPOINTS.AI.INSIGHTS),
        api.get(API_ENDPOINTS.STORES.LIST),
      ]);
      
      setInsights(insightsRes.data.insights || []);
      setStores(storesRes.data);

      // Fetch predictions for each store
      const predictionsData: Record<number, PredictionData> = {};
      for (const store of storesRes.data) {
        try {
          const predRes = await api.get(API_ENDPOINTS.AI.PREDICT_COMPLETION(store.id));
          predictionsData[store.id] = predRes.data;
        } catch (err) {
          console.error(`Failed to fetch predictions for store ${store.id}`, err);
        }
      }
      setPredictions(predictionsData);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch AI insights');
    } finally {
      setLoading(false);
    }
  };

  const handleStoreSelect = async (storeId: number) => {
    setSelectedStore(storeId);
    try {
      const response = await api.get(API_ENDPOINTS.AI.TASK_PRIORITIZATION(storeId));
      setPrioritizedTasks(response.data.tasks || []);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch task prioritization');
    }
  };

  const handleGenerateFollowUp = async (task: any) => {
    if (!task.assigned_to) {
      setError('Task has no assignee. Cannot generate follow-up message.');
      return;
    }

    setSelectedTask(task);
    setGeneratingMessage(true);
    setMessageDialogOpen(true);

    try {
      const response = await api.post(`/ai/task/${task.id}/generate-followup`);
      setGeneratedMessage(response.data.message);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to generate follow-up message');
      setGeneratedMessage('Failed to generate message. Please try again.');
    } finally {
      setGeneratingMessage(false);
    }
  };

  const handleSendMessage = async () => {
    if (!selectedTask || !generatedMessage) return;

    try {
      await api.post('/whatsapp/send-follow-up', {
        phone: selectedTask.assigned_to?.phone,
        message: generatedMessage,
      });
      setError('');
      alert('Follow-up message sent successfully!');
      handleCloseMessageDialog();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send message');
    }
  };

  const handleCloseMessageDialog = () => {
    setMessageDialogOpen(false);
    setSelectedTask(null);
    setGeneratedMessage('');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Box>
      <Box mb={4}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          AI Insights & Communicator
        </Typography>
        <Typography variant="body1" color="text.secondary">
          AI-powered predictions, recommendations, and intelligent communication
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* AI Insights Overview */}
      <Typography variant="h6" fontWeight="bold" gutterBottom mb={2}>
        Store Risk Assessment
      </Typography>
      <Grid container spacing={3} mb={4}>
        {insights.map((insight) => (
          <Grid item xs={12} md={6} lg={4} key={insight.store_id}>
            <Card
              elevation={0}
              sx={{
                borderRadius: 3,
                border: '2px solid',
                borderColor: riskColors[insight.risk_level],
                transition: 'all 0.3s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: '0 12px 24px rgba(0,0,0,0.1)',
                },
              }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                  <Typography variant="h6" fontWeight="bold">
                    {insight.store_name}
                  </Typography>
                  <Chip
                    label={insight.risk_level.toUpperCase()}
                    sx={{
                      backgroundColor: riskColors[insight.risk_level],
                      color: 'white',
                      fontWeight: 600,
                    }}
                  />
                </Box>

                <Box display="flex" gap={2} mb={2}>
                  <Box flex={1}>
                    <Typography variant="caption" color="text.secondary">
                      Completion
                    </Typography>
                    <Typography variant="h6" fontWeight="bold" color="primary">
                      {insight.metrics.completion_rate}%
                    </Typography>
                  </Box>
                  <Box flex={1}>
                    <Typography variant="caption" color="text.secondary">
                      Overdue
                    </Typography>
                    <Typography variant="h6" fontWeight="bold" color="error">
                      {insight.metrics.overdue_tasks}
                    </Typography>
                  </Box>
                  <Box flex={1}>
                    <Typography variant="caption" color="text.secondary">
                      Days Left
                    </Typography>
                    <Typography variant="h6" fontWeight="bold">
                      {insight.metrics.days_until_opening || 'N/A'}
                    </Typography>
                  </Box>
                </Box>

                {insight.risk_factors.length > 0 && (
                  <Box mb={2}>
                    <Typography variant="caption" fontWeight="600" color="error.main" display="block" mb={1}>
                      Risk Factors:
                    </Typography>
                    {insight.risk_factors.map((factor, idx) => (
                      <Typography key={idx} variant="caption" color="text.secondary" display="block">
                        • {factor}
                      </Typography>
                    ))}
                  </Box>
                )}

                {insight.recommendations.length > 0 && (
                  <Box>
                    <Typography variant="caption" fontWeight="600" color="primary.main" display="block" mb={1}>
                      AI Recommendations:
                    </Typography>
                    {insight.recommendations.map((rec, idx) => (
                      <Typography key={idx} variant="caption" color="text.secondary" display="block">
                        • {rec}
                      </Typography>
                    ))}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {insights.length === 0 && (
        <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider', mb: 4 }}>
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Assessment sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              No active stores to analyze
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Create stores and add tasks to see AI insights
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Completion Predictions */}
      <Typography variant="h6" fontWeight="bold" gutterBottom mb={2} mt={4}>
        Completion Date Predictions
      </Typography>
      <Grid container spacing={3} mb={4}>
        {Object.values(predictions).map((pred) => (
          <Grid item xs={12} md={6} key={pred.store_id}>
            <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <Timeline sx={{ fontSize: 32, color: pred.on_track ? 'success.main' : 'error.main' }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {pred.store_name}
                    </Typography>
                    <Chip
                      label={pred.on_track ? 'On Track' : 'Behind Schedule'}
                      size="small"
                      color={pred.on_track ? 'success' : 'error'}
                      sx={{ fontWeight: 600 }}
                    />
                  </Box>
                </Box>

                <Grid container spacing={2} mb={2}>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Remaining Tasks
                    </Typography>
                    <Typography variant="body1" fontWeight="600">
                      {pred.metrics.remaining_tasks}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Daily Progress
                    </Typography>
                    <Typography variant="body1" fontWeight="600">
                      {pred.metrics.average_tasks_per_day} tasks/day
                    </Typography>
                  </Grid>
                </Grid>

                {pred.predicted_completion && (
                  <Alert
                    severity={pred.on_track ? 'success' : 'warning'}
                    sx={{ fontSize: '0.85rem' }}
                    icon={pred.on_track ? <CheckCircle /> : <Warning />}
                  >
                    Predicted completion: <strong>{new Date(pred.predicted_completion).toLocaleDateString()}</strong>
                    {pred.days_difference !== null && (
                      <Typography variant="caption" display="block">
                        {pred.on_track
                          ? `${pred.days_difference} days before opening`
                          : `${Math.abs(pred.days_difference)} days after opening`}
                      </Typography>
                    )}
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* AI Task Prioritization */}
      <Typography variant="h6" fontWeight="bold" gutterBottom mb={2} mt={4}>
        AI Task Prioritization & Communicator
      </Typography>
      <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider', mb: 3 }}>        <CardContent>
          <Box display="flex" alignItems="center" gap={2} mb={3}>
            <SmartToy sx={{ fontSize: 32, color: 'primary.main' }} />
            <Box flex={1}>
              <Typography variant="h6" fontWeight="bold">
                AI-Powered Communicator
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Generate intelligent follow-up messages for overdue tasks
              </Typography>
            </Box>
          </Box>

          <TextField
            fullWidth
            select
            label="Select Store"
            value={selectedStore || ''}
            onChange={(e) => handleStoreSelect(Number(e.target.value))}
            sx={{ mb: 3 }}
          >
            <MenuItem value="">Select a store</MenuItem>
            {stores.map((store) => (
              <MenuItem key={store.id} value={store.id}>
                {store.name} - {store.location}
              </MenuItem>
            ))}
          </TextField>

          {prioritizedTasks.length > 0 && (
            <Box>
              <Typography variant="subtitle2" fontWeight="600" mb={2}>
                AI-Prioritized Tasks (Top 10)
              </Typography>
              <List>
                {prioritizedTasks.map((task, idx) => (
                  <React.Fragment key={task.id}>
                    <ListItem
                      sx={{
                        borderRadius: 2,
                        mb: 1,
                        bgcolor: 'rgba(102, 126, 234, 0.03)',
                        '&:hover': { bgcolor: 'rgba(102, 126, 234, 0.08)' },
                      }}
                      secondaryAction={
                        task.assigned_to && (
                          <Button
                            size="small"
                            variant="contained"
                            startIcon={<Send />}
                            onClick={() => handleGenerateFollowUp(task)}
                            sx={{
                              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                              textTransform: 'none',
                            }}
                          >
                            AI Follow-Up
                          </Button>
                        )
                      }
                    >
                      <ListItemIcon>
                        <Chip
                          label={`#${idx + 1}`}
                          size="small"
                          sx={{
                            width: 32,
                            height: 32,
                            borderRadius: '50%',
                            fontWeight: 'bold',
                            bgcolor: 'primary.main',
                            color: 'white',
                          }}
                        />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center" gap={1}>
                            <Typography variant="body1" fontWeight="600">
                              {task.title}
                            </Typography>
                            <Chip
                              label={task.priority}
                              size="small"
                              color={
                                task.priority === 'high' ? 'error' : task.priority === 'medium' ? 'warning' : 'success'
                              }
                            />
                          </Box>
                        }
                        secondary={
                          <>
                            {task.description && (
                              <Typography variant="caption" display="block">
                                {task.description}
                              </Typography>
                            )}
                            {task.assigned_to && (
                              <Typography variant="caption" color="text.secondary">
                                Assigned to: {task.assigned_to.name}
                              </Typography>
                            )}
                          </>
                        }
                      />
                    </ListItem>
                  </React.Fragment>
                ))}
              </List>
            </Box>
          )}

          {selectedStore && prioritizedTasks.length === 0 && (
            <Alert severity="info">No pending tasks found for this store.</Alert>
          )}
        </CardContent>
      </Card>

      {/* AI Message Dialog */}
      <Dialog open={messageDialogOpen} onClose={handleCloseMessageDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={2}>
            <Psychology sx={{ fontSize: 32, color: 'primary.main' }} />
            <Box>
              <Typography variant="h6" fontWeight="bold">
                AI-Generated Follow-Up Message
              </Typography>
              {selectedTask && (
                <Typography variant="caption" color="text.secondary">
                  Task: {selectedTask?.title}
                </Typography>
              )}
            </Box>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            {generatingMessage ? (
              <Box display="flex" flexDirection="column" alignItems="center" py={4}>
                <CircularProgress size={40} sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary">
                  AI is generating your personalized message...
                </Typography>
              </Box>
            ) : (
              <>
                <Alert severity="info" icon={<Lightbulb />}>
                  This message was intelligently generated by AI based on task context, priority, and timeline.
                </Alert>
                <TextField
                  fullWidth
                  label="Message"
                  value={generatedMessage}
                  onChange={(e) => setGeneratedMessage(e.target.value)}
                  multiline
                  rows={6}
                  helperText="You can edit this message before sending"
                />
                {selectedTask?.assigned_to && (
                  <Typography variant="caption" color="text.secondary">
                    Will be sent to: {selectedTask?.assigned_to?.name} ({selectedTask?.assigned_to?.phone})
                  </Typography>
                )}
              </>
            )}
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={handleCloseMessageDialog} sx={{ textTransform: 'none' }}>
            Cancel
          </Button>
          <Button
            variant="contained"
            startIcon={<Send />}
            onClick={handleSendMessage}
            disabled={!generatedMessage || generatingMessage}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            Send via WhatsApp
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AIInsights;
