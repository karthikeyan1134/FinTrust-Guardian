import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PolicyView = () => {
    const [policies, setPolicies] = useState([]);

    useEffect(() => {
        const fetchPolicies = async () => {
            try {
                const response = await axios.get('/api/policies');
                setPolicies(response.data);
            } catch (error) {
                console.error('Error fetching policies:', error);
            }
        };

        fetchPolicies();
    }, []);

    return (
        <div className="policy-view">
            <h2>Data Sharing Policies</h2>
            {policies.length > 0 ? (
                <ul>
                    {policies.map((policy, index) => (
                        <li key={index}>
                            <strong>Partner:</strong> {policy.partner_id} <br />
                            <strong>Purpose:</strong> {policy.purpose} <br />
                            <strong>Data Fields:</strong> {policy.data_fields.join(', ')} <br />
                            <strong>Consent Required:</strong> {policy.consent_required ? 'Yes' : 'No'}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No policies available.</p>
            )}
        </div>
    );
};

export default PolicyView;