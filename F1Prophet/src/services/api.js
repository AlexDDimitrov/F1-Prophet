import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const driversAPI = {
    getAllDrivers: async () => {
        const response = await axios.get(`${API_BASE}/drivers`);
        return response.data;
    },
    getDriverDetail: async (driverId) => {
        const response = await axios.get(`${API_BASE}/drivers/${driverId}`);
        return response.data;
    }
};