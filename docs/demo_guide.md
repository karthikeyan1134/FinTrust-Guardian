# Demo Guide for FinTrust Guardian

## Overview

This demo guide provides a step-by-step walkthrough for showcasing the FinTrust Guardian application. It is designed to help you effectively demonstrate the key features and functionalities of the system during technical interviews or presentations.

## Preparation

Before starting the demo, ensure that you have completed the following steps:

1. **Clone the Repository**: Make sure you have the latest version of the project.
   ```bash
   git clone https://github.com/yourusername/fintrust-guardian.git
   cd fintrust-guardian
   ```

2. **Install Dependencies**: Follow the installation instructions in the README to set up both the backend and frontend.
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ../frontend
   npm install
   ```

3. **Initialize Mock Data**: Generate mock data for demonstration purposes.
   ```bash
   python scripts/generate_mock_data.py
   ```

4. **Start the Services**: Launch the backend, data exchange, and frontend services.
   ```bash
   # Start Policy Gateway
   cd backend
   python app.py &

   # Start Data Vault
   cd ../data-exchange
   python server.py &

   # Start Compliance Dashboard
   cd ../frontend
   npm start
   ```

## Demo Workflow

### 1. Introduction

- Briefly introduce the FinTrust Guardian project and its purpose in privacy-preserving data sharing in fintech.
- Highlight the importance of regulatory compliance and user privacy.

### 2. Policy Gateway Demonstration

- Show how the Policy Gateway manages data sharing requests.
- Use the following cURL command to simulate a partner data request:
  ```bash
  curl -X POST http://localhost:5000/authorize \
    -H "Content-Type: application/json" \
    -d '{
      "partner_id": "partner_ABC",
      "user_id": "user_123",
      "purpose": "loan_application"
    }'
  ```

- Explain the response, focusing on the secure token and its significance.

### 3. Data Exchange Process

- Demonstrate how the secure data exchange works using the token received from the Policy Gateway.
- Run the client script to retrieve secure data:
  ```bash
  cd data-exchange
  python client.py --token "your_secure_token" --host localhost --port 9999
  ```

- Discuss the ephemeral nature of the connection and the security measures in place.

### 4. Compliance Dashboard

- Navigate to the Compliance Dashboard at `http://localhost:3000`.
- Showcase the real-time monitoring features:
  - Live view of data sharing activities.
  - Audit logs and policy visualization.
  
### 5. Highlight Key Features

- **Privacy-by-Design**: Explain data minimization and purpose limitation.
- **Security Features**: Discuss token-based authentication, ephemeral connections, and data masking.
- **Compliance & Monitoring**: Emphasize the importance of audit trails and regulatory reporting.

### 6. Conclusion

- Summarize the key points demonstrated during the session.
- Invite questions and provide clarifications as needed.

## Tips for a Successful Demo

- Practice the demo multiple times to ensure smooth execution.
- Be prepared to answer questions about the architecture, technology stack, and security features.
- Highlight the real-world applications and benefits of the FinTrust Guardian framework.

By following this guide, you will be able to effectively demonstrate the capabilities of the FinTrust Guardian application and showcase your technical skills in privacy-preserving fintech solutions.