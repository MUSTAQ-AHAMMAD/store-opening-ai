import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Chip,
  Alert,
  CircularProgress,
  MenuItem,
  InputAdornment,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Search,
  CheckCircle,
  Schedule,
  Warning,
  Assignment,
  Person,
} from '@mui/icons-material';
import api from '../services/api';
import { API_ENDPOINTS } from '../config';
import { format } from 'date-fns';

interface Task {
  id: number;
  title: string;
  description?: string;
  status: string;
  priority: string;
  due_date?: string;
  checklist_id: number;
  assigned_to_id?: number;
  assigned_to?: {
    name: string;
    role: string;
  };
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

interface Checklist {
  id: number;
  name: string;
  store_id: number;
  store?: {
    name: string;
  };
}

interface TeamMember {
  id: number;
  name: string;
  role: string;
}

const priorityColors: Record<string, string> = {
  low: '#4caf50',
  medium: '#ff9800',
  high: '#f44336',
};

const statusColors: Record<string, string> = {
  pending: '#9e9e9e',
  in_progress: '#2196f3',
  completed: '#4caf50',
  blocked: '#f44336',
};

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [checklists, setChecklists] = useState<Checklist[]>([]);
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    due_date: '',
    checklist_id: '',
    assigned_to_id: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    filterTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tasks, searchQuery, statusFilter, priorityFilter]);

  const fetchData = async () => {
    try {
      const [checklistsRes, teamRes] = await Promise.all([
        api.get(API_ENDPOINTS.CHECKLISTS.LIST),
        api.get(API_ENDPOINTS.TEAM.LIST),
      ]);
      
      setChecklists(checklistsRes.data);
      setTeamMembers(teamRes.data);

      // Fetch all tasks from all checklists
      const allTasks: Task[] = [];
      for (const checklist of checklistsRes.data) {
        try {
          const tasksRes = await api.get(API_ENDPOINTS.CHECKLISTS.TASKS(checklist.id));
          allTasks.push(...tasksRes.data);
        } catch (err) {
          console.error(`Failed to fetch tasks for checklist ${checklist.id}`, err);
        }
      }
      setTasks(allTasks);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const filterTasks = () => {
    let filtered = tasks;

    if (searchQuery) {
      filtered = filtered.filter(
        (task) =>
          task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          task.description?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter((task) => task.status === statusFilter);
    }

    if (priorityFilter !== 'all') {
      filtered = filtered.filter((task) => task.priority === priorityFilter);
    }

    setFilteredTasks(filtered);
  };

  const handleOpenDialog = (task?: Task) => {
    if (task) {
      setEditingTask(task);
      setFormData({
        title: task.title,
        description: task.description || '',
        status: task.status,
        priority: task.priority,
        due_date: task.due_date ? task.due_date.split('T')[0] : '',
        checklist_id: task.checklist_id.toString(),
        assigned_to_id: task.assigned_to_id?.toString() || '',
      });
    } else {
      setEditingTask(null);
      setFormData({
        title: '',
        description: '',
        status: 'pending',
        priority: 'medium',
        due_date: '',
        checklist_id: checklists.length > 0 ? checklists[0].id.toString() : '',
        assigned_to_id: '',
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingTask(null);
  };

  const handleSubmit = async () => {
    try {
      const payload = {
        title: formData.title,
        description: formData.description || undefined,
        status: formData.status,
        priority: formData.priority,
        due_date: formData.due_date || undefined,
        assigned_to_id: formData.assigned_to_id ? parseInt(formData.assigned_to_id) : undefined,
      };

      if (editingTask) {
        await api.put(`/checklists/tasks/${editingTask.id}`, payload);
      } else {
        await api.post(API_ENDPOINTS.CHECKLISTS.TASKS(parseInt(formData.checklist_id)), payload);
      }
      handleCloseDialog();
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to save task');
    }
  };

  const handleDelete = async (taskId: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await api.delete(`/checklists/tasks/${taskId}`);
        fetchData();
      } catch (err: any) {
        setError(err.response?.data?.error || 'Failed to delete task');
      }
    }
  };

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      await api.put(`/checklists/tasks/${taskId}`, { status: newStatus });
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to update task status');
    }
  };

  const getChecklistInfo = (checklistId: number) => {
    const checklist = checklists.find((c) => c.id === checklistId);
    return checklist ? `${checklist.name} - ${checklist.store?.name || 'Unknown'}` : 'Unknown';
  };

  const isOverdue = (dueDate?: string) => {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date() && true;
  };

  const getStats = () => {
    const total = tasks.length;
    const completed = tasks.filter((t) => t.status === 'completed').length;
    const inProgress = tasks.filter((t) => t.status === 'in_progress').length;
    const overdue = tasks.filter((t) => isOverdue(t.due_date) && t.status !== 'completed').length;
    
    return { total, completed, inProgress, overdue };
  };

  const stats = getStats();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Task Management
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Track and manage tasks across all stores
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
          disabled={checklists.length === 0}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            textTransform: 'none',
            fontWeight: 600,
            px: 3,
            py: 1.5,
          }}
        >
          Add Task
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Stats Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Tasks
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    {stats.total}
                  </Typography>
                </Box>
                <Assignment sx={{ fontSize: 40, color: '#667eea', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Completed
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="success.main">
                    {stats.completed}
                  </Typography>
                </Box>
                <CheckCircle sx={{ fontSize: 40, color: '#4caf50', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    In Progress
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="primary.main">
                    {stats.inProgress}
                  </Typography>
                </Box>
                <Schedule sx={{ fontSize: 40, color: '#2196f3', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Overdue
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="error.main">
                    {stats.overdue}
                  </Typography>
                </Box>
                <Warning sx={{ fontSize: 40, color: '#f44336', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      <Card
        elevation={0}
        sx={{
          mb: 3,
          borderRadius: 3,
          border: '1px solid',
          borderColor: 'divider',
        }}
      >
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Search />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                select
                label="Status"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <MenuItem value="all">All Statuses</MenuItem>
                <MenuItem value="pending">Pending</MenuItem>
                <MenuItem value="in_progress">In Progress</MenuItem>
                <MenuItem value="completed">Completed</MenuItem>
                <MenuItem value="blocked">Blocked</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                select
                label="Priority"
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
              >
                <MenuItem value="all">All Priorities</MenuItem>
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </TextField>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tasks Grid */}
      <Grid container spacing={3}>
        {filteredTasks.map((task) => (
          <Grid item xs={12} key={task.id}>
            <Card
              elevation={0}
              sx={{
                borderRadius: 3,
                border: '1px solid',
                borderColor: isOverdue(task.due_date) && task.status !== 'completed' ? 'error.main' : 'divider',
                transition: 'all 0.3s',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                },
              }}
            >
              <CardContent>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12} md={6}>
                    <Box display="flex" alignItems="start" gap={2}>
                      <Box flex={1}>
                        <Typography variant="h6" fontWeight="bold" gutterBottom>
                          {task.title}
                        </Typography>
                        {task.description && (
                          <Typography variant="body2" color="text.secondary" mb={1}>
                            {task.description}
                          </Typography>
                        )}
                        <Typography variant="caption" color="text.secondary">
                          {getChecklistInfo(task.checklist_id)}
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={4}>
                        <Box>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Priority
                          </Typography>
                          <Chip
                            label={task.priority.toUpperCase()}
                            size="small"
                            sx={{
                              backgroundColor: priorityColors[task.priority],
                              color: 'white',
                              fontWeight: 600,
                              fontSize: '0.7rem',
                            }}
                          />
                        </Box>
                      </Grid>
                      <Grid item xs={4}>
                        <Box>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Status
                          </Typography>
                          <Chip
                            label={task.status.replace('_', ' ').toUpperCase()}
                            size="small"
                            sx={{
                              backgroundColor: statusColors[task.status],
                              color: 'white',
                              fontWeight: 600,
                              fontSize: '0.7rem',
                            }}
                          />
                        </Box>
                      </Grid>
                      <Grid item xs={4}>
                        <Box>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Due Date
                          </Typography>
                          <Typography
                            variant="body2"
                            fontWeight="600"
                            color={isOverdue(task.due_date) && task.status !== 'completed' ? 'error.main' : 'text.primary'}
                          >
                            {task.due_date ? format(new Date(task.due_date), 'MMM dd, yyyy') : 'No date'}
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                    <Box display="flex" alignItems="center" justifyContent="space-between" mt={2}>
                      <Box display="flex" alignItems="center" gap={1}>
                        {task.assigned_to ? (
                          <>
                            <Person sx={{ fontSize: 16, color: 'text.secondary' }} />
                            <Typography variant="body2" color="text.secondary">
                              {task.assigned_to.name}
                            </Typography>
                          </>
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            Unassigned
                          </Typography>
                        )}
                      </Box>
                      <Box display="flex" gap={1}>
                        <Tooltip title="Mark as In Progress">
                          <IconButton
                            size="small"
                            onClick={() => handleStatusChange(task.id, 'in_progress')}
                            disabled={task.status === 'in_progress' || task.status === 'completed'}
                            sx={{ backgroundColor: 'white', '&:hover': { backgroundColor: '#e3f2fd' } }}
                          >
                            <Schedule fontSize="small" color={task.status === 'in_progress' ? 'primary' : 'action'} />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Mark as Completed">
                          <IconButton
                            size="small"
                            onClick={() => handleStatusChange(task.id, 'completed')}
                            disabled={task.status === 'completed'}
                            sx={{ backgroundColor: 'white', '&:hover': { backgroundColor: '#e8f5e9' } }}
                          >
                            <CheckCircle fontSize="small" color={task.status === 'completed' ? 'success' : 'action'} />
                          </IconButton>
                        </Tooltip>
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(task)}
                          sx={{ backgroundColor: 'white', '&:hover': { backgroundColor: '#f5f5f5' } }}
                        >
                          <Edit fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDelete(task.id)}
                          sx={{ backgroundColor: 'white', color: 'error.main', '&:hover': { backgroundColor: '#ffebee' } }}
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </Box>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {filteredTasks.length === 0 && (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" py={8}>
          <Assignment sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No tasks found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {checklists.length === 0
              ? 'Please create a checklist first to add tasks'
              : searchQuery || statusFilter !== 'all' || priorityFilter !== 'all'
              ? 'Try adjusting your filters'
              : 'Get started by adding your first task'}
          </Typography>
        </Box>
      )}

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Typography variant="h6" fontWeight="bold">
            {editingTask ? 'Edit Task' : 'Add New Task'}
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            <TextField
              fullWidth
              label="Task Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
            />
            <TextField
              fullWidth
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              multiline
              rows={3}
            />
            {!editingTask && (
              <TextField
                fullWidth
                select
                label="Checklist"
                value={formData.checklist_id}
                onChange={(e) => setFormData({ ...formData, checklist_id: e.target.value })}
                required
              >
                {checklists.map((checklist) => (
                  <MenuItem key={checklist.id} value={checklist.id.toString()}>
                    {checklist.name} - {checklist.store?.name || 'Unknown Store'}
                  </MenuItem>
                ))}
              </TextField>
            )}
            <TextField
              fullWidth
              select
              label="Assigned To"
              value={formData.assigned_to_id}
              onChange={(e) => setFormData({ ...formData, assigned_to_id: e.target.value })}
            >
              <MenuItem value="">Unassigned</MenuItem>
              {teamMembers.map((member) => (
                <MenuItem key={member.id} value={member.id.toString()}>
                  {member.name} - {member.role}
                </MenuItem>
              ))}
            </TextField>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Priority"
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  required
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Status"
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  required
                >
                  <MenuItem value="pending">Pending</MenuItem>
                  <MenuItem value="in_progress">In Progress</MenuItem>
                  <MenuItem value="completed">Completed</MenuItem>
                  <MenuItem value="blocked">Blocked</MenuItem>
                </TextField>
              </Grid>
            </Grid>
            <TextField
              fullWidth
              label="Due Date"
              type="date"
              value={formData.due_date}
              onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={handleCloseDialog} sx={{ textTransform: 'none' }}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!formData.title || (!editingTask && !formData.checklist_id)}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            {editingTask ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Tasks;
