# FinTrust Guardian - System Architecture

## Overview

FinTrust Guardian implements a **decoupled architecture** that separates policy enforcement from data transfer, ensuring maximum security, scalability, and auditability for financial data sharing operations.

## Core Architectural Principles

### 1. Separation of Concerns

- **Control Plane**: Manages policies, consent, and authorization
- **Data Plane**: Handles secure, direct data transfer
- **Audit Plane**: Maintains immutable logs and compliance reporting

### 2. Privacy-by-Design

- Data minimization at every layer
- Purpose limitation through centralized policies
- Consent enforcement at the gateway level
- Cryptographic protection of sensitive data

### 3. Zero-Trust Security

- Never trust, always verify
- Token-based authentication for every operation
- Ephemeral connections to minimize exposure
- Immutable audit trails for forensic analysis

## System Components

### 1. Policy Enforcement Gateway (Control Plane)

**Technology**: Flask (Python)
**Port**: 5000
**Purpose**: Central authorization and policy enforcement

```
┌─────────────────────────────────────────────────────────┐
│                Policy Enforcement Gateway               │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Policy    │  │    Data     │  │     Audit       │  │
│  │   Engine    │  │   Masking   │  │    Service      │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  API Endpoints: /authorize, /logs, /policies           │
└─────────────────────────────────────────────────────────┘
```

**Key Responsibilities**:

- Validate partner requests against policies
- Apply real-time data masking and tokenization
- Generate one-time-use access tokens
- Maintain comprehensive audit logs
- Enforce consent and purpose limitations

**Request Flow**:

1. Partner sends data request to `/authorize`
2. Gateway validates against policy store
3. If approved, applies data masking rules
4. Generates secure, time-limited token
5. Returns token with Data Vault connection details
6. Logs entire transaction for audit

### 2. Secure Data Exchange (Data Plane)

**Technology**: Python Sockets
**Port**: 9999
**Purpose**: Direct, ephemeral data transfer

```
┌─────────────────────────────────────────────────────────┐
│                 Secure Data Exchange                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │    Token    │  │    Data     │  │   Connection    │  │
│  │ Validator   │  │   Vault     │  │    Manager      │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Socket Protocol: TCP, One-time tokens, Auto-close     │
└─────────────────────────────────────────────────────────┘
```

**Key Features**:

- Direct socket connections (bypasses web layers)
- Token validation against shared token store
- Automatic connection termination after transfer
- No data caching or intermediate storage
- Real-time transfer success logging

**Transfer Protocol**:

1. Client connects to socket server
2. Client sends token for validation
3. Server validates token against authorized requests
4. If valid, server sends specific data segment
5. Connection immediately closes
6. Token is invalidated to prevent reuse

### 3. Immutable PII Vault (Security Layer)

**Technology**: Python + Cryptography
**Purpose**: Tamper-proof customer data storage

```
┌─────────────────────────────────────────────────────────┐
│                  Immutable PII Vault                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Encryption  │  │ Hash Chain  │  │   Integrity     │  │
│  │   Engine    │  │  Manager    │  │   Validator     │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Features: AES-256, SHA-256, Blockchain-style chains   │
└─────────────────────────────────────────────────────────┘
```

**Security Features**:

- AES-256 encryption for all PII data
- SHA-256 hash chains for integrity verification
- Append-only data structure (no updates, only new records)
- Cryptographic proof of data authenticity
- Tamper detection through hash verification

**Data Structure**:

```json
{
	"block_id": "uuid",
	"user_id": "user_123",
	"encrypted_data": "AES_encrypted_PII",
	"data_hash": "SHA256_of_encrypted_data",
	"previous_hash": "SHA256_of_previous_block",
	"timestamp": "ISO_8601_timestamp",
	"signature": "cryptographic_signature"
}
```

### 4. Compliance Dashboard (Monitoring Plane)

**Technology**: React + JavaScript
**Port**: 3000
**Purpose**: Real-time monitoring and audit visualization

```
┌─────────────────────────────────────────────────────────┐
│                Compliance Dashboard                     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │    Audit    │  │   Policy    │  │     Real-time   │  │
│  │   Viewer    │  │   Display   │  │    Monitoring   │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Components: Tables, Charts, Alerts, Export Tools      │
└─────────────────────────────────────────────────────────┘
```

**Dashboard Features**:

- Real-time audit log display
- Policy compliance monitoring
- Data access pattern visualization
- Alert system for suspicious activities
- Export capabilities for compliance reports

## Data Flow Architecture

