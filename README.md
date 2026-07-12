# 🚀 AppVerse Lite — AI-Powered Application Discovery Platform

> *Intelligent app discovery with intent-based search, AI-generated insights, and conversational assistance powered by Gemini*

---

## 📋 Overview

**AppVerse Lite** is a next-generation application marketplace built with a microservices architecture that seamlessly integrates artificial intelligence to revolutionize how users discover and understand applications. Unlike traditional app directories that rely on static descriptions and basic filtering, AppVerse Lite uses cutting-edge AI to dynamically generate rich app descriptions, understand user intent through natural language search, and provide real-time conversational assistance.

The platform leverages **Google's Gemini 2.5 Flash LLM** combined with **Retrieval-Augmented Generation (RAG)** using FAISS and sentence transformers for semantic search capabilities. This means users don't just search for apps—they have an intelligent assistant that understands what they're looking for, even if they don't know exactly which category they need. Developers can create or update app listings, and the AI automatically generates comprehensive summaries, use cases, and benefits that help potential users quickly understand the value proposition.

The architecture decouples concerns through specialized Spring Boot microservices (User Service, App Service) backed by MySQL, a reactive API Gateway, and a dedicated Python FastAPI AI microservice. This modular design ensures scalability, maintainability, and the flexibility to enhance AI capabilities independently without impacting the core business logic. Everything runs in Docker containers, making deployment effortless across any environment.

---

## 🧠 How It Works

### 1️⃣ **AI App Description Generator**

The AI Description Generator transforms basic app metadata into rich, compelling content that helps potential users make informed decisions quickly.

**End-to-End Flow:**
```
Developer Input (App Name + Description + Category)
              ↓
App Service receives create/update request
              ↓
Sends structured payload to AI Service (/explain endpoint)
              ↓
FastAPI routes to AI microservice (port 8001)
              ↓
Gemini 2.5 Flash LLM analyzes the app metadata
              ↓
Generates JSON response with:
  • Professional summary
  • Practical use cases (list)
  • Key benefits (list)
              ↓
Response sent back through App Service
              ↓
Frontend displays AI-generated insights to users
```

**Example:**
- **Input:** Finance app called "BudgetPro" with description "Track spending"
- **AI Output:** Detailed summary explaining it's for personal finance management, use cases like household budgeting and expense categorization, benefits like spending visibility and financial goals

---

### 2️⃣ **Intent-Based Smart Search**

Smart Search understands what users *mean* to find, not just keyword matches. It combines LLM-powered intent detection with semantic search powered by embeddings.

**End-to-End Flow:**
```
User enters query: "I want to track my money" or "Find health apps for meditation"
              ↓
Search request sent to AI Service (/search endpoint)
              ↓
Step 1 - INTENT DETECTION:
   Gemini analyzes query and classifies into category
   (e.g., "track my money" → Finance, "meditation" → Health)
              ↓
Step 2 - CATEGORY FILTERING:
   Fetch all apps matching detected category from database
              ↓
Step 3 - SEMANTIC EMBEDDING:
   Convert user query to vector embedding using sentence-transformers
   Convert each app to embedding (app name + category + description)
              ↓
Step 4 - VECTOR SEARCH WITH FAISS:
   Use FAISS (meta's vector database) to find top-3 most similar apps
   Returns semantically relevant results (not keyword-based)
              ↓
Step 5 - SMART OVERVIEW:
   Gemini generates contextual summary explaining why these results match
              ↓
Response to frontend:
{
  "category": "Finance",
  "apps": [
    "BudgetPro: Track spending...",
    "MoneyMind: Financial planning...",
    "SpendWise: Smart budgeting..."
  ],
  "overview": "These finance apps help you track and manage your money..."
}
              ↓
Frontend displays ranked results with AI summary
```

---

### 3️⃣ **Conversational Chat Assistant**

Real-time chat that understands context, maintains conversation history, and provides intelligent responses about both apps and platform usage.

**End-to-End Flow:**
```
User types message in chat: "How do I upload my app?"
              ↓
Chat request sent to AI Service (/chat endpoint)
              ↓
Session ID used to retrieve previous conversation history (max 6 messages)
              ↓
Construct prompt with:
   • Previous conversation context
   • Current user message
   • System role: "Helpful AI Assistant"
              ↓
Send to Gemini API with conversation context
              ↓
LLM generates contextually aware response
              ↓
Response stored in session memory (FastAPI server)
              ↓
Message history updated:
   - User: "How do I upload my app?"
   - Assistant: "Go to dashboard, click Upload button..."
              ↓
Next user message includes full conversation history
              ↓
Multi-turn conversation flows naturally with continuity
```

