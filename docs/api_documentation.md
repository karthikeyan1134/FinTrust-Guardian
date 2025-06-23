# FinTrust Guardian - API Documentation

## Overview

The FinTrust Guardian API provides secure, policy-driven access to financial data through a RESTful interface. All endpoints implement comprehensive authentication, authorization, and audit logging.

**Base URL**: `http://localhost:5000`
**API Version**: v1
**Content-Type**: `application/json`

## Authentication

All API requests require authentication headers:

```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
X-API-Version: v1
```

## Core Endpoints

### 1. Data Authorization

#### POST /authorize

Request access to user data for a specific purpose.

**Endpoint**: `POST /authorize`

**Request Body**:

```json
{
	"partner_id": "string (required)",
	"user_id": "string (required)",
	"purpose": "string (required)",
	"requested_data": ["array of strings (optional)"],
	"expires_in": "integer (optional, default: 300)"
}
```

**Response - Success (200)**:

```json
{
	"status": "approved",
	"request_id": "uuid",
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
	"exchange_host": "localhost",
	"exchange_port": 9999,
	"expires_in": 300,
	"expires_at": "2024-01-15T10:30:00Z",
	"data_segments": ["transactions_3m", "basic_profile"],
	"masking_applied": ["bank_account", "ssn"]
}
```

**Response - Denied (403)**:

```json
{
	"status": "denied",
	"reason": "insufficient_permissions",
	"message": "Partner not authorized for requested data type",
	"policy_violation": {
		"rule": "data_type_restriction",
		"allowed_data": ["basic_profile"],
		"requested_data": ["full_transactions"]
	}
}
```

**Response - Error (400)**:

```json
{
	"error": "validation_error",
	"message": "Missing required field: user_id",
	"details": {
		"field": "user_id",
		"expected": "string",
		"received": "null"
	}
}
```

**Example Request**:

```bash
curl -X POST http://localhost:5000/authorize \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": "partner_ABC",
    "user_id": "user_123",
    "purpose": "loan_application"
  }'
```

### 2. Audit Logs

#### GET /logs

Retrieve audit logs of data access activities.

**Endpoint**: `GET /logs`

**Query Parameters**:

- `partner_id` (string, optional): Filter by partner
- `user_id` (string, optional): Filter by user
- `start_date` (ISO 8601, optional): Start date filter
- `end_date` (ISO 8601, optional): End date filter
- `status` (string, optional): Filter by status (approved/denied)
- `limit` (integer, optional, default: 100): Number of records
- `offset` (integer, optional, default: 0): Pagination offset

**Response - Success (200)**:

```json
{
	"logs": [
		{
			"id": "uuid",
			"timestamp": "2024-01-15T10:25:30Z",
			"partner_id": "partner_ABC",
			"user_id": "user_123",
			"purpose": "loan_application",
			"status": "approved",
			"data_accessed": ["transactions_3m"],
			"masking_applied": ["bank_account"],
			"token_used": "eyJ0eXAiOiJKV1Q...",
			"transfer_completed": true,
			"transfer_timestamp": "2024-01-15T10:26:45Z",
			"ip_address": "192.168.1.100",
			"user_agent": "PartnerAPI/1.0"
		}
	],
	"pagination": {
		"total": 1250,
		"limit": 100,
		"offset": 0,
		"has_more": true
	}
}
```

**Example Request**:

```bash
curl -X GET "http://localhost:5000/logs?partner_id=partner_ABC&limit=50" \
  -H "Authorization: Bearer <jwt_token>"
```

### 3. Policy Management

#### GET /policies

Retrieve current data sharing policies.

**Endpoint**: `GET /policies`

**Query Parameters**:

- `partner_id` (string, optional): Get policies for specific partner
- `active_only` (boolean, optional, default: true): Only active policies

**Response - Success (200)**:

