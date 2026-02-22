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
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Add,
  Send,
  Group,
  Archive,
  Message,
  Store as StoreIcon,
  Check,
  WhatsApp as WhatsAppIcon,
} from '@mui/icons-material';
import api from '../services/api';
import { API_ENDPOINTS } from '../config';
import { format } from 'date-fns';

interface WhatsAppGroup {
  id: number;
  store_id: number;
  group_name: string;
  group_sid?: string;
  is_active: boolean;
  created_at: string;
  archived_at?: string;
  store?: {
    name: string;
    location: string;
  };
}

interface Store {
  id: number;
  name: string;
  location: string;
}

interface Message {
  id: number;
  sender: string;
  message: string;
  timestamp: string;
  message_type: string;
}

const WhatsApp: React.FC = () => {
  const [groups, setGroups] = useState<WhatsAppGroup[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [messageDialogOpen, setMessageDialogOpen] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState<WhatsAppGroup | null>(null);
  const [archivedMessages, setArchivedMessages] = useState<Message[]>([]);
  const [formData, setFormData] = useState({
    store_id: '',
    group_name: '',
  });
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [groupsRes, storesRes] = await Promise.all([
        api.get(API_ENDPOINTS.WHATSAPP.GROUPS),
        api.get(API_ENDPOINTS.STORES.LIST),
      ]);
      setGroups(groupsRes.data);
      setStores(storesRes.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenCreateDialog = () => {
    setFormData({
      store_id: stores.length > 0 ? stores[0].id.toString() : '',
      group_name: '',
    });
    setCreateDialogOpen(true);
  };

  const handleCloseCreateDialog = () => {
    setCreateDialogOpen(false);
  };

  const handleCreateGroup = async () => {
    try {
      const store = stores.find((s) => s.id === parseInt(formData.store_id));
      const payload = {
        store_id: parseInt(formData.store_id),
        group_name: formData.group_name || `${store?.name} - Opening Team`,
      };
      
      await api.post(API_ENDPOINTS.WHATSAPP.CREATE_GROUP, payload);
      setSuccess('Communication channel record created successfully!');
      handleCloseCreateDialog();
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create group');
    }
  };

  const handleOpenMessageDialog = (group: WhatsAppGroup) => {
    setSelectedGroup(group);
    setMessageText('');
    setMessageDialogOpen(true);
  };

  const handleCloseMessageDialog = () => {
    setMessageDialogOpen(false);
    setSelectedGroup(null);
  };

  const handleSendMessage = async () => {
    if (!selectedGroup || !messageText.trim()) return;

    try {
      await api.post(`/whatsapp/groups/${selectedGroup.id}/send`, {
        message: messageText,
      });
      setSuccess('Message sent successfully!');
      setMessageText('');
      handleCloseMessageDialog();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send message');
    }
  };

  const handleArchiveGroup = async (groupId: number) => {
    if (!window.confirm('Are you sure you want to archive this group? This will deactivate the group.')) {
      return;
    }

    try {
      await api.post(API_ENDPOINTS.WHATSAPP.ARCHIVE(groupId), {
        conversations: [], // In production, this would fetch actual conversations
      });
      setSuccess('Group archived successfully!');
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to archive group');
    }
  };

  const handleViewArchive = async (groupId: number) => {
    try {
      const response = await api.get(API_ENDPOINTS.WHATSAPP.ARCHIVE(groupId));
      setArchivedMessages(response.data.conversations || []);
      setSuccess('Archived conversations loaded successfully');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load archived conversations');
    }
  };

  const getAvailableStores = () => {
    const storesWithGroups = groups.filter((g) => g.is_active).map((g) => g.store_id);
    return stores.filter((s) => !storesWithGroups.includes(s.id));
  };

  const availableStores = getAvailableStores();

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
            WhatsApp Integration
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage WhatsApp groups and communications
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleOpenCreateDialog}
          disabled={availableStores.length === 0}
          sx={{
            background: 'linear-gradient(135deg, #25D366 0%, #128C7E 100%)',
            textTransform: 'none',
            fontWeight: 600,
            px: 3,
            py: 1.5,
          }}
        >
          Add Communication Record
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      {/* Stats */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={4}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Active Groups
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="success.main">
                    {groups.filter((g) => g.is_active).length}
                  </Typography>
                </Box>
                <Group sx={{ fontSize: 40, color: '#25D366', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Archived Groups
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    {groups.filter((g) => !g.is_active).length}
                  </Typography>
                </Box>
                <Archive sx={{ fontSize: 40, color: '#667eea', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid', borderColor: 'divider' }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Groups
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    {groups.length}
                  </Typography>
                </Box>
                <WhatsAppIcon sx={{ fontSize: 40, color: '#128C7E', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Groups List */}
      <Grid container spacing={3}>
        {groups.map((group) => (
          <Grid item xs={12} md={6} key={group.id}>
            <Card
              elevation={0}
              sx={{
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
                      bgcolor: group.is_active ? '#25D366' : '#9e9e9e',
                    }}
                  >
                    <WhatsAppIcon sx={{ fontSize: 32 }} />
                  </Avatar>
                  <Box flex={1}>
                    <Typography variant="h6" fontWeight="bold">
                      {group.group_name}
                    </Typography>
                    <Chip
                      label={group.is_active ? 'Active' : 'Archived'}
                      size="small"
                      sx={{
                        backgroundColor: group.is_active ? '#25D366' : '#9e9e9e',
                        color: 'white',
                        fontWeight: 600,
                        fontSize: '0.7rem',
                      }}
                    />
                  </Box>
                </Box>

                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <StoreIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                  <Typography variant="body2" color="text.secondary">
                    {group.store?.name} - {group.store?.location}
                  </Typography>
                </Box>

                <Typography variant="caption" color="text.secondary" display="block" mb={2}>
                  Created: {format(new Date(group.created_at), 'MMM dd, yyyy')}
                  {group.archived_at && ` • Archived: ${format(new Date(group.archived_at), 'MMM dd, yyyy')}`}
                </Typography>

                <Box display="flex" gap={1}>
                  {group.is_active ? (
                    <>
                      <Button
                        variant="contained"
                        size="small"
                        startIcon={<Send />}
                        onClick={() => handleOpenMessageDialog(group)}
                        sx={{
                          background: 'linear-gradient(135deg, #25D366 0%, #128C7E 100%)',
                          textTransform: 'none',
                          fontWeight: 600,
                          flex: 1,
                        }}
                      >
                        Send Message
                      </Button>
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<Archive />}
                        onClick={() => handleArchiveGroup(group.id)}
                        sx={{ textTransform: 'none' }}
                      >
                        Archive
                      </Button>
                    </>
                  ) : (
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Message />}
                      onClick={() => handleViewArchive(group.id)}
                      sx={{ textTransform: 'none', flex: 1 }}
                    >
                      View Archive
                    </Button>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {groups.length === 0 && (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" py={8}>
          <WhatsAppIcon sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No WhatsApp groups yet
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {stores.length === 0
              ? 'Please create a store first to set up a communication channel'
              : 'Get started by adding your first communication channel record'}
          </Typography>
        </Box>
      )}

      {/* Create Group Dialog */}
      <Dialog open={createDialogOpen} onClose={handleCloseCreateDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Typography variant="h6" fontWeight="bold">
            Add Communication Record
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            <Alert severity="info">
              This creates an internal communication channel record for the store team.
              Messages are sent individually to each team member via Twilio WhatsApp.
              Recipients must join the Twilio sandbox first by sending the sandbox keyword.
            </Alert>
            <TextField
              fullWidth
              select
              label="Store"
              value={formData.store_id}
              onChange={(e) => {
                const store = stores.find((s) => s.id === parseInt(e.target.value));
                setFormData({
                  store_id: e.target.value,
                  group_name: store ? `${store.name} - Opening Team` : '',
                });
              }}
              required
            >
              {availableStores.map((store) => (
                <MenuItem key={store.id} value={store.id.toString()}>
                  {store.name} - {store.location}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Group Name"
              value={formData.group_name}
              onChange={(e) => setFormData({ ...formData, group_name: e.target.value })}
              helperText="Leave empty to use default format: Store Name - Opening Team"
            />
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={handleCloseCreateDialog} sx={{ textTransform: 'none' }}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleCreateGroup}
            disabled={!formData.store_id}
            sx={{
              background: 'linear-gradient(135deg, #25D366 0%, #128C7E 100%)',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            Add Record
          </Button>
        </DialogActions>
      </Dialog>

      {/* Send Message Dialog */}
      <Dialog open={messageDialogOpen} onClose={handleCloseMessageDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Typography variant="h6" fontWeight="bold">
            Send Message to {selectedGroup?.group_name}
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={2}>
            <Alert severity="info">
              This message will be sent to all team members in the store's WhatsApp group via Twilio.
            </Alert>
            <TextField
              fullWidth
              label="Message"
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              multiline
              rows={4}
              placeholder="Type your message here..."
              required
            />
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
            disabled={!messageText.trim()}
            sx={{
              background: 'linear-gradient(135deg, #25D366 0%, #128C7E 100%)',
              textTransform: 'none',
              fontWeight: 600,
            }}
          >
            Send Message
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WhatsApp;
