import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './team.css';

function Team({ team, favoriteTeam }) {
    const navigate = useNavigate();

    const [isFavorite, setIsFavorite] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const reverseTeamMap = {
        "Red Bull": "red_bull",
        "Mercedes": "mercedes",
        "Ferrari": "ferrari",
        "McLaren": "mclaren",
        "Aston Martin": "aston_martin",
        "Alpine": "alpine",
        "Williams": "williams",
        "RB": "rb",
        "Audi": "audi",
        "Haas": "haas"
    };

    useEffect(() => {
        if (!favoriteTeam) {
            setIsFavorite(false);
            return;
        }
        setIsFavorite(reverseTeamMap[favoriteTeam] === team.team_id);
    }, [favoriteTeam, team.team_id]);

    const handleToggleFavorite = async () => {
        const token = localStorage.getItem('token');
        if (!token) return navigate('/login');

        setLoading(true);
        setIsFavorite(prev => !prev);

        try {
            await fetch(`http://localhost:5000/api/users/profile/favorite-team/${team.team_id}`, {
                method: 'POST',
                headers: { Authorization: `Bearer ${token}` }
            });
        } catch (err) {
            console.error("Error toggling favorite:", err);
            setError(err.message);
            setIsFavorite(prev => !prev);
        } finally {
            setLoading(false);
        }
    };

    const teamImage = `/images/teams/${team.team_id}.png`;

    const getTeamGradient = (team_id) => {
        const teams = {
            "red_bull": ["#0600EF", "#DC052D"],
            "mercedes": ["#00D2BE", "#000000"],
            "ferrari": ["#DC0000", "#FFD700"],
            "mclaren": ["#FF8700", "#000000"],
            "aston_martin": ["#006F62", "#00FFB3"],
            "alpine": ["#0090FF", "#FF87BC"],
            "williams": ["#005AFF", "#FFFFFF"],
            "rb": ["#1A2A3A", "#2B4562"],
            "audi": ["#000000", "#E10600"],
            "haas": ["#FFFFFF", "#B6BABD"],
        };

        const colors = teams[team_id];

        if (!colors) {
            return 'linear-gradient(135deg, #333, #111)';
        }

        return `
            linear-gradient(
                135deg,
                ${colors[0]} 0%,
                ${colors[0]} 65%,
                ${colors[1]} 65%,
                ${colors[1]} 100%
            ),
            linear-gradient(
                90deg,
                rgba(255,255,255,0.15) 0%,
                rgba(255,255,255,0.15) 5%,
                transparent 5%
            ),
            linear-gradient(
                45deg,
                rgba(255,255,255,0.05) 25%,
                transparent 25%
            )
        `;
    };

    return (
        <div 
            className='team-card' 
            style={{ 
                background: getTeamGradient(team.team_id),
                border: isFavorite ? '3px solid gold' : '3px solid #333',
            }}
        >
            <div className='team-image-section'>
                <img 
                    src={teamImage} 
                    alt={team.name}
                    className='team-image'
                    onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                    }}
                />
                <div className='team-placeholder' style={{display: 'none'}}>
                    <span className='placeholder-name'>{team.name}</span>
                </div>
            </div>

            <div className='team-info-boxes'>
                <div className='info-box-team'>
                    <span className='info-label'>Name</span>
                    <span className='info-value'>{team.name}</span>
                </div>

                <div className='info-box-team'>
                    <span className='info-label'>Nationality</span>
                    <span className='info-value'>{team.nationality}</span>
                </div>

                <div className='info-box-team'>
                    <span className='info-label'>Position</span>
                    <span className='info-value'>
                        {team.position ? `P${team.position}` : 'N/A'}
                    </span>
                </div>

                <div className='info-box-team'>
                    <span className='info-label'>Points</span>
                    <span className='info-value'>{team.points}</span>
                </div>

                <div className='driver-actions'>
                    <button 
                        className='view-profile-btn'
                        onClick={handleToggleFavorite}
                        disabled={loading}
                        title={isFavorite ? 'Remove favorite' : 'Add favorite'}
                    >
                        {isFavorite ? 'Rem Favorite' : 'Add Favorite'}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Team;