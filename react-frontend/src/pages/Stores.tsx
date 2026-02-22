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
  LinearProgress,
  Alert,
  CircularProgress,
  MenuItem,
  InputAdornment,
  Divider,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Search,
  LocationOn,
  CalendarToday,
  TrendingUp,
  PersonAdd,
  Remove,
} from '@mui/icons-material';
import api from '../services/api';
import { API_ENDPOINTS } from '../config';
import { format } from 'date-fns';

interface Store {
  id: number;
  name: string;
  location: string;
  opening_date: string;
  status: string;
  workflow_stage: number;
  completion_percentage?: number;
  total_tasks?: number;
  completed_tasks?: number;
}

interface TeamMemberInput {
  name: string;
  role: string;
  phone: string;
  email: string;
}

const statusColors: Record<string, string> = {
  planning: '#2196f3',
  in_progress: '#ff9800',
  completed: '#4caf50',
  delayed: '#f44336',
};

const Stores: React.FC = () => {
  const [stores, setStores] = useState<Store[]>([]);
  const [filteredStores, setFilteredStores] = useState<Store[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingStore, setEditingStore] = useState<Store | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    opening_date: '',
    status: 'planning',
  });
  const [teamMembers, setTeamMembers] = useState<TeamMemberInput[]>([]);

  useEffect(() => {
    fetchStores();
  }, []);

  useEffect(() => {
    filterStores();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stores, searchQuery, statusFilter]);

  const fetchStores = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.STORES.LIST);
      setStores(response.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch stores');
    } finally {
      setLoading(false);
    }
  };

  const filterStores = () => {
    let filtered = stores;

    if (searchQuery) {
      filtered = filtered.filter(
        (store) =>
          store.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          store.location.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter((store) => store.status === statusFilter);
    }

    setFilteredStores(filtered);
  };

  const handleOpenDialog = (store?: Store) => {
    if (store) {
      setEditingStore(store);
      setFormData({
        name: store.name,
        location: store.location,
        opening_date: store.opening_date.split('T')[0],
        status: store.status,
      });
    } else {
      setEditingStore(null);
      setFormData({
        name: '',
        location: '',
        opening_date: '',
        status: 'planning',
      });
      setTeamMembers([]);
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingStore(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingStore) {
        await api.put(API_ENDPOINTS.STORES.UPDATE(editingStore.id), formData);
      } else {
        const payload: any = { ...formData };
        const validMembers = teamMembers.filter((m) => m.name.trim() && m.phone.trim());
        if (validMembers.length > 0) {
          payload.team_members = validMembers;
        }
        await api.post(API_ENDPOINTS.STORES.CREATE, payload);
      }
      handleCloseDialog();
      fetchStores();
    } catch (err: any) {
      setError(err.response?.data?.message || err.response?.data?.error || 'Failed to save store');
    }
  };

  const addTeamMember = () => {
    setTeamMembers([...teamMembers, { name: '', role: 'team_member', phone: '', email: '' }]);
  };

  const removeTeamMember = (index: number) => {
    setTeamMembers(teamMembers.filter((_, i) => i !== index));
  };

  const updateTeamMember = (index: number, field: keyof TeamMemberInput, value: string) => {
    const updated = teamMembers.map((m, i) => (i === index ? { ...m, [field]: value } : m));
    setTeamMembers(updated);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this store?')) {
      try {
        await api.delete(API_ENDPOINTS.STORES.DELETE(id));
        fetchStores();
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to delete store');
      }
    }
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
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Store Management
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage your store opening projects
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            textTransform: 'none',
            fontWeight: 600,
            px: 3,
            py: 1.5,
          }}
        >
          Add Store
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

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
                placeholder="Search by name or location..."
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
                label="Status Filter"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <MenuItem value="all">All Statuses</MenuItem>
                <MenuItem value="planning">Planning</MenuItem>
                <MenuItem value="in_progress">In Progress</MenuItem>
                <MenuItem value="completed">Completed</MenuItem>
                <MenuItem value="delayed">Delayed</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2" color="text.secondary">
                Showing {filteredStores.length} of {stores.length} stores
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {filteredStores.map((store) => (
          <Grid item xs={12} md={6} lg={4} key={store.id}>
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
                <Box display="flex" justifyContent="space-between" alignItems="start" mb={2}>
                  <Typography variant="h6" fontWeight="bold">
                    {store.name}
                  </Typography>
                  <Chip
                    label={store.status.replace('_', ' ').toUpperCase()}
                    size="small"
                    sx={{
                      backgroundColor: statusColors[store.status] || '#999',
                      color: 'white',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                    }}
                  />
                </Box>

                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <LocationOn sx={{ fontSize: 18, color: 'text.secondary' }} />
                  <Typography variant="body2" color="text.secondary">
                    {store.location}
                  </Typography>
                </Box>

                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <CalendarToday sx={{ fontSize: 18, color: 'text.secondary' }} />
                  <Typography variant="body2" color="text.secondary">
                    {format(new Date(store.opening_date), 'MMM dd, yyyy')}
                  </Typography>
                </Box>

                <Box mb={2}>
                  <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2" fontWeight="600">
                      Progress
                    </Typography>
                    <Typography variant="body2" fontWeight="600" color="primary">
                      {store.completion_percentage?.toFixed(0) || 0}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={store.completion_percentage || 0}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: 'rgba(102, 126, 234, 0.1)',
                      '& .MuiLinearProgress-bar': {
                        borderRadius: 4,
                        background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                      },
                    }}
                  />
                </Box>

                <Box
                  display="flex"
                  alignItems="center"
                  justifyContent="space-between"
                  sx={{
                    p: 1.5,
                    borderRadius: 2,
                    backgroundColor: 'rgba(102, 126, 234, 0.05)',
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1}>
                    <TrendingUp sx={{ fontSize: 18, color: 'primary.main' }} />
                    <Typography variant="body2" fontWeight="600">
                      {store.completed_tasks || 0} / {store.total_tasks || 0} Tasks
                    </Typography>
                  </Box>
                  <Box display="flex" gap={1}>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(store)}
                      sx={{
                        backgroundColor: 'white',
                        '&:hover': { backgroundColor: '#f5f5f5' },
                      }}
                    >
                      <Edit fontSize="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(store.id)}
                      sx={{
                        backgroundColor: 'white',
                        color: 'error.main',
                        '&:hover': { backgroundColor: '#ffebee' },
                      }}
                    >
                      <Delete fontSize="small" />
                    </IconButton>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {filteredStores.length === 0 && (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          py={8}
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No stores found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {searchQuery || statusFilter !== 'all'
              ? 'Try adjusting your filters'
              : 'Get started by adding your first store'}
          </Typography>
        </Box>
      )}

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Typography variant="h6" fontWeight="bold">
            {editingStore ? 'Edit Store' : 'Add New Store'}
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            <TextField
              fullWidth
              label="Store Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
            <TextField
              fullWidth
              label="Location"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              required
            />
            <TextField
              fullWidth
              label="Opening Date"
              type="date"
              value={formData.opening_date}
              onChange={(e) => setFormData({ ...formData, opening_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              required
            />
            <TextField
              fullWidth
              select
              label="Status"
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            >
              <MenuItem value="planning">Planning</MenuItem>
              <MenuItem value="in_progress">In Progress</MenuItem>
              <MenuItem value="completed">Completed</MenuItem>
              <MenuItem value="delayed">Delayed</MenuItem>
            </TextField>

            {!editingStore && (
              <>
                <Divider />
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="subtitle1" fontWeight="600">
                    Responsible Team Members (optional)
                  </Typography>
                  <Button
                    size="small"
                    startIcon={<PersonAdd />}
                    onClick={addTeamMember}
                    sx={{ textTransform: 'none' }}
                  >
                    Add Member
                  </Button>
                </Box>
                {teamMembers.length > 0 && (
                  <Alert severity="info" sx={{ py: 0.5 }}>
                    The first member will be set as the primary responsible person for all workflow stages.
                  </Alert>
                )}
                {teamMembers.map((member, index) => (
                  <Box
                    key={index}
                    sx={{ p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}
                  >
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="body2" fontWeight="600">
                        Member {index + 1}
                      </Typography>
                      <IconButton size="small" onClick={() => removeTeamMember(index)}>
                        <Remove fontSize="small" />
                      </IconButton>
                    </Box>
                    <Grid container spacing={1}>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          size="small"
                          label="Name"
                          value={member.name}
                          onChange={(e) => updateTeamMember(index, 'name', e.target.value)}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          size="small"
                          label="Role"
                          value={member.role}
                          onChange={(e) => updateTeamMember(index, 'role', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          size="small"
                          label="Phone (E.164, e.g. +1234567890)"
                          value={member.phone}
                          onChange={(e) => updateTeamMember(index, 'phone', e.target.value)}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          size="small"
                          label="Email (optional)"
                          value={member.email}
                          onChange={(e) => updateTeamMember(index, 'email', e.target.value)}
                        />
                      </Grid>
                    </Grid>
                  </Box>
                ))}
              </>
            )}
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={handleCloseDialog} sx={{ textTransform: 'none' }}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleSubmit}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            {editingStore ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Stores;
