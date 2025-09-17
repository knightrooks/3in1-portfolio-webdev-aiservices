# API Documentation

## Overview

The 3-in-1 Portfolio Platform provides a comprehensive REST API for accessing portfolio data, web development services, AI agents, and payment processing functionality.

**Base URL**: `https://your-domain.com/api`  
**Version**: v1  
**Authentication**: JWT Bearer tokens

---

## Authentication

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

### Using Authentication
Include the access token in the Authorization header:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## Portfolio API

### Get Portfolio Overview
```http
GET /api/portfolio
```

**Response:**
```json
{
  "profile": {
    "name": "John Doe",
    "title": "Full Stack Developer",
    "bio": "Passionate developer with 5 years of experience...",
    "location": "San Francisco, CA",
    "email": "john@example.com"
  },
  "stats": {
    "projects_completed": 50,
    "years_experience": 5,
    "satisfied_clients": 30,
    "technologies": 15
  }
}
```

### Get Projects
```http
GET /api/portfolio/projects
```

**Query Parameters:**
- `category` - Filter by project category (web, mobile, ai)
- `limit` - Number of projects to return (default: 10)
- `offset` - Pagination offset (default: 0)

**Response:**
```json
{
  "projects": [
    {
      "id": 1,
      "title": "E-commerce Platform",
      "description": "Full-featured online store with payment integration",
      "category": "web",
      "technologies": ["Python", "Flask", "PostgreSQL", "Stripe"],
      "image": "/static/img/portfolio/project1.jpg",
      "url": "https://example-store.com",
      "github": "https://github.com/user/project1",
      "completed_date": "2024-03-15"
    }
  ],
  "total": 25,
  "page": 1,
  "pages": 3
}
```

### Get Single Project
```http
GET /api/portfolio/projects/{id}
```

**Response:**
```json
{
  "id": 1,
  "title": "E-commerce Platform",
  "description": "Comprehensive online store solution...",
  "long_description": "Detailed project description with challenges and solutions...",
  "category": "web",
  "technologies": ["Python", "Flask", "PostgreSQL", "Stripe"],
  "features": [
    "User authentication",
    "Shopping cart functionality",
    "Payment processing",
    "Admin dashboard"
  ],
  "images": [
    "/static/img/portfolio/project1-1.jpg",
    "/static/img/portfolio/project1-2.jpg"
  ],
  "url": "https://example-store.com",
  "github": "https://github.com/user/project1",
  "completed_date": "2024-03-15",
  "client": "ABC Company",
  "testimonial": "Excellent work, exceeded expectations!"
}
```

### Get Skills
```http
GET /api/portfolio/skills
```

**Response:**
```json
{
  "skills": [
    {
      "category": "Backend",
      "technologies": [
        {"name": "Python", "proficiency": 90, "years_experience": 5},
        {"name": "Flask", "proficiency": 85, "years_experience": 3},
        {"name": "PostgreSQL", "proficiency": 80, "years_experience": 4}
      ]
    },
    {
      "category": "Frontend",
      "technologies": [
        {"name": "JavaScript", "proficiency": 85, "years_experience": 4},
        {"name": "React", "proficiency": 75, "years_experience": 2},
        {"name": "CSS", "proficiency": 90, "years_experience": 5}
      ]
    }
  ]
}
```

---

## Web Development Services API

### Get Services
```http
GET /api/webdev/services
```

**Response:**
```json
{
  "services": [
    {
      "id": "website_development",
      "name": "Website Development",
      "description": "Custom website development with modern technologies",
      "features": [
        "Responsive design",
        "SEO optimization",
        "Content management",
        "Performance optimization"
      ],
      "starting_price": 1500,
      "delivery_time": "2-4 weeks"
    },
    {
      "id": "ecommerce_development",
      "name": "E-commerce Development",
      "description": "Full-featured online store solutions",
      "features": [
        "Product catalog",
        "Shopping cart",
        "Payment integration",
        "Order management"
      ],
      "starting_price": 3000,
      "delivery_time": "4-8 weeks"
    }
  ]
}
```

### Calculate Pricing
```http
GET /api/webdev/pricing?service=website&pages=5&features=cms,seo&rush=false
```

**Query Parameters:**
- `service` - Service type (website, ecommerce, app)
- `pages` - Number of pages
- `features` - Comma-separated list of features
- `rush` - Rush delivery (boolean)

**Response:**
```json
{
  "service": "website",
  "base_price": 1500,
  "breakdown": {
    "pages": {"count": 5, "price_per_page": 200, "total": 1000},
    "features": [
      {"name": "cms", "price": 500},
      {"name": "seo", "price": 300}
    ],
    "rush_fee": 0
  },
  "subtotal": 2300,
  "tax": 184,
  "total": 2484,
  "currency": "USD"
}
```