**Alternative - Platform Assistant** (`/assistant` endpoint):
- Specialized version that only answers platform-related questions
- Configured to discuss: uploading, updating, dashboard, browsing, navigation
- Rejects off-topic queries professionally

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                  │
│                    Angular Frontend (Browser)                        │
│  [User Dashboard] [App Browse] [AI Chat] [Search Bar]                │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP/REST
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   API GATEWAY (Spring Boot)                          │
│              Port 8080 - Route & Load Balance                        │
│  - Request routing                                                   │
│  - Load balancing                                                    │
│  - Common auth/logging                                               │
└──┬─────────────────┬──────────────────┬──────────────────────────────┘
   │                 │                  │
   ↓                 ↓                  ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
│ USER SERVICE │ │ APP SERVICE  │ │ AI SERVICE (FastAPI) │
│ Spring Boot  │ │ Spring Boot  │ │ Python + Uvicorn     │
│ Port 8081    │ │ Port 8082    │ │ Port 8001            │
├──────────────┤ ├──────────────┤ ├──────────────────────┤
│ • Auth       │ │ • CRUD Apps  │ │ • /explain           │
│ • JWT        │ │ • Search ops │ │ • /search            │
│ • User mgmt  │ │ • Call AI    │ │ • /chat              │
│              │ │   Service    │ │ • /assistant         │
└──────┬───────┘ └──────┬───────┘ │                      │
       │                │         ├─────────────────────┤
       │                │         │ RAG Components:     │
       │                │         │ • FAISS index       │
       │                │         │ • Sentence Trans    │
       │                │         │ • Chat memory       │
       │                │         └──────┬──────────────┘
       │                │                │
       └────────┬───────┴────────────────┘
                │ (Internal APIs)
                ↓
      ┌─────────────────────┐
      │   MySQL Database    │
      │   (Containerized)   │
      ├─────────────────────┤
      │ • Users             │
      │ • Apps              │
      │ • Interactions      │
      │ • Categories        │
      └─────────────────────┘

External API Call:
AI Service → Google Gemini 2.5 Flash API (LLM Processing)
```

**Data Flow for AI Search Request:**
```
User Query "Find finance apps"
    ↓
API Gateway → App Service (/search)
    ↓
App Service → AI Service (/search)
    ↓
[AI Service Steps]
1. Gemini detects: category = "Finance"
2. Query MySQL: SELECT * FROM apps WHERE category = "Finance"
3. FAISS embedding: convert query to vector
4. FAISS search: find top-3 semantically similar apps
5. Gemini summary: generate contextual overview
    ↓
Response with category, results, and AI summary
    ↓
App Service → API Gateway
    ↓
