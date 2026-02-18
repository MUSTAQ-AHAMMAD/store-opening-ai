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
  Avatar,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Search,
  Phone,
  Email,
  Person,
  Work,
} from '@mui/icons-material';
import api from '../services/api';
import { API_ENDPOINTS } from '../config';

interface TeamMember {
  id: number;
  name: string;
  role: string;
  phone: string;
  email?: string;
  store_id: number;
  is_active: boolean;
  total_tasks?: number;
  completed_tasks?: number;
  pending_tasks?: number;
}

interface Store {
  id: number;
  name: string;
  location: string;
}

const roleColors: Record<string, string> = {
  'Store Manager': '#667eea',
  'Assistant Manager': '#764ba2',
  'Team Lead': '#f093fb',
  'Staff': '#4facfe',
  'Contractor': '#43e97b',
};

const Team: React.FC = () => {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [filteredMembers, setFilteredMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [storeFilter, setStoreFilter] = useState('all');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingMember, setEditingMember] = useState<TeamMember | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    phone: '',
    email: '',
    store_id: '',
    is_active: true,
  });

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    filterMembers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [teamMembers, searchQuery, storeFilter]);

  const fetchData = async () => {
    try {
      const [membersRes, storesRes] = await Promise.all([
        api.get(API_ENDPOINTS.TEAM.LIST),
        api.get(API_ENDPOINTS.STORES.LIST),
      ]);
      setTeamMembers(membersRes.data);
      setStores(storesRes.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const filterMembers = () => {
    let filtered = teamMembers;

    if (searchQuery) {
      filtered = filtered.filter(
        (member) =>
          member.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          member.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
          member.phone.includes(searchQuery)
      );
    }

    if (storeFilter !== 'all') {
      filtered = filtered.filter((member) => member.store_id === parseInt(storeFilter));
    }

    setFilteredMembers(filtered);
  };

  const handleOpenDialog = (member?: TeamMember) => {
    if (member) {
      setEditingMember(member);
      setFormData({
        name: member.name,
        role: member.role,
        phone: member.phone,
        email: member.email || '',
        store_id: member.store_id.toString(),
        is_active: member.is_active,
      });
    } else {
      setEditingMember(null);
      setFormData({
        name: '',
        role: '',
        phone: '',
        email: '',
        store_id: stores.length > 0 ? stores[0].id.toString() : '',
        is_active: true,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingMember(null);
  };

  const handleSubmit = async () => {
    try {
      const payload = {
        ...formData,
        store_id: parseInt(formData.store_id),
      };
      
      if (editingMember) {
        await api.put(`${API_ENDPOINTS.TEAM.LIST}/${editingMember.id}`, payload);
      } else {
        await api.post(API_ENDPOINTS.TEAM.CREATE, payload);
      }
      handleCloseDialog();
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to save team member');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this team member?')) {
      try {
        await api.delete(API_ENDPOINTS.TEAM.DELETE(id));
        fetchData();
      } catch (err: any) {
        setError(err.response?.data?.error || 'Failed to delete team member');
      }
    }
  };

  const getStoreName = (storeId: number) => {
    const store = stores.find((s) => s.id === storeId);
    return store ? store.name : 'Unknown Store';
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
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
            Team Management
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage your team members and assignments
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
          Add Team Member
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
                placeholder="Search by name, role, or phone..."
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
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                select
                label="Store Filter"
                value={storeFilter}
                onChange={(e) => setStoreFilter(e.target.value)}
              >
                <MenuItem value="all">All Stores</MenuItem>
                {stores.map((store) => (
                  <MenuItem key={store.id} value={store.id.toString()}>
                    {store.name}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={2}>
              <Typography variant="body2" color="text.secondary">
                {filteredMembers.length} members
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {filteredMembers.map((member) => (
          <Grid item xs={12} md={6} lg={4} key={member.id}>
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
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <Avatar
                    sx={{
                      width: 56,
                      height: 56,
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      fontSize: '1.2rem',
                      fontWeight: 'bold',
                    }}
                  >
                    {getInitials(member.name)}
                  </Avatar>
                  <Box flex={1}>
                    <Typography variant="h6" fontWeight="bold">
                      {member.name}
                    </Typography>
                    <Chip
                      label={member.role}
                      size="small"
                      sx={{
                        backgroundColor: roleColors[member.role] || '#999',
                        color: 'white',
                        fontWeight: 600,
                        fontSize: '0.7rem',
                        height: 20,
                      }}
                    />
                  </Box>
                </Box>

                <Box display="flex" flexDirection="column" gap={1} mb={2}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Work sx={{ fontSize: 16, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {getStoreName(member.store_id)}
                    </Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Phone sx={{ fontSize: 16, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">
                      {member.phone}
                    </Typography>
                  </Box>
                  {member.email && (
                    <Box display="flex" alignItems="center" gap={1}>
                      <Email sx={{ fontSize: 16, color: 'text.secondary' }} />
                      <Typography variant="body2" color="text.secondary" sx={{ wordBreak: 'break-all' }}>
                        {member.email}
                      </Typography>
                    </Box>
                  )}
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
                  <Box>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Tasks: {member.total_tasks || 0}
                    </Typography>
                    <Typography variant="caption" color="success.main" fontWeight="600">
                      ✓ {member.completed_tasks || 0} completed
                    </Typography>
                  </Box>
                  <Box display="flex" gap={1}>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(member)}
                      sx={{
                        backgroundColor: 'white',
                        '&:hover': { backgroundColor: '#f5f5f5' },
                      }}
                    >
                      <Edit fontSize="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(member.id)}
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

      {filteredMembers.length === 0 && (
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          py={8}
        >
          <Person sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No team members found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {searchQuery || storeFilter !== 'all'
              ? 'Try adjusting your filters'
              : 'Get started by adding your first team member'}
          </Typography>
        </Box>
      )}

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Typography variant="h6" fontWeight="bold">
            {editingMember ? 'Edit Team Member' : 'Add New Team Member'}
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            <TextField
              fullWidth
              label="Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
            <TextField
              fullWidth
              select
              label="Role"
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              required
            >
              <MenuItem value="Store Manager">Store Manager</MenuItem>
              <MenuItem value="Assistant Manager">Assistant Manager</MenuItem>
              <MenuItem value="Team Lead">Team Lead</MenuItem>
              <MenuItem value="Staff">Staff</MenuItem>
              <MenuItem value="Contractor">Contractor</MenuItem>
            </TextField>
            <TextField
              fullWidth
              label="Phone"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              required
              placeholder="+1234567890"
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
            <TextField
              fullWidth
              select
              label="Store"
              value={formData.store_id}
              onChange={(e) => setFormData({ ...formData, store_id: e.target.value })}
              required
            >
              {stores.map((store) => (
                <MenuItem key={store.id} value={store.id.toString()}>
                  {store.name} - {store.location}
                </MenuItem>
              ))}
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={handleCloseDialog} sx={{ textTransform: 'none' }}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!formData.name || !formData.role || !formData.phone || !formData.store_id}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            {editingMember ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Team;
