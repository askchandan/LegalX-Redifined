# LegalX - AI-Powered Legal Assistant

## Description

LegalX is an intelligent legal assistant chatbot that leverages advanced AI and vector search technology to provide instant, accurate answers to legal questions. Built with FastAPI backend and Next.js frontend, it processes Indian legal documents to deliver context-aware responses about laws, regulations, and legal procedures.

The system combines:
- **Natural Language Processing** for understanding legal queries
- **Vector Embeddings** for semantic search through legal documents
- **Streaming AI Responses** powered by Ollama/Qwen models
- **Modern Web Interface** with real-time chat functionality

Perfect for law students, legal professionals, and anyone seeking quick legal guidance.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **🤖 AI-Powered Chat**: Interactive legal assistant using advanced language models
- **🔍 Semantic Search**: Vector-based search through legal documents for accurate answers
- **📚 Legal Knowledge Base**: Processes and indexes Indian legal documents (IPC sections, laws)
- **⚡ Real-time Streaming**: Live response streaming for better user experience
- **🎨 Modern UI**: Clean, responsive web interface built with Next.js
- **🔧 RESTful API**: FastAPI backend for scalable legal query processing
- **🧠 Knowledge Graphs**: Enhanced understanding through connected legal concepts

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/askchandan/LegalX.git
    cd LegalX
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup the frontend (optional):**

    ```bash
    cd workspace
    npm install
    npm run build
    cd ..
    ```

## Usage

1.  **Data Setup:**

    The repository includes sample legal data. Run the setup script to verify everything is ready:

    ```bash
    python setup_data.py
    ```

    This will check your data files and provide setup instructions.

2.  **Building the Vector Store:**

    ```bash
    python built_vector_store.py
    ```

    This processes legal documents and creates a searchable vector store.

3.  **Running the Backend API:**

    ```bash
    python api_2.py
    ```

    The API will start on `http://localhost:8000`

4.  **Running the Frontend (optional):**

    ```bash
    cd workspace
    npm run dev
    ```

    The web interface will be available at `http://localhost:3000`


## Deployment

### Frontend Deployment (Vercel)

1. **Deploy to Vercel:**

   - Connect your GitHub repository to Vercel
   - Vercel will automatically detect the Next.js app in the `workspace/` directory
   - The build settings are configured in `vercel.json`

2. **Environment Variables:**

   Set the following environment variable in your Vercel dashboard:

   ```
   NEXT_PUBLIC_API_URL=https://your-backend-api-url.com
   ```

   Replace `https://your-backend-api-url.com` with your deployed backend URL.

3. **Deploy:**

   ```bash
   # Push to main branch to trigger automatic deployment
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

### Backend Deployment Options

Since Vercel doesn't support Python backends, deploy your FastAPI backend to one of these platforms:

#### 🚀 **Railway** (Recommended - Free tier available)
1. Go to [Railway.app](https://railway.app) and sign up
2. Create new project → Deploy from GitHub repo
3. Railway will auto-detect Python and install requirements.txt
4. Your backend URL will be: `https://your-project-name.up.railway.app`

#### 🐘 **Render** (Good alternative)
1. Go to [Render.com](https://render.com) and sign up
2. Create new Web Service → Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn api_2:app --host 0.0.0.0 --port $PORT`
5. Your backend URL will be: `https://your-service-name.onrender.com`

#### 🟣 **Heroku** (Classic choice)
1. Install Heroku CLI: `npm install -g heroku`
2. Create `Procfile` in root directory:
   ```
   web: uvicorn api_2:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy: `heroku create` then `git push heroku main`
4. Your backend URL will be: `https://your-app-name.herokuapp.com`

#### 🔧 **DigitalOcean App Platform**
1. Go to [DigitalOcean](https://digitalocean.com) → App Platform
2. Connect GitHub repo
3. Configure as Python app with requirements.txt
4. Your backend URL will be: `https://your-app-name.ondigitalocean.app`

#### ⚠️ **Important Notes for Backend Deployment:**

- **Model Files**: Your `all-MiniLM-L6-v2/` folder (150MB) and `chroma_store/` will be included
- **Memory Requirements**: This app needs ~2GB RAM minimum due to embeddings and ChromaDB
## 🚀 **Best Free Option: Fly.io (Full Stack Deployment)**

**Fly.io** is perfect for your needs - it supports both Python backend + Next.js frontend, doesn't spin down automatically, and has a generous free tier.

### Why Fly.io?
- ✅ **Free tier available** - Pay only for what you use (per second billing)
- ✅ **No automatic spin-down** - Apps stay running
- ✅ **Full stack support** - Python + Next.js together
- ✅ **Global deployment** - Low latency worldwide
- ✅ **Docker support** - Easy deployment

### Quick Fly.io Setup:

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Sign up & Login:**
   ```bash
   fly auth signup
   fly auth login
   ```

3. **Deploy your app:**
   ```bash
   cd your-project-directory
   fly launch
   ```

4. **Set environment variables:**
   ```bash
   fly secrets set OLLAMA_URL=https://ollama.com
   fly secrets set OLLAMA_API_KEY=your_api_key
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

### Fly.io Free Tier Limits:
- **Free credits**: $5/month worth of resources
- **512MB RAM, 1 shared CPU** (sufficient for your app)
- **No spin-down** - stays active
- **Global regions** available

### Alternative: Railway Hobby Plan ($5/month)
If you prefer Railway's interface:
- **$5/month** includes $5 usage credits
- **No spin-down** after credits
- **Better Python support** than Fly.io
- **Easy GitHub integration**

Both options work great with Ollama Cloud!
- **Build Time**: First deployment may take 10-15 minutes due to large dependencies

#### 🔄 **Quick Start (Fly.io + Ollama Cloud - FREE):**
1. **Install Fly CLI**: `iwr https://fly.io/install.ps1 -useb | iex`
2. **Sign up**: `fly auth signup` + Ollama Cloud account
3. **Deploy**: `fly launch` (select your repo)
4. **Set secrets**:
   ```
   fly secrets set OLLAMA_URL=https://ollama.com
   fly secrets set OLLAMA_API_KEY=your_ollama_key
   ```
5. **Deploy**: `fly deploy`
6. **Frontend**: Deploy `workspace/` folder to Vercel, set `NEXT_PUBLIC_API_URL=https://your-fly-app.fly.dev`

**Cost**: FREE (Fly.io gives $5/month credits, Ollama Cloud has free tier)

## Data Files

The repository includes sample legal documents for immediate use:

- **`data/ipc_sections_cleaned.json`** - Processed Indian Penal Code sections (77KB)
- **`data/ipc_sections_formatted.pdf`** - Formatted IPC document (63KB)
- **`data/Cyber Crimes Offenses & Penalties In India[1].pdf`** - Cyber crime laws (388KB)

**Note**: These files are included for demonstration. For production use, replace with your own legal documents or additional Indian legal texts.

## Demo

🚀 **Live Demo**: Ask legal questions and get instant AI-powered responses!


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Chandan Malakar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```