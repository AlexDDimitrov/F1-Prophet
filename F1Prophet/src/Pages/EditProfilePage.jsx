import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './EditProfilePage.css';

function EditProfilePage() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    
    const [editForm, setEditForm] = useState({
        username: '',
        email: '',
        current_password: '',
        new_password: '',
        confirm_password: ''
    });

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        const token = localStorage.getItem('token');

        if (!token) {
            navigate('/login');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/users/profile', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch profile');
            }

            const data = await response.json();
            setEditForm({
                username: data.username,
                email: data.email,
                current_password: '',
                new_password: '',
                confirm_password: ''
            });
            setLoading(false);
        } catch (err) {
            console.error('Error fetching profile:', err);
            setError(err.message);
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        setEditForm({
            ...editForm,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        if (editForm.new_password && editForm.new_password !== editForm.confirm_password) {
            setError('New passwords do not match');
            return;
        }

        const token = localStorage.getItem('token');
        const updateData = {
            username: editForm.username,
            email: editForm.email
        };

        if (editForm.new_password) {
            updateData.current_password = editForm.current_password;
            updateData.new_password = editForm.new_password;
        }

        try {
            const response = await fetch('http://localhost:5000/api/users/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(updateData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to update profile');
            }

            setSuccess('Profile updated successfully!');
            
            setTimeout(() => {
                navigate('/profile');
            }, 1500);

        } catch (err) {
            console.error('Error updating profile:', err);
            setError(err.message);
        }
    };

    const handleCancel = () => {
        navigate('/profile');
    };

    if (loading) {
        return (
            <div className='edit-profile-page'>
                <div className='loading'>Loading...</div>
            </div>
        );
    }

    return (
        <div className='edit-profile-page'>
            <button onClick={() => navigate('/profile')} className='edit-back-button'>
                Back to Profile
            </button>

            <div className='edit-container'>
                <header className='edit-header'>
                    <h1 className='edit-title'>Edit Profile</h1>
                </header>

                <form onSubmit={handleSubmit} className='edit-form'>
                    <div className='form-section'>
                        <h2 className='section-title'>Account Information</h2>
                        
                        <div className='form-group'>
                            <label htmlFor='username'>Username</label>
                            <input
                                type='text'
                                id='username'
                                name='username'
                                value={editForm.username}
                                onChange={handleInputChange}
                                className='form-input'
                                required
                            />
                        </div>

                        <div className='form-group'>
                            <label htmlFor='email'>Email</label>
                            <input
                                type='email'
                                id='email'
                                name='email'
                                value={editForm.email}
                                onChange={handleInputChange}
                                className='form-input'
                                required
                            />
                        </div>
                    </div>

                    <div className='form-divider'></div>

                    <div className='form-section'>
                        <h2 className='section-title'>Change Password</h2>
                        <p className='section-subtitle'>Leave blank to keep current password</p>

                        <div className='form-group'>
                            <label htmlFor='current_password'>Current Password</label>
                            <input
                                type='password'
                                id='current_password'
                                name='current_password'
                                value={editForm.current_password}
                                onChange={handleInputChange}
                                className='form-input'
                                placeholder='Required if changing password'
                            />
                        </div>

                        <div className='form-group'>
                            <label htmlFor='new_password'>New Password</label>
                            <input
                                type='password'
                                id='new_password'
                                name='new_password'
                                value={editForm.new_password}
                                onChange={handleInputChange}
                                className='form-input'
                                placeholder='At least 6 characters'
                            />
                        </div>

                        <div className='form-group'>
                            <label htmlFor='confirm_password'>Confirm New Password</label>
                            <input
                                type='password'
                                id='confirm_password'
                                name='confirm_password'
                                value={editForm.confirm_password}
                                onChange={handleInputChange}
                                className='form-input'
                                placeholder='Confirm new password'
                            />
                        </div>
                    </div>

                    {error && <div className='form-error'>{error}</div>}
                    {success && <div className='form-success'>{success}</div>}

                    <div className='form-actions'>
                        <button type='button' onClick={handleCancel} className='btn-cancel'>
                            Cancel
                        </button>
                        <button type='submit' className='btn-save'>
                            Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default EditProfilePage;