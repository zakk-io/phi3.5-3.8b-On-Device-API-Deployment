**Author: Mohamed Zakaria**

**Date:**

**Repository:**

---

# 1. Hardware Specifications

**CPU:** 12th Gen Intel(R) Core(TM) i7-1255U (x86_64)

**RAM:** 16 GB installed, 9.2 GB available during testing

**Storage:** NVMe SSD (Samsung MZVL4512HBLU), 174 GB free

**OS:** Ubuntu 24.04.2 LTS

---

# 2. Phase 1 — Model Selection & Justification

## 2.1 Selected Model

**Model Name: phi3.5:3.8b**

**Model Family: phi3.5**

**Parameter Size: 3.82B**

**License: MIT License**

## 2.2 Why This Model Is Suitable for Edge Deployment

- Maintains acceptable accuracy under **Q8** and **Q4** quantization.
- Runs efficiently on CPU-only without GPU dependency.

## 2.3 Known Weaknesses

- May produce **hallucinated facts** under complex queries.
- Limited context window compared to larger LLMs.

---

# 3. Phase 2 — Quantization & Benchmarking

## 3.1 Quantization Strategies Tested

- **8-bit:** `phi3.5:3.8b-mini-instruct-q8_0` – pre-quantized 8-bit weights
- **4-bit:** `phi3.5:3.8b-mini-instruct-q4_K_M` – pre-quantized 4-bit weights
- **2-bit: `phi3.5:3.8b-mini-instruct-q2_K`** – pre-quantized 2-bit weights

**Tools Used:** Ollama runtime 

## **3.2 Benchmark Methodology**

### **3.2.1 Disk Size**

**Command**

```bash
ollama list
```

**Explanation**

`ollama list` command lists all locally installed Ollama model details:

The **SIZE** column shows how much disk space each quantized variant uses. 

![Screenshot from 2026-02-18 15-56-59.png](attachment:76fcca43-c48e-4e59-b270-cf98402dcc9b:Screenshot_from_2026-02-18_15-56-59.png)

### **3.2.2 Tokens per Second**

**Command** 

```bash
ollama run phi3.5:3.8b-mini-instruct-q8_0 "quantum mechanics in simple terms." --verbose
```

**Explanation**

Runs the model with `--verbose` to show performance metrics, including the **evaluation rate (tokens generated per second)** — e.g., `4.98 tokens/s` 

![Screenshot from 2026-02-18 16-05-42.png](attachment:5446ee10-3380-4048-aebb-a9e551c26aba:Screenshot_from_2026-02-18_16-05-42.png)

For more accurate benchmarking, run the command **three times or more** and calculate the average tokens/sec.

### **3.2.3 200-Token Latency**

**formula** 

```latex
 200 ÷ Tokens/sec = 200-Token Latency 
```

**Explanation**

`200 ÷ 4.98 = 40.16 sec`

which means model needs `40.16 second` to generate `200 tokens`

### **3.2.4 Peak RAM Usage**

**Commands**

```bash
ollama run phi3.5:3.8b-mini-instruct-q8_0
```

In another terminal:

```bash
python3 -c "print('benchmark ' * 4000)"
```

**Explanation**

It generates a massive block of text (repeating "benchmark" 4,000 times) to instantly fill the model's memory for the stress test.

In another terminal:

```bash
htop
```

**Explanation**

`htop` shows live RAM usage per process.

**RES** (Resident) column for the `ollama` process represents the RAM currently occupied by the model.

![Screenshot from 2026-02-18 17-06-03.png](attachment:fd80ec61-c5e9-42e6-9547-baaa49c03e95:Screenshot_from_2026-02-18_17-06-03.png)

### Benchmark Table

| Quant Level | Disk Size | Peak RAM | Tokens/sec | 200-token Latency | Quality Notes |
| --- | --- | --- | --- | --- | --- |
| Q8 | 4.1 GB | 5.526 GB | 5.35 | 37.38 seconds | more accurate |
| Q4 | 2.4 GB | 3.937 GB | 7.66 | 26.10 seconds | Slightly lower accuracy |
| Q2 | 1.4 GB | 3 GB | 11.02 | 18.14 seconds | just pure hallucinations |

## 3.4 Qualitative output degradation

- Q8 produces more reliable responses but uses more RAM and disk space.
- Q4 is faster and uses less memory, but output quality slightly decreases.
- Q2**:** Very small and just pure hallucinations

---

# 4. Phase 3 — API Implementation

## 4.1 Architecture Overview

The **API** is built using **FastAPI (v0.129.0)** as the backend framework, **Ollama (v0.6.1)** for local large language model (LLM) inference, and **Python 3.12.3** as the core programming environment.

## 4.2 API Specification

### Endpoint: POST `/generate`

**200 OK**

**Request**

```json
curl --request POST \
  --url http://127.0.0.1:8000/generate \
  --header 'content-type: application/json' \
  --data '{"model": "phi3.5:3.8b-mini-instruct-q8_0","prompt": "hi"}'
```

**Response** **Body**

```json
{
  "model": "phi3.5:3.8b-mini-instruct-q8_0",
  "response": "Hello! How can I help you today?",
  "latency": 1.51,
  "tokens_per_second": 7.5
}
```

**400 Bad Request**

**Request**

```json
curl --request POST \
  --url http://127.0.0.1:8000/generate \
  --header 'content-type: application/json' \
  --data '{"model": "qwen3:1.7b","prompt": "hi"}'
```

**Response** **Body**

```bash
{
  "detail": {
    "status_code": 400,
    "error": "Model 'qwen3:1.7b' is not allowed"
  }
}
```

**400 Bad Request**

**Request Body**

```json
curl --request POST \
  --url http://127.0.0.1:8000/generate \
  --header 'content-type: application/json' \
  --data '{"model": "","prompt": "hi"}'
```

**Response** **Body**

```bash
{
  "detail": {
    "status_code": 400,
    "error": "model cannot be empty"
  }
}
```

---

## 5. Analysis

- **What is the smallest usable quantization?**

     Q4 is the **smallest usable quantization**

- **When does output quality become unacceptable?**

      Q2 showing just pure hallucinations

- **What is the best quality-to-memory ratio?**

      Q4 gives a good balance, using ~3.9 GB RAM while keeping responses accurate.

- **Would you ship this model to a real device? Why or why not?**

      Q4 is fine for edge deployment.