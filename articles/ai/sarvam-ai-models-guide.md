# Sarvam AI Models: A Comprehensive Guide to India's Sovereign AI Stack

**Date:** July 15, 2026

## Introduction

Sarvam AI is building India's sovereign AI infrastructure — a full-stack platform of models purpose-built for the country's 22 official languages. Unlike general-purpose models from OpenAI or Google that bolt on multilingual support as an afterthought, Sarvam's models are trained from the ground up on Indian language data, Indian accents, code-mixed speech (like Hinglish), and Indic scripts.

The result is a suite of models that covers the complete AI pipeline: text generation, speech recognition, speech synthesis, translation, and visual document understanding. This article breaks down each model, what you need to run it, and where it fits in real-world applications.

---

## The Model Suite

Sarvam AI's current lineup consists of six core models:

| Model | Type | Parameters | Languages | Availability |
|:---|:---|:---|:---|:---|
| **Sarvam-105B** | LLM (MoE) | 105B total / ~10.3B active | 22 Indian + English | Open weights |
| **Sarvam-30B** | LLM (MoE) | 30B total / ~2.4B active | 22 Indian + English | Open weights |
| **Saaras V3** | Speech-to-Text (ASR) | Undisclosed | 22 Indian + English | API only |
| **Bulbul V3** | Text-to-Speech (TTS) | Undisclosed | 11 Indian languages | API only |
| **Sarvam Vision** | Vision-Language (OCR) | 3B | 22+ Indian languages | API only |
| **Sarvam Translate** | Translation | Undisclosed | 22 Indian languages | Open weights |

> **Note:** Sarvam-M (24B) was an earlier intermediate release and is now considered a legacy model.

---

## Architecture: Why Mixture-of-Experts Matters

Both Sarvam-105B and Sarvam-30B use a **Mixture-of-Experts (MoE)** architecture. This is the key detail that makes their hardware requirements manageable.

In a dense model (like LLaMA 70B), every parameter activates on every token. In a MoE model, only a subset of "expert" layers fire per token — the rest stay dormant.

**What this means for you:**

- **Sarvam-105B** has 105B total parameters but only ~10.3B activate per token
- **Sarvam-30B** has 30B total parameters but only ~2.4B activate per token

The practical impact: you get the reasoning quality of a large model with the inference speed and memory footprint of a much smaller one. However, you still need enough VRAM to *load* all the weights — the savings come from compute, not storage.

---

## Hardware Requirements

### Sarvam-105B — Flagship LLM

The flagship model for complex reasoning, agentic workflows, and long-form analysis.

| Deployment Tier | Hardware | VRAM | Notes |
|:---|:---|:---|:---|
| **Production (recommended)** | 4× NVIDIA A100/H100 (80 GB) | 320 GB total | Full FP16, long context (128K tokens) |
| **Production (high-throughput)** | 8× NVIDIA H100 (80 GB) | 640 GB total | Maximum throughput, tensor parallelism=8 |
| **Cost-optimized** | 4× NVIDIA A100 (80 GB) + FP8 quantization | 320 GB total | ~30% memory reduction with FP8 weights |
| **NVFP4 quantized** | 2× NVIDIA H100 (80 GB) | 160 GB total | Reduced precision, good for lower-latency use cases |

**vLLM deployment example:**

```bash
vllm serve "sarvamai/sarvam-105b" \
  --tensor-parallel-size 4 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.92 \
  --enable-chunked-prefill \
  --trust-remote-code
```

**Key points:**
- Requires vLLM 0.6.5+ for proper MoE routing support
- Context window up to 128K tokens (adjust `--max-model-len` based on your VRAM budget)
- FP8 quantized weights are available on Hugging Face and are recommended for self-hosting

---

### Sarvam-30B — Conversational Agent LLM

Optimized for real-time conversational agents and instruction following.

| Deployment Tier | Hardware | VRAM | Notes |
|:---|:---|:---|:---|
| **Production** | 2× NVIDIA A100 (80 GB) | 160 GB total | Comfortable fit with tensor parallelism=2 |
| **High-throughput** | 4× NVIDIA A100/H100 (80 GB) | 320 GB total | Higher batch sizes and concurrency |
| **Experimentation** | 1× NVIDIA A100 (80 GB) or RTX 4090 (24 GB) + quantization | 24–80 GB | Tight fit; use 4-bit quantization on consumer GPUs |

**vLLM deployment example:**

```bash
vllm serve "sarvamai/sarvam-30b" \
  --tensor-parallel-size 2 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90 \
  --trust-remote-code
```

**Key points:**
- Context window up to 64K tokens
- Significantly more resource-friendly than the 105B variant
- Works well on smaller multi-GPU setups or high-end single-GPU configurations with quantization

