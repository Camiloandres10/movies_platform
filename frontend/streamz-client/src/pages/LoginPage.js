import React, { useState, useContext } from 'react';
import { Container, Box, Typography, TextField, Button, Paper, Alert } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import styled from 'styled-components';

const LoginContainer = styled(Container)`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
`;

const LoginForm = styled(Paper)`
  padding: 32px;
  max-width: 400px;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
`;

const StyledTextField = styled(TextField)`
  margin-bottom: 16px;
  
  .MuiInputBase-root {
    color: white;
  }
  
  .MuiOutlinedInput-root {
    fieldset {
      border-color: #333;
    }
    
    &:hover fieldset {
      border-color: white;
    }
  }
  
  .MuiInputLabel-root {
    color: #aaa;
  }
`;

const LoginButton = styled(Button)`
  background-color: #e50914;
  margin-top: 16px;
  
  &:hover {
    background-color: #f40612;
  }
`;

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!username || !password) {
      setError('Por favor, complete todos los campos');
      return;
    }
    
    setError('');
    const result = await login(username, password);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error?.non_field_errors?.[0] || 'Credenciales inválidas');
    }
  };

  return (
    <LoginContainer>
      <LoginForm elevation={3}>
        <Typography variant="h4" gutterBottom color="white">
          Iniciar Sesión
        </Typography>
        
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <form onSubmit={handleSubmit}>
          <StyledTextField
            label="Nombre de usuario"
            variant="outlined"
            fullWidth
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          
          <StyledTextField
            label="Contraseña"
            variant="outlined"
            fullWidth
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          
          <LoginButton
            type="submit"
            variant="contained"
            fullWidth
            size="large"
          >
            Iniciar Sesión
          </LoginButton>
        </form>
        
        <Box mt={2} display="flex" justifyContent="center">
          <Typography variant="body2" color="textSecondary">
            ¿No tienes una cuenta?{' '}
            <Link to="/register" style={{ color: '#e50914', textDecoration: 'none' }}>
              Regístrate
            </Link>
          </Typography>
        </Box>
      </LoginForm>
    </LoginContainer>
  );
};

export default LoginPage;