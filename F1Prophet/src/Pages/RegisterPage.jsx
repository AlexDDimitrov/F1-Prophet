import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css';

function RegisterPage() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
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

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match!');
            return;
        }

        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters long!');
            return;
        }

        e.preventDefault();
        setError('');

        try {
            const res = await fetch('http://localhost:5000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: formData.username,
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
            localStorage.setItem('token', data.token);
            navigate('/');

        } catch (err) {
            setError('Cannot connect to server. Is the backend running?');
            console.error(err);
        }
    };

    return (
        <div className='auth-page'>
            <button onClick={() => navigate('/')} className='back-button'>
                ← Back to Home
            </button>

            <div className='auth-container'>
                <div className='auth-card'>
                    <h1 className='auth-title'>Join F1 Prophet</h1>
                    <p className='auth-subtitle'>Start your racing predictions!</p>

                    {error && <div className='error-message'>{error}</div>}

                    <form onSubmit={handleSubmit} className='auth-form'>
                        <div className='form-group'>
                            <label htmlFor='username'>Username</label>
                            <input
                                type='text'
                                id='username'
                                name='username'
                                value={formData.username}
                                onChange={handleChange}
                                required
                                placeholder='Choose a username'
                                minLength='3'
                            />
                        </div>

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
                                placeholder='Create a password'
                                minLength='6'
                            />
                        </div>

                        <div className='form-group'>
                            <label htmlFor='confirmPassword'>Confirm Password</label>
                            <input
                                type='password'
                                id='confirmPassword'
                                name='confirmPassword'
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                required
                                placeholder='Confirm your password'
                                minLength='6'
                            />
                        </div>

                        <button type='submit' className='auth-submit-btn'>
                            Register
                        </button>
                    </form>

                    <div className='auth-footer'>
                        <p>Already have an account? <Link to='/login'>Login here</Link></p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RegisterPage;