### Complete Request-Response Cycle

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Partner   │    │     Policy      │    │  Immutable PII  │
│   Request   │───▶│    Gateway      │───▶│     Vault       │
└─────────────┘    └─────────────────┘    └─────────────────┘
                           │                        │
                           ▼                        ▼
                   ┌─────────────────┐    ┌─────────────────┐
                   │  Token Store    │    │   Data Masking  │
                   │   (Temporary)   │    │     Engine      │
                   └─────────────────┘    └─────────────────┘
                           │                        │
                           ▼                        ▼
                   ┌─────────────────┐    ┌─────────────────┐
                   │  Secure Data    │    │  Audit Logger   │
                   │   Exchange      │    │  (Immutable)    │
                   └─────────────────┘    └─────────────────┘
                           │                        │
                           ▼                        ▼
                   ┌─────────────────┐    ┌─────────────────┐
                   │    Partner      │    │   Compliance    │
                   │    Client       │    │   Dashboard     │
                   └─────────────────┘    └─────────────────┘
```

### Step-by-Step Flow

1. **Request Initiation**

   - Partner sends POST to `/authorize` with partner_id, user_id, purpose
   - Request includes authentication headers

2. **Policy Validation**

   - Gateway loads partner policies from policy store
   - Validates user consent and purpose limitation
   - Checks data access permissions

3. **Data Preparation**

   - Retrieves user data from Immutable PII Vault
   - Decrypts and validates data integrity
   - Applies masking rules based on partner permissions

4. **Token Generation**

   - Creates cryptographically secure one-time token
   - Stores token with associated data permissions
   - Sets expiration time (default: 5 minutes)

5. **Secure Transfer**

   - Partner uses token to connect to Data Vault
   - Socket server validates token and sends data
   - Connection closes immediately after transfer

6. **Audit Logging**
   - Every step is logged with immutable timestamps
   - Audit trail includes request, authorization, and transfer
   - Compliance dashboard updates in real-time

## Security Considerations

### Defense in Depth

1. **Network Security**

   - TLS encryption for all HTTP traffic
   - Socket connections with certificate validation
   - Rate limiting and DDoS protection

2. **Application Security**

   - Input validation and sanitization
   - SQL injection prevention (when using databases)
   - Cross-site scripting (XSS) protection

3. **Data Security**

   - AES-256 encryption for data at rest
   - Secure key management and rotation
   - Data masking and tokenization

4. **Access Control**

   - Token-based authentication
   - Role-based access control (RBAC)
   - Principle of least privilege

5. **Audit and Monitoring**
   - Comprehensive logging of all operations
   - Real-time monitoring and alerting
   - Immutable audit trails

### Threat Model

**Threats Addressed**:

- Unauthorized data access
- Data tampering and integrity violations
- Privilege escalation attacks
- Insider threats and data misuse
- Compliance violations and audit failures

**Mitigations**:

- Multi-layered authentication and authorization
- Cryptographic data protection
- Immutable audit trails
- Real-time monitoring and alerting
- Regular security assessments

## Scalability and Performance

### Horizontal Scaling Options

1. **Policy Gateway**

   - Load balancer with multiple Flask instances
   - Shared policy store (Redis/PostgreSQL)
   - Stateless design for easy scaling

2. **Data Exchange**

   - Multiple socket servers on different ports
   - Load balancing for socket connections
   - Distributed token validation

3. **Dashboard**
   - CDN for static assets
   - API caching for audit data
   - Progressive loading for large datasets

### Performance Optimizations

- **Caching**: Policy and user data caching
- **Connection Pooling**: Database connection management
- **Async Processing**: Non-blocking I/O operations
- **Data Compression**: Reduced transfer sizes
- **Index Optimization**: Fast database queries

## Deployment Architecture

### Development Environment

```
├── Local Development Servers
├── SQLite/JSON File Storage
├── Single-node deployment
└── Hot-reload capabilities
```

### Production Environment

```
├── Load Balancer (nginx/HAProxy)
├── Application Servers (Docker containers)
├── Database Cluster (PostgreSQL/MongoDB)
├── Redis Cache Layer
├── Monitoring Stack (Prometheus/Grafana)
└── Security Tools (WAF/IDS)
```

## Future Enhancements

### Short-term (Phase 2)

- Database integration (PostgreSQL/MongoDB)
- Enhanced encryption key management
- Advanced policy templating
- Mobile-responsive dashboard

### Long-term (Phase 3)

- Machine learning for anomaly detection
- Multi-region deployment support
- Blockchain integration for audit trails
- Advanced compliance reporting tools

---

This architecture provides a robust foundation for privacy-preserving data sharing in financial services while maintaining the flexibility to scale and adapt to evolving regulatory requirements.