```json
{
	"policies": [
		{
			"partner_id": "partner_ABC",
			"partner_name": "ABC Lending Corp",
			"status": "active",
			"created_at": "2024-01-01T00:00:00Z",
			"updated_at": "2024-01-10T15:30:00Z",
			"allowed_users": ["user_123", "user_456"],
			"permissions": {
				"loan_application": {
					"data_segments": ["transactions_3m", "basic_profile"],
					"masking_rules": {
						"bank_account": "partial",
						"ssn": "full"
					},
					"rate_limit": {
						"requests_per_hour": 100,
						"daily_limit": 1000
					}
				}
			},
			"compliance": {
				"gdpr_compliant": true,
				"pci_compliant": true,
				"data_retention_days": 90
			}
		}
	]
}
```

#### PUT /policies/{partner_id}

Update policies for a specific partner.

**Endpoint**: `PUT /policies/{partner_id}`

**Request Body**:

```json
{
	"permissions": {
		"loan_application": {
			"data_segments": ["transactions_3m"],
			"masking_rules": {
				"bank_account": "full"
			}
		}
	},
	"rate_limit": {
		"requests_per_hour": 50
	}
}
```

**Response - Success (200)**:

```json
{
	"message": "Policy updated successfully",
	"partner_id": "partner_ABC",
	"updated_fields": ["permissions", "rate_limit"],
	"effective_date": "2024-01-15T10:30:00Z"
}
```

### 4. Data Integrity

#### GET /integrity/verify

Verify the integrity of the immutable PII vault.

**Endpoint**: `GET /integrity/verify`

**Query Parameters**:

- `user_id` (string, optional): Verify specific user's data
- `full_chain` (boolean, optional, default: false): Full chain verification

**Response - Success (200)**:

```json
{
	"status": "verified",
	"verification_timestamp": "2024-01-15T10:30:00Z",
	"blocks_verified": 1500,
	"hash_chain_valid": true,
	"data_integrity": "intact",
	"last_block_hash": "a1b2c3d4e5f6...",
	"verification_details": {
		"total_users": 500,
		"total_blocks": 1500,
		"broken_chains": 0,
		"tampered_blocks": 0
	}
}
```

**Response - Integrity Violation (500)**:

```json
{
	"status": "violation_detected",
	"error": "hash_chain_broken",
	"affected_blocks": [1245, 1246],
	"first_violation": "2024-01-15T09:15:00Z",
	"recommended_action": "immediate_investigation_required"
}
```

### 5. Health and Status

#### GET /health

Check the health status of all system components.

**Endpoint**: `GET /health`

**Response - Healthy (200)**:

```json
{
	"status": "healthy",
	"timestamp": "2024-01-15T10:30:00Z",
	"version": "1.0.0",
	"components": {
		"policy_engine": {
			"status": "healthy",
			"response_time_ms": 15
		},
		"data_vault": {
			"status": "healthy",
			"socket_server": "listening",
			"port": 9999
		},
		"immutable_store": {
			"status": "healthy",
			"integrity": "verified",
			"last_backup": "2024-01-15T06:00:00Z"
		},
		"audit_system": {
			"status": "healthy",
			"log_count": 15000,
			"storage_usage": "45%"
		}
	},
	"metrics": {
		"requests_per_minute": 25,
		"average_response_time": 120,
		"error_rate": 0.02
	}
}
```

## Socket Protocol (Data Exchange)

### Connection Flow

The secure data exchange uses a custom TCP socket protocol:

1. **Client Connection**: Connect to socket server on port 9999
2. **Token Transmission**: Send JWT token as first message
3. **Validation**: Server validates token against authorization store
4. **Data Transfer**: If valid, server sends authorized data
5. **Connection Close**: Server immediately closes connection

### Protocol Messages

#### Client → Server (Token)

```json
{
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
	"protocol_version": "1.0"
}
```

#### Server → Client (Success)

```json
{
	"status": "success",
	"data": {
		"user_id": "user_123",
		"transactions_3m": [
			{ "id": 1, "amount": 100, "date": "2024-01-01" },
			{ "id": 2, "amount": -50, "date": "2024-01-15" }
		],
		"basic_profile": {
			"name": "Jane D***",
			"email": "j***@example.com"
		}
	},
	"metadata": {
		"transfer_id": "uuid",
		"timestamp": "2024-01-15T10:30:00Z",
		"expiry": "2024-01-15T10:35:00Z"
	}
}
```

