from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import asyncio
import httpx
import textwrap
import networkx as nx
import re
import json

from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vector_store
    print("[Startup] Loading embeddings & vector store...")
    embeddings = HuggingFaceEmbeddings(model_name="./all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory="chroma_store",
        embedding_function=embeddings
    )
    print("[Startup] Vector store ready.")
    yield
    # Cleanup if needed

app = FastAPI(title="Offline RAG API (Chroma + Qwen via Ollama)-Legal X", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PromptRequest(BaseModel):
    prompt: str


import os

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
TEMPERATURE = 0.0
TOP_P = 0.9
REPEAT_PENALTY = 1.1
MAX_TOKENS = 200
TOP_K = 1

# Globals
vector_store = None
MAX_CONTEXT_LENGTH = 800  # Maximum context length for the model 

def build_knowledge_graph(context: str) -> dict:
    G = nx.Graph()
    entities = []
    # Improved regex for legal entities
    act_pattern = re.compile(r'(\w+ Act)', re.IGNORECASE)
    section_pattern = re.compile(r'(Section \d+)', re.IGNORECASE)
    for line in context.split('\n'):
        acts = act_pattern.findall(line)
        sections = section_pattern.findall(line)
        for act in acts:
            entities.append(('Act', act.strip()))
        for sec in sections:
            entities.append(('Section', sec.strip()))
    # Add nodes
    for ent_type, ent in entities:
        G.add_node(ent, type=ent_type)
    # Infer relationships: link sections to acts if in same line or nearby
    lines = context.split('\n')
    for i, line in enumerate(lines):
        acts_in_line = act_pattern.findall(line)
        sections_in_line = section_pattern.findall(line)
        for act in acts_in_line:
            for sec in sections_in_line:
                G.add_edge(act.strip(), sec.strip(), relation='belongs_to')
        # Check nearby lines for broader relations
        if i > 0:
            prev_acts = act_pattern.findall(lines[i-1])
            for act in prev_acts:
                for sec in sections_in_line:
                    G.add_edge(act.strip(), sec.strip(), relation='related')
    return {
        'nodes': [{'id': node, 'type': data['type']} for node, data in G.nodes(data=True)],
        'edges': [{'source': u, 'target': v, 'relation': data['relation']} for u, v, data in G.edges(data=True)]
    }


@app.post("/generate", response_model=Dict[str, object])
async def generate_response(request: PromptRequest):
    # Check if vector_store is initialized
    if vector_store is None:
        raise HTTPException(status_code=500, detail="Vector store not initialized. Check startup logs and chroma_store directory.")

    # Retrieve relevant documents with scores
    docs = await asyncio.to_thread(
        vector_store.similarity_search_with_score, request.prompt, TOP_K
    )

    if not docs:
        def sorry_stream():
            yield '{"response": "Sorry, I cannot answer that based on the available documents.", "context_sources": []}'
        return StreamingResponse(sorry_stream(), media_type="application/json")

    # Concatenate context
    context = "\n\n".join([doc[0].page_content for doc in docs])
    if len(context) > MAX_CONTEXT_LENGTH:
        context = context[:MAX_CONTEXT_LENGTH]

    # Build knowledge graph from context
    graph_data = build_knowledge_graph(context)

    prompt = textwrap.dedent(f"""
You are a legal assistant for Indian law. Answer based on context. Be concise (1-3 sentences). Mention Act, Section, penalty if available. Formal tone.

Context:
{context}

Answer:
    """)

    async def stream_ollama():
        headers = {}
        if OLLAMA_API_KEY:
            headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"
        
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/generate",
                headers=headers,
                json={
                    "model": "qwen3:0.6b",
                    "prompt": prompt,
                    "stream": True,
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "repeat_penalty": REPEAT_PENALTY,
                    "max_tokens": MAX_TOKENS
                },
                timeout=120.0
            ) as response:
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Ollama model error.")
                answer_accum = ""
                think_accum = ""
                thinking_phase = True
                response_phase = False
                
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        chunk = httpx.Response(200, content=line).json()
                    except Exception:
                        continue
                    text = chunk.get("response", "")
                    thinking = chunk.get("thinking", "")
                    done = chunk.get("done", False)
                    
                    answer_accum += text
                    if thinking:
                        think_accum += thinking
                    
                    # Removed delay for faster streaming
                    # await asyncio.sleep(0.03)  # 30ms delay
                    
                    if thinking_phase and thinking:
                        # Send thinking update less frequently
                        if len(think_accum) % 50 == 0 or done:  # Send every 50 chars or when done
                            response_data = {
                                "phase": "thinking",
                                "think": think_accum.strip(),
                                "response": "",
                                "context_sources": [
                                    {
                                        "source": doc[0].metadata.get("source", "unknown"),
                                        "text": doc[0].page_content,
                                        "score": doc[1]
                                    }
                                    for doc in docs
                                ],
                                "knowledge_graph": graph_data
                            }
                            yield json.dumps(response_data) + '\n'
                    
                    if done:
                        # Final response
                        response_data = {
                            "phase": "response",
                            "think": think_accum.strip(),
                            "response": answer_accum.strip(),
                            "context_sources": [
                                {
                                    "source": doc[0].metadata.get("source", "unknown"),
                                    "text": doc[0].page_content,
                                    "score": doc[1]
                                }
                                for doc in docs
                            ],
                            "knowledge_graph": graph_data
                        }
                        yield json.dumps(response_data) + '\n'
                        break
    return StreamingResponse(stream_ollama(), media_type="application/json")

@app.get("/health")
async def health():
    return {"status": "healthy" if vector_store else "unhealthy"}

