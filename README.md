# 🔐 Confidentiality-Aware RAG System

A secure Retrieval-Augmented Generation (RAG) system that combines user authentication, Role-Based Access Control (RBAC), confidentiality-aware document retrieval, vector search, and a local Large Language Model.

The system ensures that users can retrieve and generate answers only from documents they are authorized to access.

---

## 🚀 Features

- User authentication using username and password
- Password hashing for secure credential storage
- Role-Based Access Control (RBAC)
- Four confidentiality levels
- Semantic document retrieval using embeddings
- ChromaDB vector database
- Confidentiality filtering before LLM generation
- Local LLM inference using Ollama
- Streamlit web interface
- Source transparency through authorized retrieved documents

---

## 🔐 Access Control

The system supports four user roles and four confidentiality levels.

| Role | Public | Internal | Confidential | Highly Confidential |
|------|:------:|:--------:|:------------:|:-------------------:|
| Viewer | ✅ | ❌ | ❌ | ❌ |
| Staff | ✅ | ✅ | ❌ | ❌ |
| Senior | ✅ | ✅ | ✅ | ❌ |
| Executive | ✅ | ✅ | ✅ | ✅ |

---

## 👥 Demo Users

| Username | Password | Role |
|---|---|---|
| viewer | viewer123 | Viewer |
| staff | staff123 | Staff |
| senior | senior123 | Senior |
| executive | executive123 | Executive |

---

## 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │   User Query    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Authentication  │
                    │    (SQLite)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   User Role     │
                    │ Viewer / Staff  │
                    │ Senior / Exec   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      RBAC       │
                    │ Authorization   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Query Embedding │
                    │ SentenceTransformer
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ChromaDB     │
                    │ Vector Retrieval│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Confidentiality │
                    │    Filtering    │
                    └────────┬────────┘
                             │
                 Unauthorized documents
                       are removed
                             │
                             ▼
                    ┌─────────────────┐
                    │ Authorized RAG  │
                    │     Context     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Local LLM       │
                    │ Ollama Llama 3.2│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Secure Answer  │
                    └─────────────────┘