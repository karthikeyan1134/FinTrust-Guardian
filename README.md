# FinTrust Guardian

> A proof-of-concept framework for privacy-preserving data sharing in fintech, demonstrating how financial institutions can share user data responsibly while maintaining strict privacy controls and regulatory compliance.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Project Overview

FinTrust Guardian addresses the critical tension in fintech between innovation (which requires data sharing) and user privacy protection. The system implements a **decoupled architecture** that separates policy enforcement from data transfer, ensuring that sensitive financial data is shared only when authorized and in the most secure manner possible.

### Key Innovation

- **Control Plane**: Policy Enforcement Gateway manages consent and data masking
- **Data Plane**: Secure Data Exchange handles direct, ephemeral data transfer
- **Immutable Layer**: Cryptographically protected customer PII with tamper detection

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Partner API   │────│ Policy Gateway  │────│   Data Vault    │
│    Request      │    │  (Flask API)    │    │ (Socket Server) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │ Compliance      │
                       │ Dashboard       │
                       │ (React App)     │
                       └─────────────────┘
```

## ✨ Features

### 🔐 Privacy-by-Design

- **Data Minimization**: Only required data segments are shared
- **Purpose Limitation**: Centralized policy engine enforces data usage rules
- **Consent Management**: User consent tracked and enforced at the gateway level

### 🛡️ Security Features

- **Token-based Authentication**: One-time-use tokens for data access
- **Ephemeral Connections**: Direct socket connections that close immediately after transfer
- **Data Masking**: Real-time tokenization and redaction of sensitive fields
- **Immutable Audit Trail**: Cryptographically protected access logs

### 📊 Compliance & Monitoring

- **Real-time Dashboard**: Live view of all data sharing activities
- **Audit Logging**: Complete trail of who accessed what data and when
- **Policy Visualization**: Clear view of current data sharing policies
- **Regulatory Reporting**: Built-in compliance reporting capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/fintrust-guardian.git
cd fintrust-guardian
```

2. **Set up the backend**

```bash
cd backend
pip install -r requirements.txt
```

3. **Set up the frontend**

```bash
cd frontend
npm install
```

4. **Initialize mock data**

```bash
python scripts/generate_mock_data.py
```

### Running the Application

1. **Start the Policy Gateway**

```bash
cd backend
python app.py
# Server runs on http://localhost:5000
```

2. **Start the Data Vault**

```bash
cd data-exchange
python server.py
# Socket server listens on port 9999
```

3. **Start the Compliance Dashboard**

```bash
cd frontend
npm start
# Dashboard available at http://localhost:3000
```

## 🔧 Usage Example

### 1. Partner Data Request

```bash
curl -X POST http://localhost:5000/authorize \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": "partner_ABC",
    "user_id": "user_123",
    "purpose": "loan_application"
  }'
```

### 2. Response with Secure Token

```json
{
	"status": "approved",
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
	"exchange_host": "localhost",
	"exchange_port": 9999,
	"expires_in": 300
}
```

### 3. Secure Data Retrieval

```bash
cd data-exchange
python client.py --token "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
                 --host localhost --port 9999
```

## 📁 Project Structure

```
FinTrust-Guardian/
├── backend/                  # Policy Enforcement Gateway (Flask)
├── data-exchange/           # Secure Data Exchange (Socket)
├── frontend/                # Compliance Dashboard (React)
├── immutable_store/         # Cryptographic PII protection
├── tests/                   # Comprehensive test suite
├── scripts/                 # Utility and setup scripts
└── docs/                    # Detailed documentation
```

## 🧪 Testing

Run the complete test suite:

```bash
# Backend tests
cd backend && python -m pytest tests/

# Frontend tests
cd frontend && npm test

# Integration tests
python tests/test_integration/test_full_workflow.py
```

## 📚 Documentation

- **[Architecture Guide](docs/architecture.md)** - Detailed system design and components
- **[API Documentation](docs/api_documentation.md)** - Complete API reference
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions
- **[Demo Guide](docs/demo_guide.md)** - Step-by-step interview demonstration

## 🎯 Use Cases

### Financial Institution Scenarios

- **Loan Applications**: Share transaction history with lending partners
- **Credit Scoring**: Provide masked financial data to credit bureaus
- **Regulatory Reporting**: Secure data sharing with government agencies
- **Third-party Integrations**: API access for fintech partners

### Key Benefits

- **Regulatory Compliance**: GDPR, PCI DSS, and financial regulation adherence
- **Risk Mitigation**: Reduced data exposure through ephemeral transfers
- **Audit Readiness**: Complete, immutable audit trail for compliance reviews
- **Developer-Friendly**: Clear APIs and comprehensive documentation

## 🛠️ Technology Stack

### Backend

- **Flask**: RESTful API server and policy engine
- **Python Sockets**: Direct, secure data transfer protocol
- **Cryptography**: AES encryption and SHA-256 hashing
- **JSON**: Policy and data storage (easily upgradeable to databases)

### Frontend

- **React**: Modern, responsive dashboard interface
- **Axios**: HTTP client for API communication
- **Chart.js**: Data visualization for audit logs
- **Tailwind CSS**: Utility-first styling framework

### Security

- **JWT Tokens**: Secure, time-limited access tokens
- **Hash Chains**: Blockchain-inspired data integrity verification
- **Data Masking**: Real-time PII protection and tokenization

## 🤝 Contributing

This is a demonstration project created for technical interviews. However, contributions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact & Demo

**Project Creator**: [Your Name]
**Email**: [your.email@example.com]
**LinkedIn**: [your-linkedin-profile]

### Interview Demo Available

This project includes a comprehensive demo script for technical interviews. The complete workflow can be demonstrated in 10-15 minutes, showcasing full-stack development, system architecture, and security implementation skills.

**Key Demo Points**:

- Live policy enforcement and data masking
- Real-time audit trail visualization
- Secure socket-based data transfer
- Immutable PII protection demonstration

---

_Built with ❤️ to demonstrate privacy-preserving fintech solutions_