### Submit Quote Request
```http
POST /api/webdev/quote
Content-Type: application/json

{
  "name": "John Smith",
  "email": "john@company.com",
  "company": "Smith & Associates",
  "phone": "+1-555-0123",
  "service_type": "ecommerce",
  "project_description": "Need an online store for handmade crafts",
  "budget_range": "3000-5000",
  "timeline": "2-3 months",
  "features": ["product_catalog", "payment_processing", "inventory_management"],
  "additional_requirements": "Mobile app integration needed"
}
```

**Response:**
```json
{
  "quote_id": "QT-2024-001",
  "status": "submitted",
  "message": "Quote request received successfully. We'll respond within 24 hours.",
  "estimated_price": 4200,
  "estimated_delivery": "8-12 weeks"
}
```

---

## AI Services API

### Get Available Agents
```http
GET /api/ai/agents
```

**Response:**
```json
{
  "agents": [
    {
      "id": "developer",
      "name": "Developer Agent",
      "description": "Expert software developer for coding assistance",
      "personality": "Professional, helpful, detail-oriented",
      "specialties": ["Python", "JavaScript", "Web Development", "Debugging"],
      "avatar": "/static/img/avatars/developer.png",
      "status": "online",
      "pricing": {
        "basic": {"price": 0, "features": ["Limited conversations"]},
        "pro": {"price": 29.99, "features": ["Unlimited conversations", "Code review", "Project assistance"]},
        "enterprise": {"price": 99.99, "features": ["Priority support", "Custom solutions", "Team collaboration"]}
      }
    },
    {
      "id": "data_scientist",
      "name": "Data Scientist Agent",
      "description": "Expert in data analysis, machine learning, and statistics",
      "personality": "Analytical, thorough, research-oriented",
      "specialties": ["Python", "R", "Machine Learning", "Data Visualization", "Statistics"],
      "avatar": "/static/img/avatars/data_scientist.png",
      "status": "online",
      "pricing": {
        "basic": {"price": 0, "features": ["Basic analysis help"]},
        "pro": {"price": 39.99, "features": ["Advanced analytics", "Custom models", "Data insights"]},
        "enterprise": {"price": 149.99, "features": ["Enterprise solutions", "Team training", "Custom algorithms"]}
      }
    }
  ]
}
```

### Start Chat Session
```http
POST /api/ai/chat
Content-Type: application/json
Authorization: Bearer <token>

{
  "agent": "developer",
  "message": "Help me debug this Python function",
  "session_id": "optional-existing-session",
  "context": {
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    "error": "Function is too slow for large numbers"
  }
}
```

**Response:**
```json
{
  "session_id": "sess_abc123",
  "response": "I see the issue! Your fibonacci function uses simple recursion which leads to exponential time complexity. Here's an optimized version using dynamic programming...",
  "agent": "developer",
  "suggestions": [
    {
      "title": "Optimized Fibonacci",
      "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b"
    }
  ],
  "follow_up_questions": [
    "Would you like me to explain the time complexity?",
    "Do you need help with other optimization techniques?"
  ]
}
```

### Get Chat History
```http
GET /api/ai/chat/{session_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "session_id": "sess_abc123",
  "agent": "developer",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:45:00Z",
  "messages": [
    {
      "role": "user",
      "content": "Help me debug this Python function",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "agent",
      "content": "I see the issue! Your fibonacci function...",
      "timestamp": "2024-01-15T10:30:15Z"
    }
  ],
  "usage": {
    "total_messages": 12,
    "total_tokens": 2500
  }
}
```

### Subscribe to Agent
```http
POST /api/ai/subscribe
Content-Type: application/json
Authorization: Bearer <token>

{
  "agent": "data_scientist",
  "plan": "pro",
  "payment_method_id": "pm_card_123456"
}
```

**Response:**
```json
{
  "subscription_id": "sub_abc123",
  "agent": "data_scientist",
  "plan": "pro",
  "status": "active",
  "current_period_start": "2024-01-15T00:00:00Z",
  "current_period_end": "2024-02-15T00:00:00Z",
  "amount": 39.99,
  "currency": "USD"
}
```

---

## Payments API

### Create Payment Intent
```http
POST /api/payments/create-intent
Content-Type: application/json
Authorization: Bearer <token>

{
  "amount": 2500,
  "currency": "usd",
  "service_type": "webdev",
  "description": "Website development project",
  "customer_email": "customer@example.com",
  "metadata": {
    "project_id": "PRJ-001",
    "quote_id": "QT-2024-001"
  }
}
```

**Response:**
```json
{
  "payment_intent_id": "pi_abc123",
  "client_secret": "pi_abc123_secret_xyz",
  "amount": 2500,
  "currency": "usd",
  "status": "requires_payment_method"
}
```

### Process Payment
```http
POST /api/payments/process
Content-Type: application/json
Authorization: Bearer <token>

{
  "payment_intent_id": "pi_abc123",
  "payment_method_id": "pm_card_123456"
}
```

