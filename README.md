# 🎬 AI Video & Meeting Assistant (IntelliMeet)

IntelliMeet is a production-grade, 100% free, localized AI Meeting Intelligence platform built from scratch in Python. It serves as a powerful open-source alternative to premium SaaS platforms like Otter.ai or Fireflies.ai, completely eliminating API usage costs for transcription, ingestion, and local vector retrieval. 

The system effortlessly processes multi-hour YouTube URLs or local media uploads (MP4, MP3, WAV), dynamically transcribes bilingual dialogues (English, Hindi, Hinglish), extracts structured insights, and exposes an interactive Retrieval-Augmented Generation (RAG) conversational pipeline.

---

## 🚀 Key Features

- **Omnichannel Media Ingestion:** Accepts complex YouTube URLs or local raw audio/video files.
- **Bilingual & Mixed-Dialect Speech-to-Text:** 
  - **English:** Locally loaded, hardware-agnostic **OpenAI Whisper AI** pipeline.
  - **Hindi & Hinglish:** Intelligent fallback routing via specialized **Sarvam AI APIs**.
- **Map-Reduce Context Summarization:** Overcomes context window bottlenecks through recursive chunked summarization via **Mistral AI**.
- **Structured Semantic Extraction:** Isolates action items (with identified owners and deadlines), crucial organizational decisions, and outstanding open questions.
- **Localized Retrievable Memory (RAG):** Persists multi-hour session transcripts to an encrypted, localized **ChromaDB** instance utilizing **HuggingFace** semantic embeddings.
- **Cyberpunk Streamlit Interface:** A high-performance, dark-themed frontend optimized with custom reactive pipeline tracking state status.

---

## 🛠️ High-Level System Architecture

The pipeline uses a decoupled, modular design divided across processing layers:

1. **Ingestion Layer (`audio_processor.py`):** Downloads, converts dual-channel stereos into optimized mono audio signals, downsamples sampling frequencies to 16kHz (Whisper's sweet spot), and outputs stable 10-minute fragments to prevent VRAM spikes.
2. **Transcription Layer (`transcriber.py`):** Directs media packets into local or cloud API nodes based on target dialect profiles. Handles custom sub-chunking rules down to 25-second windows where hardware or external constraints apply.
3. **Intelligence Layer (`summarize.py` & `extractor.py`):** Chains prompt patterns sequentially using **LangChain Expression Language (LCEL)** to extract atomic deliverables.
4. **Knowledge Isolation Layer (`vector_store.py` & `rag_engine.py`):** Batches processed transcripts into dense semantic vector graphs using `all-MiniLM-L6-v2` local transformers inside ChromaDB collections.

---

## 📂 Repository Structure

```text
├── app.py                      # Reactive Streamlit Interface
├── main.py                     # Central Core Pipeline Coordinator
├── requirements.txt            # Package Dependency Registry
├── .env.example                # Protected Environment Settings template
├── core/
│   ├── transcriber.py          # Dual Speech-to-Text Execution Routing
│   ├── summarize.py            # LangChain Map-Reduce Summarizer Chains
│   ├── extractor.py            # LCEL Information Structure extractors
│   └── rag_engine.py           # Top-K Semantic Retrieval and LLM QA Engine
└── utils/
    └── audio_processor.py      # yt-dlp, pydub, Mono/16kHz Optimization