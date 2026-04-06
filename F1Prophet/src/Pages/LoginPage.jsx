import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css';

function LoginPage() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const res = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password
                })
            });

            const data = await res.json();

            if (!res.ok) {
                setError(data.error);
                return;
            }

            localStorage.setItem('user', JSON.stringify(data.user));
            navigate('/');

        } catch (err) {
            setError(`Cannot connect to server.`);
            console.log(err);
        }
    };

    return (
        <div className='auth-page'>
            <button onClick={() => navigate('/')} className='back-button'>
                ← Back to Home
            </button>

            <div className='auth-container'>
                <div className='auth-card'>
                    <h1 className='auth-title'>Login to F1 Prophet</h1>
                    <p className='auth-subtitle'>Welcome back, champion!</p>

                    {error && <div className='error-message'>{error}</div>}

                    <form onSubmit={handleSubmit} className='auth-form'>
                        <div className='form-group'>
                            <label htmlFor='email'>Email</label>
                            <input
                                type='email'
                                id='email'
                                name='email'
                                value={formData.email}
                                onChange={handleChange}
                                required
                                placeholder='your.email@example.com'
                            />
                        </div>

                        <div className='form-group'>
                            <label htmlFor='password'>Password</label>
                            <input
                                type='password'
                                id='password'
                                name='password'
                                value={formData.password}
                                onChange={handleChange}
                                required
                                placeholder='Enter your password'
                            />
                        </div>

                        <button type='submit' className='auth-submit-btn'>
                            Login
                        </button>
                    </form>

                    <div className='auth-footer'>
                        <p>Don't have an account? <Link to='/register'>Register here</Link></p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;