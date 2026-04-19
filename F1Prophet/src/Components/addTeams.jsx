import React, {useState, useEffect} from 'react';
import Team from './team';
import F1Loader from '../Components/F1Loader';
import './addTeams.css';

function CollectTeams() {
    const [teams, setTeams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTeams = async () => {
            try{
                const response = await fetch('http://localhost:5000/api/teams');

                if (!response.ok) {
                    throw new Error('Failed to fetch teams');
                }

                const data = await response.json();
                setTeams(data);
                setLoading(false);
            } catch (err) {
                console.error('Error fetching teams: ', err);
                setError(err.message);
                setLoading(false);
            }
        };

        fetchTeams();
    }, []);

    if (loading) {
        return (
            <div>                
                <div className='predict-page'>
                    <F1Loader message="Loading teams..." />
                </div>
            </div>
        );
    }

    if (error) {
        return <div className='error'>Error: {error}</div>;
    }

    return (
        <div className='teams-grid'>
            {teams.map((team) => (
                <Team key={team.team_id} team={team}/>
            ))}
        </div>
    );
}

export default CollectTeams;