Frontend renders results with explanations
```

---

## 📚 Tech Stack

| **Category** | **Technology** | **Purpose** |
|---|---|---|
| **Backend** | Spring Boot 3.2.5 | Application framework for microservices |
| | Java 17 | Primary language for backend services |
| | Spring Cloud Gateway | API Gateway for request routing and load balancing |
| | Spring Security | Authentication and authorization |
| | Spring WebFlux | Reactive, non-blocking web framework |
| | Feign Client | Declarative HTTP client for inter-service communication |
| | Lombok | Reduce boilerplate Java code |
| **AI Service** | FastAPI | Modern, fast Python web framework for AI APIs |
| | Uvicorn | ASGI server for FastAPI |
| | Python 3.x | Programming language for AI service |
| **LLM & AI** | Google Generative AI (Gemini 2.5 Flash) | Large language model for text generation |
| | FAISS (Facebook AI Similarity Search) | Vector similarity search for semantic matching |
| | Sentence Transformers | Convert text to semantic embeddings |
| | NumPy | Numerical operations for embedding processing |
| **Database** | MySQL 8.0 | Relational database for persistent storage |
| **DevOps & Deployment** | Docker | Containerization of all services |
| | Docker Compose | Multi-container orchestration and deployment |
| | Docker Hub | Container image registry |
| **Testing** | Spring Boot Test | Unit and integration testing for Java services |
| **API Standards** | REST | HTTP-based API communication |
| | Pydantic | Data validation for FastAPI |

---

## ✨ Key Features

### 🤖 **AI-Powered Description Generation**
Automatically generates comprehensive app summaries with use cases and benefits. When a developer uploads or updates an app, the Gemini API analyzes the metadata and creates marketing-ready content in seconds. No manual copywriting needed—AI ensures consistent, professional descriptions that highlight real value.

### 🔍 **Intent-Based Smart Search**
Understands what users *mean* rather than just matching keywords. Type "apps for managing my finances" and the system detects you want Finance category apps, then uses semantic search (FAISS embeddings) to find the most relevant matches. Works across multiple languages and conversational phrasing.

### 💬 **Multi-Turn Chat with Memory**
Stateful conversational assistant that remembers previous messages in the same session. Ask follow-up questions naturally; the AI maintains context across the conversation. Session IDs allow users to have independent conversations that don't interfere with each other.

### 🎯 **Specialized Assistant Responses**
Dedicated `/assistant` endpoint that provides platform-focused guidance. Ask "How do I upload an app?" and get step-by-step instructions. Intelligently rejects off-topic questions while staying helpful within the platform's scope.

### 🔐 **Secure Multi-Tenant Architecture**
User Service handles JWT-based authentication with secure token expiration (24 hours). Each user is isolated; they can only modify their own apps. Internal API calls use secret key validation (X-INTERNAL-KEY header) to prevent unauthorized service-to-service communication.

### 📊 **Interaction Logging & Analytics**
Every user action (app creation, updates, searches, chat interactions) is logged to the database. Enables user behavior tracking, feature usage analytics, and debugging. Timestamps captured for all events.

### 🏷️ **Dynamic Category Management**
Categories (Finance, Entertainment, Health, Productivity) are configurable and extensible. Apps are tagged by category for faster filtering. AI uses category data to improve search accuracy and relevance.

### 🔄 **RAG Pipeline for Semantic Search**
Uses Retrieval-Augmented Generation combining FAISS vector similarity search with LLM-powered result summarization. Converts unstructured app data into embeddings, finds semantically closest matches, then generates human-readable explanations of *why* these results match the query.

### 🚀 **Microservices Scalability**
Each service (User, App, AI) runs independently in Docker containers. Services can be scaled, updated, or replaced without affecting others. API Gateway abstracts complexity; frontend always talks to the gateway, never directly to services.

### 🔗 **Inter-Service Communication**
Services communicate via REST APIs. App Service uses Feign client to call User Service for user lookups. App Service calls AI Service for explanation and search operations. All calls are synchronous with proper error handling.

### 📦 **Containerized Deployment**
Complete Docker Compose setup for local development and production deployment. All services (MySQL, User Service, App Service, API Gateway, AI Service) start with one command. Environment variables configurable per deployment.

### 🛡️ **Error Handling & Resilience**
Global exception handlers in Spring Boot services convert errors to user-friendly responses. AI Service includes retry logic with exponential backoff for Gemini API rate limits (429 errors). Graceful degradation when external APIs are unavailable.

---

## 🚀 Getting Started

### 📋 Prerequisites

Before you begin, ensure you have installed:

- **Docker** (v20.10+) and **Docker Compose** (v1.29+)
- **Java 17** (for local Spring Boot development)
- **Python 3.9+** (for local FastAPI development)
- **Maven 3.8+** (for building Spring Boot services)
- **Git** (for version control)
- **Google Generative AI API Key** (from [Google AI Studio](https://aistudio.google.com/app/apikey))

### 📥 Installation

#### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/appverse-lite.git
cd appverse-lite
```

#### **2. Configure Environment Variables**

Create a `.env` file in the root directory:

```env
# MySQL Configuration
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_DATABASE=appverse_lite

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_min_32_chars
JWT_EXPIRATION_MS=86400000

# Google Gemini API
GEMINI_API_KEY=your_google_ai_api_key_here

# Service URLs
AI_SERVICE_BASE_URL=http://localhost:8001
APP_SERVICE_BASE_URL=http://localhost:8082
USER_SERVICE_BASE_URL=http://localhost:8081
```

#### **3. Build All Services**
```bash
# Build all Docker images
docker-compose build
```

#### **4. Start All Services**
```bash
# Start all containers (MySQL, User Service, App Service, API Gateway, AI Service)
docker-compose up -d

# Verify all services are running
docker-compose ps
```