#### Server → Client (Error)

```json
{
	"status": "error",
	"error_code": "invalid_token",
	"message": "Token has expired or is invalid",
	"timestamp": "2024-01-15T10:30:00Z"
}
```

### Python Socket Client Example

```python
import socket
import json

def retrieve_data(token, host='localhost', port=9999):
    try:
        # Create socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send token
        token_message = {
            "token": token,
            "protocol_version": "1.0"
        }
        client_socket.send(json.dumps(token_message).encode())

        # Receive data
        response = client_socket.recv(4096).decode()
        data = json.loads(response)

        client_socket.close()
        return data

    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Error Codes

### HTTP Status Codes

| Code | Status                | Description                       |
| ---- | --------------------- | --------------------------------- |
| 200  | OK                    | Request successful                |
| 201  | Created               | Resource created successfully     |
| 400  | Bad Request           | Invalid request parameters        |
| 401  | Unauthorized          | Missing or invalid authentication |
| 403  | Forbidden             | Insufficient permissions          |
| 404  | Not Found             | Resource not found                |
| 429  | Too Many Requests     | Rate limit exceeded               |
| 500  | Internal Server Error | Server error occurred             |
| 503  | Service Unavailable   | Service temporarily unavailable   |

### Application Error Codes

| Code                       | Category        | Description                        |
| -------------------------- | --------------- | ---------------------------------- |
| `INVALID_PARTNER`          | Authorization   | Partner ID not recognized          |
| `USER_NOT_FOUND`           | Authorization   | User ID not found                  |
| `INSUFFICIENT_PERMISSIONS` | Authorization   | Partner lacks required permissions |
| `INVALID_PURPOSE`          | Authorization   | Purpose not allowed for partner    |
| `CONSENT_REQUIRED`         | Authorization   | User consent not provided          |
| `RATE_LIMIT_EXCEEDED`      | Rate Limiting   | Too many requests                  |
| `TOKEN_EXPIRED`            | Token           | Access token has expired           |
| `TOKEN_INVALID`            | Token           | Access token is malformed          |
| `DATA_NOT_FOUND`           | Data            | Requested data not available       |
| `MASKING_ERROR`            | Data Processing | Error applying data masking        |
| `INTEGRITY_VIOLATION`      | Security        | Data integrity check failed        |
| `AUDIT_LOG_ERROR`          | Logging         | Failed to write audit log          |

## Rate Limiting

### Default Limits

- **Per Partner**: 1000 requests per hour
- **Per User**: 100 requests per hour
- **Global**: 10,000 requests per hour

### Rate Limit Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248000
X-RateLimit-Window: 3600
```

### Rate Limit Exceeded Response

```json
{
	"error": "rate_limit_exceeded",
	"message": "Too many requests. Limit: 1000/hour",
	"retry_after": 3600,
	"reset_time": "2024-01-15T11:00:00Z"
}
```

## Data Masking Rules

### Masking Types

| Type       | Description        | Example                |
| ---------- | ------------------ | ---------------------- |
| `none`     | No masking applied | `"john.doe@email.com"` |
| `partial`  | Partial masking    | `"j***.doe@email.com"` |
| `full`     | Complete masking   | `"***"`                |
| `tokenize` | Replace with token | `"TKN_AB12CD34EF56"`   |
| `hash`     | One-way hash       | `"a1b2c3d4e5f6..."`    |

### Field-Specific Rules

```json
{
	"masking_rules": {
		"email": "partial",
		"phone": "partial",
		"ssn": "full",
		"bank_account": "tokenize",
		"name": "partial",
		"address": "partial",
		"credit_score": "none"
	}
}
```

## Webhook Notifications

### Event Types

- `data.accessed` - Data was successfully accessed
- `data.denied` - Data access was denied
- `policy.updated` - Partner policy was updated
- `integrity.violation` - Data integrity issue detected
- `rate_limit.exceeded` - Rate limit was exceeded

### Webhook Payload

```json
{
	"event": "data.accessed",
	"timestamp": "2024-01-15T10:30:00Z",
	"request_id": "uuid",
	"partner_id": "partner_ABC",
	"user_id": "user_123",
	"data": {
		"purpose": "loan_application",
		"data_segments": ["transactions_3m"],
		"masking_applied": ["bank_account"]
	}
}
```