**Response:**
```json
{
  "payment_intent_id": "pi_abc123",
  "status": "succeeded",
  "amount": 2500,
  "currency": "usd",
  "receipt_url": "https://pay.stripe.com/receipts/...",
  "transaction_id": "txn_abc123"
}
```

### Get Payment Status
```http
GET /api/payments/{payment_intent_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "payment_intent_id": "pi_abc123",
  "status": "succeeded",
  "amount": 2500,
  "currency": "usd",
  "created": "2024-01-15T10:30:00Z",
  "succeeded_at": "2024-01-15T10:32:15Z",
  "payment_method": {
    "type": "card",
    "card": {
      "brand": "visa",
      "last4": "4242"
    }
  }
}
```

---

## Contact & Support API

### Submit Contact Form
```http
POST /api/contact
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "subject": "Project Inquiry",
  "message": "I'm interested in discussing a web development project...",
  "phone": "+1-555-0123",
  "company": "Doe Industries",
  "service_interest": "webdev",
  "budget": "5000-10000",
  "timeline": "3-6 months"
}
```

**Response:**
```json
{
  "inquiry_id": "INQ-2024-001",
  "status": "submitted",
  "message": "Thank you for your inquiry. We'll respond within 24 hours.",
  "reference_number": "REF-ABC123"
}
```

### Submit Support Ticket
```http
POST /api/support/ticket
Content-Type: application/json
Authorization: Bearer <token>

{
  "subject": "Payment processing issue",
  "description": "I'm having trouble completing my payment for the AI subscription",
  "priority": "high",
  "category": "billing",
  "attachments": [
    {
      "filename": "screenshot.png",
      "content": "base64-encoded-content"
    }
  ]
}
```

**Response:**
```json
{
  "ticket_id": "TKT-2024-001",
  "status": "open",
  "priority": "high",
  "created_at": "2024-01-15T10:30:00Z",
  "estimated_response_time": "2-4 hours"
}
```

---

## WebSocket API

### AI Chat WebSocket

Connect to: `ws://your-domain.com/ai`

#### Events

**Join Agent Room:**
```json
{
  "event": "join_agent",
  "data": {
    "agent": "developer",
    "session_id": "sess_abc123"
  }
}
```

**Send Message:**
```json
{
  "event": "send_message",
  "data": {
    "message": "Help me with this code",
    "agent": "developer",
    "context": {
      "code": "print('hello world')"
    }
  }
}
```

**Receive Agent Response:**
```json
{
  "event": "agent_response",
  "data": {
    "response": "I can help you with that code!",
    "agent": "developer",
    "session_id": "sess_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Typing Indicator:**
```json
{
  "event": "agent_typing",
  "data": {
    "agent": "developer",
    "typing": true
  }
}
```

---

## Rate Limits

- **Unauthenticated**: 100 requests per hour
- **Authenticated**: 1000 requests per hour
- **Premium Users**: 5000 requests per hour
- **WebSocket**: 60 messages per minute per connection

## Error Responses

All API endpoints return errors in the following format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided data is invalid",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Common Error Codes

- `AUTHENTICATION_REQUIRED` (401)
- `INSUFFICIENT_PERMISSIONS` (403) 
- `RESOURCE_NOT_FOUND` (404)
- `VALIDATION_ERROR` (422)
- `RATE_LIMIT_EXCEEDED` (429)
- `INTERNAL_SERVER_ERROR` (500)

---

## SDKs and Examples

### Python SDK Example

```python
import requests

class PortfolioAPI:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        
    def get_portfolio(self):
        response = requests.get(f"{self.base_url}/api/portfolio")
        return response.json()
        
    def chat_with_agent(self, agent, message, session_id=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "agent": agent,
            "message": message,
            "session_id": session_id
        }
        response = requests.post(
            f"{self.base_url}/api/ai/chat",
            json=data,
            headers=headers
        )
        return response.json()

# Usage
api = PortfolioAPI("https://your-domain.com", "your-api-key")
portfolio = api.get_portfolio()
chat_response = api.chat_with_agent("developer", "Help me debug this code")
```

### JavaScript SDK Example

```javascript
class PortfolioAPI {
  constructor(baseUrl, apiKey = null) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }
  
  async getPortfolio() {
    const response = await fetch(`${this.baseUrl}/api/portfolio`);
    return response.json();
  }
  
  async chatWithAgent(agent, message, sessionId = null) {
    const response = await fetch(`${this.baseUrl}/api/ai/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        agent: agent,
        message: message,
        session_id: sessionId
      })
    });
    return response.json();
  }
}

// Usage
const api = new PortfolioAPI('https://your-domain.com', 'your-api-key');
const portfolio = await api.getPortfolio();
const chatResponse = await api.chatWithAgent('developer', 'Help me debug this code');
```