import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/Dashboard.css";

const Dashboard = () => {
	const [auditLogs, setAuditLogs] = useState([]);
	const [policies, setPolicies] = useState([]);

	useEffect(() => {
		fetchAuditLogs();
		fetchPolicies();
	}, []);

	const fetchAuditLogs = async () => {
		try {
			const response = await axios.get("/logs");
			setAuditLogs(response.data);
		} catch (error) {
			console.error("Error fetching audit logs:", error);
		}
	};

	const fetchPolicies = async () => {
		try {
			const response = await axios.get("/policies");
			setPolicies(response.data);
		} catch (error) {
			console.error("Error fetching policies:", error);
		}
	};

	return (
		<div className="dashboard">
			<h1>Compliance Dashboard</h1>
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
							<td>{log.timestamp}</td>
							<td>{log.user_id}</td>
							<td>{log.partner_id}</td>
							<td>{log.purpose}</td>
							<td>{log.data_accessed}</td>
						</tr>
					))}
				</tbody>
			</table>
			<h2>Current Policies</h2>
			<ul>
				{policies.map((policy, index) => (
					<li key={index}>{policy.description}</li>
				))}
			</ul>
		</div>
	);
};

export default Dashboard;