## SDK Examples

### Python SDK

```python
from fintrust_guardian import FinTrustClient

# Initialize client
client = FinTrustClient(
    base_url="http://localhost:5000",
    api_key="your_api_key"
)

# Request data access
response = client.authorize(
    partner_id="partner_ABC",
    user_id="user_123",
    purpose="loan_application"
)

if response.status == "approved":
    # Use token to retrieve data
    data = client.retrieve_data(
        token=response.token,
        host=response.exchange_host,
        port=response.exchange_port
    )
    print(data)
```

### JavaScript SDK

```javascript
const FinTrustGuardian = require("fintrust-guardian-js");

const client = new FinTrustGuardian({
	baseUrl: "http://localhost:5000",
	apiKey: "your_api_key",
});

// Request data access
const response = await client.authorize({
	partnerId: "partner_ABC",
	userId: "user_123",
	purpose: "loan_application",
});

if (response.status === "approved") {
	// Retrieve data using token
	const data = await client.retrieveData({
		token: response.token,
		host: response.exchangeHost,
		port: response.exchangePort,
	});
	console.log(data);
}
```

## Testing

### Unit Tests

```bash
# Run API tests
python -m pytest tests/test_api/

# Run specific endpoint tests
python -m pytest tests/test_api/test_authorize.py -v
```

### Integration Tests

```bash
# Full workflow test
python tests/test_integration/test_full_workflow.py

# Load testing
python tests/performance/test_load.py --requests 1000
```

### Mock Data

For testing purposes, use the provided mock data:

```json
{
	"user_123": {
		"pii": {
			"name": "Jane Doe",
			"email": "jane.doe@example.com",
			"phone": "+1-555-0123",
			"ssn": "123-45-6789"
		},
		"financial": {
			"bank_account": "GB29NWBK60161331926819",
			"credit_score": 750
		},
		"transactions_all": [
			{
				"id": 1,
				"amount": 1000,
				"date": "2024-01-01",
				"merchant": "Salary Deposit"
			},
			{
				"id": 2,
				"amount": -50,
				"date": "2024-01-02",
				"merchant": "Coffee Shop"
			}
		],
		"transactions_3m": [
			{
				"id": 1,
				"amount": 1000,
				"date": "2024-01-01",
				"merchant": "Salary Deposit"
			}
		]
	}
}
```

## Security Considerations

### API Security

1. **Authentication**: All endpoints require valid JWT tokens
2. **Authorization**: Role-based access control (RBAC)
3. **Input Validation**: All inputs are validated and sanitized
4. **Rate Limiting**: Prevents abuse and DoS attacks
5. **Audit Logging**: Complete audit trail of all operations

### Data Protection

1. **Encryption**: All sensitive data encrypted at rest
2. **Masking**: Real-time data masking based on permissions
3. **Tokenization**: Sensitive fields replaced with tokens
4. **Integrity**: Cryptographic verification of data integrity
5. **Retention**: Automatic data purging based on policies

### Network Security

1. **TLS**: All HTTP traffic encrypted with TLS 1.3
2. **Certificate Pinning**: Prevents man-in-the-middle attacks
3. **IP Whitelisting**: Restrict access to authorized IPs
4. **Firewall Rules**: Network-level access controls

## Support and Troubleshooting

### Common Issues

1. **Token Expiration**: Tokens expire after 5 minutes by default
2. **Rate Limiting**: Check rate limit headers in responses
3. **Permission Errors**: Verify partner has required permissions
4. **Socket Connection**: Ensure Data Vault is running on port 9999

### Debug Mode

Enable debug logging:

```bash
export FLASK_ENV=development
export FINTRUST_DEBUG=true
python app.py
```

### Monitoring

- **Health Endpoint**: `/health` for system status
- **Metrics**: Prometheus metrics available at `/metrics`
- **Logs**: Structured JSON logs for analysis

---

For additional support, please refer to the [troubleshooting guide](deployment.md#troubleshooting) or contact the development team.