Services will be available at:
- **API Gateway**: http://localhost:8080
- **User Service**: http://localhost:8081
- **App Service**: http://localhost:8082
- **AI Service**: http://localhost:8001

### 🐍 Running the AI Service (FastAPI) - Local Development

If you want to develop/run the AI service locally (not in Docker):

#### **1. Navigate to AI Service**
```bash
cd ai-service
```

#### **2. Create Virtual Environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **4. Configure Environment**
```bash
# Create .env file in ai-service directory
echo GEMINI_API_KEY=your_api_key_here > .env
```

#### **5. Run Development Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Server runs at: http://localhost:8001

Test the health endpoint:
```bash
curl http://localhost:8001/
# Response: {"message":"AI service is running✅"}
```

---

### ☕ Running the Backend (Spring Boot) - Local Development

If you want to run Spring Boot services locally:

#### **1. Start MySQL**
Ensure MySQL is running (via Docker or local installation):
```bash
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=appverse_lite \
  -p 3306:3306 \
  mysql:8.0
```

#### **2. User Service**
```bash
cd user-service

# Build
./mvnw clean package

# Run
java -jar target/user-service-0.0.1-SNAPSHOT.jar
```
Runs at: http://localhost:8081

#### **3. App Service**
```bash
cd app-service

# Build
./mvnw clean package

# Set environment variables
export AI_SERVICE_BASE_URL=http://localhost:8001
export DB_HOST=localhost

# Run
java -jar target/app-service-0.0.1-SNAPSHOT.jar
```
Runs at: http://localhost:8082

#### **4. API Gateway**
```bash
cd api-gateway

# Build
./mvnw clean package

# Run
java -jar target/api-gateway-0.0.1-SNAPSHOT.jar
```
Runs at: http://localhost:8080

---

### 🌐 Running the Frontend (Angular) - Local Development

Frontend runs in your browser (no separate server needed for static assets):

1. **Configure API Gateway URL** in Angular `environment.ts`:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8080/api'
   };
   ```

2. **Build & Serve** (or use your existing Angular CLI setup)
   ```bash
   ng serve --port 4200
   ```

3. **Access at**: http://localhost:4200

---

### 🔑 Environment Variables Reference

| Variable | Description | Example |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | MySQL root password | `SecurePass123!` |
| `MYSQL_DATABASE` | Database name | `appverse_lite` |
| `JWT_SECRET` | Secret key for JWT signing (min 32 chars) | `your_very_secure_secret_key_at_least_32_characters_long` |
| `JWT_EXPIRATION_MS` | JWT token expiry (milliseconds) | `86400000` (24 hours) |
| `GEMINI_API_KEY` | Google Generative AI key | `AIzaSyD...` |
| `AI_SERVICE_BASE_URL` | AI Service URL | `http://ai-service:8001` (Docker) or `http://localhost:8001` (local) |
| `DB_HOST` | MySQL host | `mysql` (Docker) or `localhost` (local) |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USERNAME` | MySQL user | `root` |
| `DB_PASSWORD` | MySQL password | Same as `MYSQL_ROOT_PASSWORD` |

---

## 📡 API Overview

### **App Management Endpoints**

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/apps` | Create a new app | JWT Required |
| `GET` | `/api/apps` | List all apps | Public |
| `GET` | `/api/apps/{id}` | Get app details | Public |
| `PUT` | `/api/apps/{id}` | Update app | JWT Required |
| `POST` | `/api/apps/{id}/explain` | Get AI explanation for app | JWT Required |
| `GET` | `/api/apps/internal/apps/category/{category}` | Get apps by category (internal) | Secret Key |

### **AI Service Endpoints**

| Method | Endpoint | Payload | Response |
|---|---|---|---|
| `POST` | `/ai/explain` | `{ name, description, category }` | `{ summary, use_cases[], benefits[] }` |
| `POST` | `/ai/search` | `{ query }` | `{ category, apps[], overview }` |
| `POST` | `/ai/chat` | `{ session_id, message }` | `{ reply }` |
| `POST` | `/ai/assistant` | `{ message }` | `{ reply }` |
| `GET` | `/` | - | Health check |

### **Authentication Endpoints** (User Service)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register new user |
| `POST` | `/api/auth/login` | Login & get JWT token |
| `POST` | `/api/auth/refresh` | Refresh JWT token |

---

## 🎯 Example Workflows

