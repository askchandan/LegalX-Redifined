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


## Data Files

The repository includes sample legal documents for immediate use:

- **`data/ipc_sections_cleaned.json`** - Processed Indian Penal Code sections (77KB)
- **`data/ipc_sections_formatted.pdf`** - Formatted IPC document (63KB)
- **`data/Cyber Crimes Offenses & Penalties In India[1].pdf`** - Cyber crime laws (388KB)

**Note**: These files are included for demonstration. For production use, replace with your own legal documents or additional Indian legal texts.

## Demo

🚀 **Live Demo**: Ask legal questions and get instant AI-powered responses!

## GitHub About Description

```
🤖 LegalX - AI-Powered Legal Assistant

An intelligent chatbot that provides instant answers to legal questions using advanced AI and vector search technology. Built with FastAPI backend and Next.js frontend, it processes Indian legal documents to deliver context-aware responses about laws, regulations, and legal procedures.

✨ Features: AI chat, semantic search, legal knowledge base, real-time streaming, modern web UI
🛠️ Tech: Python, FastAPI, Next.js, React, ChromaDB, Ollama, HuggingFace
```

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