---

### Saaras V3 — Speech-to-Text

Streaming and batch speech-to-text for 22 Indian languages.

| Aspect | Details |
|:---|:---|
| **Availability** | API only (via Sarvam platform) |
| **Self-hosting** | Not available for local deployment |
| **Latency** | Streaming mode with low-latency decoding |
| **Strengths** | Background noise handling, multi-accent support, code-mixed speech (e.g., Hinglish) |

**API usage (Python SDK):**

```python
from sarvamai import SarvamAI

client = SarvamAI(api_key="your-api-key")

response = client.speech.transcribe(
    file=open("audio.wav", "rb"),
    language="hi-IN",
    model="saaras-v3"
)
print(response.text)
```

---

### Bulbul V3 — Text-to-Speech

Natural, expressive speech synthesis for 11 Indian languages.

| Aspect | Details |
|:---|:---|
| **Availability** | API only (via Sarvam platform) |
| **Self-hosting** | Not available for local deployment |
| **Languages** | 11 Indian languages |
| **Features** | Customizable pitch, pace, and speaker tone; production-ready voice quality |

**API usage (Python SDK):**

```python
from sarvamai import SarvamAI

client = SarvamAI(api_key="your-api-key")

response = client.speech.synthesize(
    text="नमस्ते, आपका स्वागत है।",
    language="hi-IN",
    model="bulbul-v3"
)
# Save the audio output
with open("output.wav", "wb") as f:
    f.write(response.audio)
```

---

### Sarvam Vision — Document Intelligence

A 3B parameter vision-language model for OCR and document digitization.

| Aspect | Details |
|:---|:---|
| **Availability** | API only (via Sarvam platform) |
| **Self-hosting** | Not available for local deployment |
| **Model size** | 3B parameters |
| **Strengths** | Complex document layouts, handwritten text, Indic scripts across 22+ languages |

**API usage (Python SDK):**

```python
from sarvamai import SarvamAI

client = SarvamAI(api_key="your-api-key")

response = client.vision.extract(
    file=open("document.png", "rb"),
    language="ta-IN",  # Tamil
    model="sarvam-vision"
)
print(response.text)
```

---

### Sarvam Translate — Multilingual Translation

Open-weights model for long-form, context-aware translation.

| Aspect | Details |
|:---|:---|
| **Availability** | Open weights (Hugging Face) |
| **Languages** | 22 Indian languages (bidirectional) |
| **Strengths** | Long-form documents, context preservation, domain-specific terminology |
| **Self-hosting** | Possible via Hugging Face Transformers |

---

## Hardware Decision Matrix

Not sure what hardware to provision? Use this quick reference:

| Use Case | Recommended Model | Minimum Hardware | Monthly Cloud Cost (est.) |
|:---|:---|:---|:---|
| Internal enterprise chatbot | Sarvam-30B | 2× A100 80 GB | ~$4,000–$6,000 |
| Complex reasoning / agents | Sarvam-105B | 4× A100 80 GB | ~$8,000–$14,000 |
| Voice-first customer support | Saaras V3 + Bulbul V3 | API (no hardware) | Pay-per-use |
| Document digitization pipeline | Sarvam Vision | API (no hardware) | Pay-per-use |
| Multilingual content translation | Sarvam Translate | 1× GPU (16+ GB VRAM) | ~$500–$1,500 |
| Full sovereign AI stack | All models | 4–8× H100 80 GB + API | ~$15,000–$25,000 |

> **CPU-only inference:** While technically possible for the smaller models using GGUF/llama.cpp quantizations, CPU-only deployment is impractical for production workloads due to high latency. It may be suitable for local experimentation with the 30B model using 4-bit quantization on machines with 64+ GB RAM.

---

## Sample Use Cases

### 1. Multilingual Voice-First Customer Support Bot

**Problem:** An Indian e-commerce platform needs to handle customer queries in Hindi, Tamil, Telugu, and Bengali — via voice.

**Solution Stack:**
- **Saaras V3** → Transcribes the customer's voice query in their native language
- **Sarvam-30B** → Processes the query, retrieves order status, generates a response
- **Bulbul V3** → Converts the response back to natural-sounding speech

```
Customer speaks in Tamil
    → Saaras V3 (ASR): "என் ஆர்டர் எங்கே?"
    → Sarvam-30B (LLM): Looks up order, generates Tamil response
    → Bulbul V3 (TTS): Speaks response back in Tamil
```

**Why Sarvam over alternatives:** Global ASR models like Whisper struggle with Indian accents, code-mixed speech, and low-resource languages like Odia or Assamese. Sarvam's models are specifically trained on these patterns.

---

### 2. Government Document Digitization Pipeline

