import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await login(email, password);
            localStorage.setItem('accessToken', response.access);
            localStorage.setItem('userEmail', email); // Store user's email
            //alert('Login successful!');
            console.log('Login successful, redirecting to /notes');
            navigate('/notes');  // Redirect to notes page after successful login
            window.location.href = '/notes'; // Alternative redirect method
            console.log('After navigate');
        } catch (error) {
            console.error('Login failed:', error.response || error.message);
            alert('Login failed!');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                required
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
            />
            <button type="submit">Login</button>
            <button onClick={() => navigate('/notes')}>Go to Notes</button>

        </form>
    );
}

export default LoginPage;
