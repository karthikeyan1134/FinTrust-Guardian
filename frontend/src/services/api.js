import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust the base URL as needed

// Function to authorize a partner's data request
export const authorizeDataRequest = async (partnerId, userId, purpose) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/authorize`, {
            partner_id: partnerId,
            user_id: userId,
            purpose: purpose
        });
        return response.data;
    } catch (error) {
        console.error('Error authorizing data request:', error);
        throw error;
    }
};

// Function to retrieve audit logs
export const getAuditLogs = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/logs`);
        return response.data;
    } catch (error) {
        console.error('Error fetching audit logs:', error);
        throw error;
    }
};

// Function to get current data sharing policies
export const getPolicies = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/policies`);
        return response.data;
    } catch (error) {
        console.error('Error fetching policies:', error);
        throw error;
    }
};