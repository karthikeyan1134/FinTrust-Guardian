import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AuditTable = () => {
    const [auditLogs, setAuditLogs] = useState([]);

    useEffect(() => {
        const fetchAuditLogs = async () => {
            try {
                const response = await axios.get('/logs');
                setAuditLogs(response.data);
            } catch (error) {
                console.error('Error fetching audit logs:', error);
            }
        };

        fetchAuditLogs();
    }, []);

    return (
        <div className="audit-table">
            <h2>Audit Logs</h2>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>User ID</th>
                        <th>Partner ID</th>
                        <th>Purpose</th>
                        <th>Data Accessed</th>
                    </tr>
                </thead>
                <tbody>
                    {auditLogs.map((log, index) => (
                        <tr key={index}>
                            <td>{new Date(log.timestamp).toLocaleString()}</td>
                            <td>{log.user_id}</td>
                            <td>{log.partner_id}</td>
                            <td>{log.purpose}</td>
                            <td>{log.data_accessed}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AuditTable;