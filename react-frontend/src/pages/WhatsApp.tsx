import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { Construction } from '@mui/icons-material';

const WhatsApp: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        WhatsApp Integration
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={4}>
        Manage WhatsApp groups and communications
      </Typography>
      <Card
        elevation={0}
        sx={{
          borderRadius: 3,
          border: '1px solid',
          borderColor: 'divider',
          textAlign: 'center',
          py: 8,
        }}
      >
        <CardContent>
          <Construction sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" fontWeight="bold" gutterBottom>
            WhatsApp Integration Coming Soon
          </Typography>
          <Typography variant="body2" color="text.secondary">
            This feature is under development
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WhatsApp;
