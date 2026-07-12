import axios from 'axios';
import { API_START } from './api_start';

const API_BASE = API_START;

export const driversAPI = {
    getAllDrivers: async () => {
        const response = await axios.get(`${API_BASE}/api/drivers`);
        return response.data;
    },
    getDriverDetail: async (driverId) => {
        const response = await axios.get(`${API_BASE}/api/drivers/${driverId}`);
        return response.data;
    }
};