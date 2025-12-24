# sprout-ai-exam

# Sprout AI Exam – Complete Setup Guide

---

## Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Project Overview](#-project-overview)
- [Running the Services](#-running-the-services)
- [API Endpoints](#-api-endpoints)
- [Streamlit Chat UI](#-streamlit-chat-ui)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [System Requirements](#-system-requirements)
- [Agent Decision Logic](#-agent-decision-logic)
- [Additional Resources](#-additional-resources)
- [License](#-license)

---

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/joanmarievale-collab/sprout-ai-exam.git
cd sprout-ai-exam

# Create environment file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Build and start all services
docker-compose up --build
```

---

### Option 2: Manual Setup (Development)

```bash
# 1. Clone the repository
git clone https://github.com/joanmarievale-collab/sprout-ai-exam.git
cd sprout-ai-exam

# 2. Create virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create .env file
nano .env  # or use any text editor

# 5. Start services (in separate terminals)
# Terminal 1:
cd sentiment_api_service
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2:
cd agent_system
python main.py

# Terminal 3:
streamlit run streamlit/chat_ui.py
```
---

### Prerequisites
- [Python 3.8+ (for manual setup)]
- [Docker & Docker Compose (for Docker setup)]
- [Git]
- [Groq API Key]

---

### Step-by-Step Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/joanmarievale-collab/sprout-ai-exam.git
cd sprout-ai-exam
```
---

#### Step 2: Step 2: Get a Groq API Key

- [1. Go to https://console.groq.com]
- [2. Sign up or log in with your account]
- [3. Navigate to API Keys section]
- [4. Click Create New API Key]
- [5. Copy the key (you'll need it in Step 3)]

#### Step 3: Create Environment File
Create a .env file in the project root:

```bash
# Create empty .env file
touch .env
```
##### Add the following content to .env:

```bash
# ===== App =====
APP_NAME=Technical Exam Sentiment Analysis
APP_VERSION=1.0.0
DEBUG=false
API_PREFIX=/sentiment

# ===== Model =====
MODEL_NAME=cardiffnlp/twitter-roberta-base-sentiment
DEVICE=auto
MAX_TOKENS=512

# ===== Groq LLM (REQUIRED) =====
GROQ_API_KEY=your_groq_api_key_here

# ===== Networking =====
SENTIMENT_AGENT_HOST=localhost
SENTIMENT_AGENT_PORT=8000
```
Replace your_groq_api_key_here with your actual Groq API key from Step 2.
---