### **Workflow 1: Upload App with AI Description**
```
1. Developer logs in → gets JWT token
2. POST /api/apps with { name, description, category }
3. App Service creates app record in MySQL
4. App Service calls AI Service POST /ai/explain
5. Gemini generates summary, use cases, benefits
6. Frontend displays auto-generated content
7. Developer can review and optionally edit
```

### **Workflow 2: Semantic Search**
```
1. User types "I need to manage my finances" in search
2. POST /ai/search with { query }
3. Gemini detects category = "Finance"
4. Fetch Finance apps from MySQL
5. Convert query & apps to embeddings
6. FAISS finds top 3 most relevant apps
7. Gemini generates summary: "These finance apps..."
8. Frontend displays ranked results with explanation
```

### **Workflow 3: Chat Assistance**
```
1. User: "How do I update my app?"
2. Chat request includes session_id
3. AI Service retrieves conversation history (max 6 messages)
4. Constructs prompt with history + current message
5. Gemini responds: "Go to dashboard, select your app, click edit..."
6. Response added to session memory
7. User: "What about the category field?"
8. System includes previous context; AI knows we're talking about apps
```

---

## 📁 Project Structure

```
appverse-lite/
├── docker-compose.yml          # Multi-container setup
├── README.md                   # This file
│
├── user-service/               # Spring Boot - Authentication & User Management
│   ├── pom.xml
│   ├── src/main/java/...
│   ├── src/test/java/...
│   └── Dockerfile
│
├── app-service/                # Spring Boot - App CRUD & AI Integration
│   ├── pom.xml
│   ├── src/main/java/
│   │   ├── controller/         # REST endpoints
│   │   ├── service/            # Business logic
│   │   ├── repository/         # Database access
│   │   ├── entity/             # Data models
│   │   └── dto/                # Transfer objects
│   ├── src/test/java/...
│   └── Dockerfile
│
├── api-gateway/                # Spring Boot - Request Routing & Load Balancing
│   ├── pom.xml
│   ├── src/main/java/...
│   └── Dockerfile
│
├── ai-service/                 # FastAPI - AI-Powered Features
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app entry
│   ├── routes/
│   │   └── routing.py          # API endpoints
│   ├── services/
│   │   └── ai_service.py       # LLM integration (Gemini)
│   ├── rag/
│   │   └── RagService.py       # FAISS + embeddings
│   ├── models/
│   │   └── schemas.py          # Request/response models
│   ├── utils/
│   │   ├── AiFunctions.py      # AI helper functions
│   │   ├── chat_memory.py      # Session storage
│   │   └── prompt_templates.py # LLM prompts
│   ├── core/
│   │   └── Config.py           # Configuration
│   ├── springRequests/
│   │   └── fetchAppsByCategory.py  # Call App Service
│   ├── test_models.py
│   └── Dockerfile
│
└── .env.example                # Environment template
```

---

## 🧪 Testing

### **Test AI Service Endpoints**

```bash
# Health check
curl http://localhost:8001/

# Explain an app
curl -X POST http://localhost:8001/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "name": "BudgetPro",
    "description": "Track and manage your spending",
    "category": "Finance"
  }'

# Search apps
curl -X POST http://localhost:8001/ai/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Find apps to manage my money"}'

# Chat with assistant
curl -X POST http://localhost:8001/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "user123", "message": "How do I upload an app?"}'
```

### **Test Backend Services**

```bash
# Get all apps
curl http://localhost:8080/api/apps

# Create app (requires JWT token)
curl -X POST http://localhost:8080/api/apps \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MoneyTracker",
    "description": "Expense tracking app",
    "category": "Finance"
  }'
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| Services won't start in Docker | Run `docker-compose logs` to see error messages |
| MySQL connection refused | Ensure MySQL container is healthy: `docker-compose ps` |
| Gemini API 429 (rate limit) | AI Service has retry logic; wait 1-2 seconds between requests |
| AI Service not responding | Check if `GEMINI_API_KEY` is set in `.env` |
| Frontend can't reach API | Verify API Gateway is running on port 8080 |
| FAISS search returns no results | Ensure apps exist in database and semantic similarity is found |

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows existing style conventions
- Tests are written for new features
- Documentation is updated
- Commits are clearly described

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**  
- GitHub: https://github.com/ankurkumar2002
- Email: ankurkumarsingh0488@gmail.com

---

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact the maintainers
- Check existing documentation

---

**Last Updated**: June 2026  
**Version**: 1.0.0
