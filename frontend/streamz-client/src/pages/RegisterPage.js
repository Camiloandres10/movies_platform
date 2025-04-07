import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../api/config';
import { Container, Box, Typography, TextField, Button, Paper, Alert, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import styled from 'styled-components';

const RegisterContainer = styled(Container)`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
`;

const RegisterForm = styled(Paper)`
  padding: 32px;
  max-width: 500px;
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

const RegisterButton = styled(Button)`
  background-color: #e50914;
  margin-top: 16px;
  
  &:hover {
    background-color: #f40612;
  }
`;

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    plan: ''
  });
  const [plans, setPlans] = useState([]);
  const [error, setError] = useState('');
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch subscription plans
    axios.get(API_ENDPOINTS.PLANS)
      .then(response => {
        // Verifica si la respuesta tiene estructura paginated o es un array directo
        const plansData = response.data.results || response.data;
        setPlans(Array.isArray(plansData) ? plansData : []);
      })
      .catch(error => {
        console.error('Error fetching plans:', error);
        setPlans([]);
      });
  }, []);

  // Asegúrate de que tienes esta definición después de tus estados
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.email || !formData.password || !formData.password2) {
      setError('Por favor, complete todos los campos obligatorios');
      return;
    }

    if (formData.password !== formData.password2) {
      setError('Las contraseñas no coinciden');
      return;
    }

    setError('');
    const result = await register(formData);

    if (result.success) {
      navigate('/');
    } else {
      const errorMsg = result.error?.username ||
        result.error?.email ||
        result.error?.password ||
        'Error en el registro';
      setError(Array.isArray(errorMsg) ? errorMsg[0] : errorMsg);
    }
  };

  return (
    <RegisterContainer>
      <RegisterForm elevation={3}>
        <Typography variant="h4" gutterBottom color="white">
          Regístrate
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <form onSubmit={handleSubmit}>
          <StyledTextField
            label="Nombre de usuario"
            variant="outlined"
            fullWidth
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />

          <StyledTextField
            label="Correo electrónico"
            variant="outlined"
            fullWidth
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <StyledTextField
            label="Nombre"
            variant="outlined"
            fullWidth
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />

          <StyledTextField
            label="Apellido"
            variant="outlined"
            fullWidth
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />

          <StyledTextField
            label="Contraseña"
            variant="outlined"
            fullWidth
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <StyledTextField
            label="Confirmar contraseña"
            variant="outlined"
            fullWidth
            type="password"
            name="password2"
            value={formData.password2}
            onChange={handleChange}
            required
          />

          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Plan de suscripción *</InputLabel>
            <Select
              value={formData.plan}
              name="plan"
              onChange={handleChange}
              required
            >
              {Array.isArray(plans) && plans.map((plan) => (
                <MenuItem key={plan.id} value={plan.id}>
                  {plan.name} - ${plan.price}/mes ({plan.video_quality})
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <RegisterButton
            type="submit"
            variant="contained"
            fullWidth
            size="large"
          >
            Registrarse
          </RegisterButton>
        </form>

        <Box mt={2} display="flex" justifyContent="center">
          <Typography variant="body2" color="textSecondary">
            ¿Ya tienes una cuenta?{' '}
            <Link to="/login" style={{ color: '#e50914', textDecoration: 'none' }}>
              Inicia sesión
            </Link>
          </Typography>
        </Box>
      </RegisterForm>
    </RegisterContainer>
  );
};

export default RegisterPage;