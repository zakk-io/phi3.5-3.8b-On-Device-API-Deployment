# Phi-3.5 On-Device API Deployment

This repository provides a production-ready FastAPI wrapper for deploying quantized **Phi-3.5 (3.8B)** models on edge devices using **Ollama**. It includes comprehensive benchmarking for various quantization levels (Q2, Q4, Q8) to help you choose the best performance-to-quality ratio for your hardware.

## 🚀 Features

- **FastAPI Backend:** High-performance asynchronous API.
- **Quantization Support:** Optimized for Q8, Q4, and Q2 variants.
- **Edge Optimized:** Designed to run efficiently on CPU-only environments.

## 📊 Benchmarking Summary

Based on testing on a **12th Gen Intel i7-1255U (16GB RAM)**, here is the performance breakdown:

| Quant Level | Disk Size | Peak RAM | Tokens/sec | 200-token Latency | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q8** | 4.1 GB | 5.53 GB | 5.35 | 37.38s | High accuracy, high resource |
| **Q4** | 2.4 GB | 3.94 GB | 7.66 | 26.10s | **Best Balance (Recommended)** |
| **Q2** | 1.4 GB | 3.00 GB | 11.02 | 18.14s | Fast but high hallucination |

## 🛠️ Prerequisites

1. **Ollama:** Install from [ollama.com](https://ollama.com).
2. **Python 3.12+**
3. **Required Models:**
   ```bash
   ollama pull phi3.5:3.8b-mini-instruct-q8_0
   ollama pull phi3.5:3.8b-mini-instruct-q4_K_M
   ollama pull phi3.5:3.8b-mini-instruct-q2_K
   ```

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zakk-io/phi3.5-3.8b-On-Device-API-Deployment.git
   cd phi3.5-3.8b-On-Device-API-Deployment/
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

## 🏃 Running the API

Start the server:

```bash
fastapi dev app.py
```
The API will be available at `http://127.0.0.1:8000`.

## API Specification

### Generate Response
**Endpoint:** `POST /generate`


**Example Curl:**
```bash
curl --request POST 
  --url http://127.0.0.1:8000/generate 
  --header 'content-type: application/json' 
  --data '{"model": "phi3.5:3.8b-mini-instruct-q4_K_M","prompt": "hi"}'
```

**Successful Response:**
```json
{
  "model": "phi3.5:3.8b-mini-instruct-q4_K_M",
  "response": "Hello! How can I help you today?",
  "latency": 1.51,
  "tokens_per_second": 7.5
}
```

## ⚠️ Allowed Models
The API restricts usage to the following verified quantized versions:
- `phi3.5:3.8b-mini-instruct-q8_0`
- `phi3.5:3.8b-mini-instruct-q4_K_M`
- `phi3.5:3.8b-mini-instruct-q2_K`