**Problem:** A state government needs to digitize thousands of handwritten land records in Kannada and Telugu scripts.

**Solution Stack:**
- **Sarvam Vision** → Extracts text from scanned documents including handwritten entries
- **Sarvam Translate** → Translates extracted content to Hindi/English for national-level indexing
- **Sarvam-30B** → Structures the extracted data into standardized database records

```python
from sarvamai import SarvamAI

client = SarvamAI(api_key="your-api-key")

# Step 1: Extract text from scanned land record
ocr_result = client.vision.extract(
    file=open("land_record_kannada.png", "rb"),
    language="kn-IN"
)

# Step 2: Translate to English for indexing
translation = client.translate.translate(
    text=ocr_result.text,
    source_language="kn-IN",
    target_language="en-IN"
)

# Step 3: Structure the data
structured = client.chat.completions.create(
    model="sarvam-30b",
    messages=[{
        "role": "user",
        "content": f"Extract owner name, survey number, area, and land type from: {translation.text}"
    }]
)
```

---

### 3. EdTech AI Tutor in Regional Languages

**Problem:** An online education platform wants to offer AI tutoring that speaks and understands students in their mother tongue.

**Solution Stack:**
- **Saaras V3** → Student asks a question by speaking in Marathi
- **Sarvam-105B** → Generates a detailed, pedagogically sound explanation
- **Bulbul V3** → Reads the explanation back to the student
- **Sarvam Vision** → Student can share a photo of a problem from their textbook

**Why Sarvam-105B here:** The flagship model's stronger reasoning capabilities produce better explanations for complex subjects like mathematics, science, and logic — areas where the 30B model may produce shallower answers.

---

### 4. Healthcare Triage Bot for Rural Clinics

**Problem:** Rural health workers with limited English fluency need an AI assistant that can help triage patients and document symptoms.

**Solution Stack:**
- **Saaras V3** → Health worker dictates patient symptoms in their dialect
- **Sarvam-30B** → Provides preliminary triage guidance based on symptom analysis
- **Sarvam Translate** → Translates the triage report to English for the supervising doctor
- **Bulbul V3** → Reads back instructions to the health worker

---

### 5. Media Localization and Video Dubbing

**Problem:** A content platform wants to dub Hindi-language video content into 10+ Indian languages for regional audiences.

**Solution Stack:**
- **Saaras V3** → Transcribes the original Hindi audio
- **Sarvam Translate** → Translates the transcript to the target language
- **Bulbul V3** → Generates dubbed audio in the target language with natural prosody

---

## Getting Started

### Option A: Use the Sarvam API (Quickest)

```bash
pip install sarvamai
```

```python
from sarvamai import SarvamAI

client = SarvamAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="sarvam-30b",
    messages=[{"role": "user", "content": "भारत की राजधानी क्या है?"}]
)
print(response.choices[0].message.content)
```

### Option B: Self-Host the LLMs (Full Control)

1. Download weights from [Hugging Face (sarvamai)](https://huggingface.co/sarvamai)
2. Install vLLM: `pip install vllm`
3. Launch the server:

```bash
vllm serve "sarvamai/sarvam-30b" \
  --tensor-parallel-size 2 \
  --max-model-len 8192 \
  --trust-remote-code
```

4. Query via OpenAI-compatible API:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sarvamai/sarvam-30b",
    "messages": [{"role": "user", "content": "Explain quantum computing in Hindi"}]
  }'
```

---

## Key Takeaways

1. **MoE architecture is the enabler.** Sarvam's flagship models punch above their weight class because only a fraction of parameters activate per token — giving you big-model quality at small-model speed.

2. **Self-hosting the LLMs is practical.** The 30B model fits on a 2-GPU setup; the 105B needs 4–8 GPUs. FP8 quantization is your friend.

3. **Speech and vision are API-only (for now).** Saaras, Bulbul, and Sarvam Vision are tightly optimized managed services. Use the API unless open-source alternatives (Whisper, etc.) meet your accuracy bar for Indian languages — they usually don't.

4. **The sweet spot is the full stack.** Sarvam's real moat isn't any single model — it's the integrated pipeline from voice input → understanding → generation → voice output, all natively in Indian languages.

5. **Cost scales with ambition.** A voice chatbot using APIs might cost a few hundred dollars/month. A fully sovereign, self-hosted stack with the 105B model runs $15–25K/month on cloud GPUs.

---

## References

- [Sarvam AI Official Platform](https://sarvam.ai)
- [Sarvam AI on Hugging Face](https://huggingface.co/sarvamai)
- [Sarvam AI Documentation](https://docs.sarvam.ai)
- [NVIDIA Partnership Announcement](https://nvidia.com)
- [AI Kosh Repository](https://github.com/sarvamai)
