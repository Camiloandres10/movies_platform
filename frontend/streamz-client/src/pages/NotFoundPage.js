import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

const NotFoundContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  text-align: center;
  color: white;
`;

const HomeButton = styled(Button)`
  background-color: #e50914;
  margin-top: 24px;
  
  &:hover {
    background-color: #f40612;
  }
`;

const NotFoundPage = () => {
  return (
    <Box sx={{ backgroundColor: '#111', minHeight: '100vh' }}>
      <NotFoundContainer>
        <Typography variant="h1" gutterBottom>404</Typography>
        <Typography variant="h4" gutterBottom>Página no encontrada</Typography>
        <Typography variant="body1">
          La página que estás buscando no existe o ha sido movida.
        </Typography>
        
        <HomeButton 
          variant="contained" 
          component={Link} 
          to="/"
        >
          Volver al inicio
        </HomeButton>
      </NotFoundContainer>
    </Box>
  );
};

export default NotFoundPage;