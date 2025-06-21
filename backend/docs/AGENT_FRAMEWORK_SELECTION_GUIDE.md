# Agent Framework Selection Guide (June 2025)

## Introduction

This comprehensive guide helps you choose the right AI agent framework from the full spectrum of available options - it is structured in three main sections to help you quickly find what you need:

1. **High-Level Framework Selection Guide**: User group-based recommendations that provide shortlists of frameworks based on your organizational needs, technical constraints, and deployment preferences
2. **Best-Fit Snapshots**: Quick one-line summaries for each framework to help you identify the most promising options without reading the detailed analysis
3. **Detailed Framework Analysis**: In-depth evaluation of each framework using a 12-lens evaluation framework for comprehensive comparison

### High-Level Framework Selection Guide

This guide organizes frameworks into four distinct categories based on your organizational needs and technical approach:

**Visual Low-Code Builders** (Flowise AI, Dify, n8n) are ideal for companies or enterprises interested in enabling most of their employees to manage agents themselves. These platforms provide intuitive drag-and-drop interfaces that make AI agent development accessible to non-technical users, while still offering enterprise-grade capabilities and extensive integration options. They excel at rapid prototyping and bridging business process automation with AI capabilities.

**Cloud Ecosystem Integration** frameworks are purpose-built for organizations already invested in major cloud platforms. **Google Vertex AI Agent Builder** serves Google Cloud-centric companies, while **AutoGen** provides enterprise-ready multi-agent capabilities with deep Microsoft Azure integration and flexible deployment options across cloud environments.

**LLM-Agnostic Frameworks** (CrewAI, LangChain/LangGraph, PydanticAI, Agnos AI) are perfect for organizations wanting complete independence from any single LLM provider. These frameworks offer maximum flexibility to switch between models and vendors, protecting against vendor lock-in while providing extensive customization options for complex agent workflows. They prioritize developer control, type safety, and architectural flexibility over vendor-specific optimizations.

**TypeScript-Native Development** (Mastra) serves as the go-to framework for teams building AI agents with TypeScript backends. While many frameworks offer TypeScript support, most prioritize Python with TypeScript as secondary - often through community-maintained libraries or third-party ports that may lack feature parity or maintenance consistency. Other frameworks like LangChain provide official dual-language support but require managing separate codebases and SDKs. Mastra offers a TypeScript-first approach with native MCP integration, type-safe tool definitions, and seamless integration with the broader JavaScript/Node.js ecosystem.

**Developer-Focused Vendor-Based Solutions** (OpenAI Agents SDK, Mistral Agents API, Anthropic Claude Agents) serve teams wanting cutting-edge capabilities optimized for specific LLM providers. While these frameworks may offer some multi-provider support, they are fundamentally designed around their primary vendor's models and capabilities. They provide the fastest path to production with vendor-specific features but may limit long-term flexibility compared to truly agnostic alternatives.

---

## Best-fit Snapshots

**Google Vertex AI Agent Builder (+ A2A)**: Enterprises already using Google Cloud Infrastructure

**OpenAI Agents SDK**: Lightweight and will get major updates soon. Fast inmplementation.

**CrewAI**: Widely used open source framework favoring slim and easy code & plugin ecosystem

**LangChain / LangGraph**: Extensive ecosystem but quite heavy; Suitable for huge integrations

**AutoGen**: Enterprise-ready multi-agent framework with strong Microsoft ecosystem integration and flexible deployment options

**PydanticAI**: Type-safe Python agent framework with automatic schema validation and comprehensive LLM provider support

**Mistral Agents API**: EU-focused managed agent service with strong privacy positioning and first-class MCP integration

**Anthropic Claude Agents**: API-first agent platform with strong MCP integration, ideal for developers wanting Claude's reasoning capabilities without framework overhead

**Agnos AI**: Layered architecture for gradual complexity scaling with strong multimodal capabilities and extensive model provider support

**Mastra**: TypeScript-native framework with first-class MCP support, ideal for teams building AI agents with TypeScript backends

**Flowise AI**: Low-code visual agent builder with LangChain compatibility, ideal for rapid prototyping and non-technical users

**Dify**: Enterprise-ready visual workflow platform with extensive model provider support and marketplace ecosystem

**n8n**: Workflow automation platform with AI agent capabilities, ideal for business process automation with AI integration

---

## 12-Lens Evaluation Framework

### Framework Overview
- [Google Vertex AI Agent Builder (+ A2A)](#google-vertex-ai-agent-builder--a2a-enterprise-ga)
- [OpenAI Agents SDK](#openai-agents-sdk-116k-)
- [CrewAI](#crewai-331k-)
- [LangChain / LangGraph](#langchain--langgraph-110k--144k-)
- [AutoGen](#autogen-462k-)
- [PydanticAI](#pydanticai-40k-)
- [Mistral Agents API](#mistral-agents-api-early-access)
- [Anthropic Claude Agents](#anthropic-claude-agents-saas)
- [Agnos AI](#agnos-ai-285k-)
- [Mastra](#mastra-146k-)
- [Flowise AI](#flowise-ai-403k-)
- [Dify](#dify-104k-)
- [n8n](#n8n)

### Evaluation Criteria
- [Evaluation Lenses](#evaluation-lenses) - 12-lens evaluation framework

---

## Evaluation Lenses

| # | Dimension | Why it matters | Typical signals |
|---|-----------|---------------|-----------------|
| 1 | Programming model & primitives | Determines how quickly you can read, extend and test agent logic | Count/clarity of core concepts; boilerplate; multi‑language SDKs |
| 2 | Built-in orchestration features | Impacts determinism, latency, cost | LLM‑planned vs code‑graph; workflow DSLs; break‑points |
| 3 | Model agnosticism | Freedom to switch LLM vendors | Native adapters (LiteLLM, vLLM…); model registry; local model hooks |
| 4 | Inter‑agent protocol support | Enables cross‑framework agent collaboration | A2A, HTTP JSON, SSE, etc. |
| 5 | MCP support | Enables standardized tool/context protocol integration | Native toolbox; plug‑in architecture; default discovery |
| 6 | Tool / data connectors | Real‑world agents need actions & context | Pre‑built tools, plugin ecosystem, RAG helpers |
| 7 | Guardrails — response‑format safety | Keeps outputs structured & machine‑parsable | Schema‑first APIs; auto‑JSON mode; function calling helpers |
| 8 | Enterprise safety & compliance | Required for regulated workloads | Content filters; IAM / VPC‑SC; policy engines; data residency |
| 9 | Memory & state management | Sustains context across long tasks | Built‑in stores vs BYO Redis/VectorDB; export options |
|10 | Observability & evaluation | Debugging and prod health | Built‑in tracing; OTLP export; connectors (LangSmith, Langfuse, …) |
|11 | Deployment & scaling model | Dev‑ops burden & infra freedom | Managed runtime vs DIY; serverless autoscale; on‑prem portability |
|12 | Multimodal I/O | Voice/vision/video UX potential | Native STT/TTS; vision in/out; video streaming/generation |

---

## Google Vertex AI Agent Builder (+ A2A) (Enterprise GA)

### 1. Programming model & primitives
`Agent`, `Tool`, `Guardrail`, `Workflow` (Python ADK)

### 2. Built-in orchestration features
**Workflow Agents**: `SequentialAgent`, `ParallelAgent`, `LoopAgent`; **LLMAgent** for dynamic routing; **CustomAgent** template; A2A message bus for cross-vendor teams

### 3. Model agnosticism
Any Vertex Model Garden model (Gemini, Claude, Mistral, etc.)

### 4. Inter‑agent protocol support
**A2A** (JSON‑RPC over HTTP/SSE)

### 5. MCP support
**Yes** (native ADK toolbox)

### 6. Tool / data connectors
100+ Google connectors (BigQuery, Apigee, etc.)

### 7. Guardrails — response‑format safety
Declarative schemas + deterministic guards

### 8. Enterprise safety & compliance
Gemini filters, VPC‑SC, CMEK, IAM

### 9. Memory & state management
Short‑ & long‑term stores managed by Agent Engine (exportable, backend fixed)

### 10. Observability & evaluation
Streams to Cloud Trace/Logging; OTLP; manual LangSmith via OTLP

### 11. Deployment & scaling model
Fully‑managed serverless Agent Engine

### 12. Multimodal I/O
Bidirectional audio + video; images

---

## OpenAI Agents SDK (11.6k ★)

### 1. Programming model & primitives
`Agent`, `function_tool`, `Handoff`, `Guardrail`

### 2. Built-in orchestration features
Planner → Executor loop, `handoffs`, agents-as-tools pattern; code-orchestrated or LLM-planned flows

### 3. Model agnosticism
OpenAI + 100+ vendors via LiteLLM adapter

### 4. Inter‑agent protocol support
None (handoff inside process / HTTP you write)

### 5. MCP support
**Yes** (built‑in, or via `openai‑agents‑mcp` plug‑in)

### 6. Tool / data connectors
Bundled web/file/computer tools; any Python fn

### 7. Guardrails — response‑format safety
Pydantic schemas on every tool/agent

### 8. Enterprise safety & compliance
Self‑managed; optional abuse monitor

### 9. Memory & state management
BYO store (Redis, Postgres, Zep…)

### 10. Observability & evaluation
Built‑in tracing UI + OTLP exporter; Langfuse & LangSmith guides

### 11. Deployment & scaling model
Anywhere Python runs (local → FaaS)

### 12. Multimodal I/O
Voice helper; images; no video gen

---

## CrewAI (33.1k ★)

### 1. Programming model & primitives
`Agent`, `Task`, `Crew`, `Flow`

### 2. Built-in orchestration features
**Processes**: `sequential`, `hierarchical`; **Flows**: event-driven state machine with conditional branches

### 3. Model agnosticism
LiteLLM native; Ollama/local REST supported

### 4. Inter‑agent protocol support
Optional A2A transport

### 5. MCP support
**Yes** (default tool discovery)

### 6. Tool / data connectors
Community & enterprise connector packs

### 7. Guardrails — response‑format safety
Task‑level guardrails; Portkey option

### 8. Enterprise safety & compliance
BYO network & policy; Portkey redaction

### 9. Memory & state management
Defaults: ChromaDB + SQLite; customizable via env vars / storage classes

### 10. Observability & evaluation
First‑class hooks for Langfuse, AgentOps, Arize; LangSmith via LangChain

### 11. Deployment & scaling model
pip‑install; no managed runtime yet

### 12. Multimodal I/O
STT native, TTS beta; images; DIY video

---

## LangChain / LangGraph (110k ★ / 14.4k ★)

### 1. Programming model & primitives
Agent, Tool, StateGraph (or higher-level create_react_agent helpers) and typed State objects. These let you assemble node-and-edge graphs while still re-using LangChain's tool & prompt abstractions.

### 2. Built-in orchestration features
Graphs are explicit and state-aware: you define nodes, transitions and (optional) human-in-the-loop or validation hooks. Pre-built workflows (e.g., multi-agent collaboration) sit on the same engine, and every run can stream intermediate events.

### 3. Model agnosticism
LangChain ships a LiteLLM adapter (langchain-litellm) that transparently routes calls to >100 providers (Anthropic, Azure, Mistral, local vLLM, etc.). You can also plug any custom ChatModel or REST endpoint.

### 4. Inter‑agent protocol support
LangGraph can speak A2A (official sample in Google's A2A repo) and has first-party MCP adapters (langchain-mcp-adapters) so one agent can invoke tools hosted on any MCP-compatible server.

### 5. MCP support
**Yes** (first-party MCP adapters via langchain-mcp-adapters)

### 6. Tool / data connectors
Hundreds of ready-made tool integrations (search, SQL, Python REPL, web-scrape, OpenWeather, etc.) across both Python & JS — browseable in the LangChain integrations directory.

### 7. Guardrails — response‑format safety
Pydantic schemas can be attached to agents or individual nodes; post-model hooks allow automatic validation or correction. Community add-ons like Portkey Guardrails plug in for PII redaction, hallucination-checks, and schema enforcement.

### 8. Enterprise safety & compliance
No built-in perimeter; you choose the hosting environment and may layer Guardrails AI, Portkey, or cloud-native filters (e.g., AWS Bedrock Guardrails) on top.

### 9. Memory & state management
Short-term "thread" state is persisted automatically through checkpointers; long-term memories are JSON docs stored in the platform's backing store. You can swap in your own saver (SQLite, vector DB, S3, etc.) or keep it purely in-memory for prototypes.

### 10. Observability & evaluation
One-line tracing to LangSmith (first-party), with full OpenTelemetry export, plus plug-ins for Langfuse, Arize, AgentOps, etc. Studio can replay any LangSmith trace inside a graph debugger.

### 11. Deployment & scaling model
Options range from pip install && uvicorn on your laptop to the fully-managed LangGraph Platform (GA May 2025), or self-hosted data/control planes for regulated workloads; a free "Standalone Container (Lite)" tier exists for <1 M node-execs / yr.

### 12. Multimodal I/O
Native event streaming; STT/TTS and vision handled through plug-in tools (e.g., Google Speech-to-Text, Text-to-Speech, image loaders). No first-party video generator, but audio + incremental token streaming are first-class.

---

## AutoGen (46.2k ★)

### 1. Programming model & primitives
`ConversableAgent`, `AssistantAgent`, `UserProxyAgent` as the building blocks; teams like `TwoAgentChat`, `GroupChat`, and graph‑aware `GraphFlow` live in *autogen‑agentchat*

### 2. Built-in orchestration features
Out‑of‑the‑box patterns include sequential / round‑robin chats, *selector* chats, swarms, and fully directed graphs via **GraphFlow**; each supports conditional branches, loops, and parallel edges

### 3. Model agnosticism
AutoGen‑core defines a generic model‑client protocol, and `autogen‑ext` ships clients for OpenAI, Azure OpenAI, Anthropic, Gemini, Mistral, Groq and local **vLLM**; you can add any REST endpoint

### 4. Inter‑agent protocol support
Native **A2A** transport for cross‑framework agent messaging, plus first‑class **MCP** adapters so agents can invoke remote MCP tools or expose their own

### 5. MCP support
**Yes** (`autogen‑ext[mcp]`, `McpToolAdapter`, `McpWorkbench`)

### 6. Tool / data connectors
Bundled helpers for code‑exec, web‑browse, shell, and vector & SQL stores (e.g., **ChromaVectorDB**, Azure AI Search). RAG cookbooks show drop‑in usage

### 7. Guardrails — response‑format safety
Any model call can specify `json_output=MyPydanticModel` for automatic validation; schema enforcement is baked in, with ongoing improvements for dataclass / Pydantic conversion

### 8. Enterprise safety & compliance
Relies on the underlying model provider's filters (e.g., Azure content moderation) and your infra; Azure AAD auth & content filters are documented, with observability guidelines for regulated workloads

### 9. Memory & state management
Short‑term dialogue state lives in runtime context; *Memory* module provides pluggable stores (JSON, vector DB, custom). RAG helpers show how to wire Chroma or Azure Cognitive Search

### 10. Observability & evaluation
Native **OpenTelemetry** tracing with one‑liner setup; integrations for Arize Phoenix, Langfuse, OpenLit, and others stream spans to any OTLP backend

### 11. Deployment & scaling model
Run embedded (`SingleThreadedAgentRuntime`), spin multiple runtimes in‑process, or go distributed (Kubernetes/Fargate). *AutoGen Studio* offers a low‑code GUI, and guides cover Cloud Run & Fargate deployment

### 12. Multimodal I/O
Voice agents via STT/TTS recipes, *MultimodalAgent* for GPT‑4V and vision models, and **VideoSurfer** agent for video comprehension; community demos cover full text‑to‑video pipelines

---

## PydanticAI (4.0k ★)

### 1. Programming model & primitives
Central `Agent` class wraps model, instructions, tools and state; agents are declared as standard Pydantic models, giving lint-time type-safety

### 2. Built-in orchestration features
Four escalating strategies: single-agent, delegated tools, programmatic hand-offs, and full **graph-based control flow** via an internal state-machine

### 3. Model agnosticism
Built-in provider layer exposes **30+ LLM back-ends** (OpenAI, Anthropic, Gemini, Mistral, DeepSeek, Ollama, etc.); you pick the provider class per agent or even per call

### 4. Inter‑agent protocol support
Native **MCP** client/server utilities (SSE, Streamable HTTP, stdio) released in v0.3; agents can both consume remote MCP tools and publish their own

### 5. MCP support
**Yes** (native MCP client/server utilities with SSE, HTTP, and stdio support)

### 6. Tool / data connectors
Library ships reference tools for RAG search, vector/SQL loaders, web scrape, code-exec, plus quick recipes for custom REST tools

### 7. Guardrails — response‑format safety
Because every agent I/O is a Pydantic model, JSON schema validation is automatic; "type-safe, schema-first" guarantee built-in

### 8. Enterprise safety & compliance
Framework is **self-host first**; you deploy where compliance demands (Docker, Cloud Run, K8s), inherit IAM & network controls from your platform

### 9. Memory & state management
Short-term chat history exposed via `message_history`; long-term storage pluggable (Postgres, Supabase, vector DB) and tracked in roadmap

### 10. Observability & evaluation
Built-in **OpenTelemetry** spans stream to Logfire by default, or any OTLP sink such as Weave, Langfuse, Phoenix and LangWatch via drop-in config

### 11. Deployment & scaling model
`pip install pydantic-ai` then run local, Docker, or serverless; tutorials cover OpenFaaS and Google Cloud Run for auto-scaling container ops

### 12. Multimodal I/O
Agents can invoke image, audio or arbitrary tool calls via structured tool definitions; sample notebooks show RAG on docs and image captioning pipelines

---

## Agnos AI (28.5k ★)

### 1. Programming model & primitives
`Agent`, `Tool`, `Team`, plus five **"Levels"** that culminate in deterministic `Workflow` classes (Level 5). These layers let you start small and grow into multi‑agent workflows without switching abstractions

### 2. Built-in orchestration features
Workflows are plain‑Python, stateful programs; they support loops, conditionals, parallel `async.gather()` edges, caching, and long‑running tasks with built‑in state

### 3. Model agnosticism
Agnos exposes a unified interface to **23+ model providers** (OpenAI, Anthropic, Gemini, Mistral, Groq, etc.) and its UAgI layer can swap models at runtime—no vendor lock‑in

### 4. Inter‑agent protocol support
Blog posts and docs show Agnos agents speaking Google's **A2A** in mixed stacks (LangChain, CrewAI)

### 5. MCP support
**Yes** (ships first‑class MCP adapters and libraries)

### 6. Tool / data connectors
100+ ready‑made tools (web search, SQL, vector DBs, image, audio, video, BigQuery, Azure AI Search) and ongoing additions via changelog (e.g., Couchbase, Milvus)

### 7. Guardrails — response‑format safety
Native **structured outputs** (`response_model=YourPydanticClass`) or `use_json_mode=True` injects schema prompts and validates the JSON on return

### 8. Enterprise safety & compliance
No built‑in VPC‑SC or IAM; you deploy Agnos where you need and rely on the model provider's filters, but the framework offers turnkey monitoring hooks

### 9. Memory & state management
Agents have built‑in session storage (SQLite/Postgres drivers), **User Memories**, and **Summaries**; you can swap any store via the `memory` or `storage` drivers for Redis, Chroma, etc.

### 10. Observability & evaluation
One‑line **OpenTelemetry** instrumentation; integrations for Langfuse, LangSmith, Arize, OpenInference, and OTLP sinks land in every release

### 11. Deployment & scaling model
Run in‑process, containerize with the **Agent API** FastAPI template (Docker Compose), or push to Cloud Run / Fargate / K8s; Postgres is the default prod store

### 12. Multimodal I/O
Agents natively accept and emit **text, image, audio, and video**; recent releases add Gemini video inputs and Groq audio toolkits

---

## Mastra (14.6k ★)

### 1. Programming model & primitives
`Agent`, `Tool`, `Workflow`, `Rag`, `Integration`, and `Eval` objects. Each is type-safe and includes built-in OpenTelemetry spans.

### 2. Built-in orchestration features
Workflows are **durable graph-based state machines** with branching, parallelism, suspends, retries, human-in-the-loop, and a forthcoming visual editor. Steps can embed other workflows or agents.

### 3. Model agnosticism
Uses the **Vercel AI SDK** for routing, giving a unified interface to GPT-4 o, Claude, Gemini, Mistral, Groq, Llama and any provider you point it at.

### 4. Inter‑agent protocol support
Ships an **MCP server package** (`@mastra/mcp-docs-server`) so agents can publish/consume tools across frameworks; no native A2A yet.

### 5. MCP support
**Yes** (native `MastraMCPClient` with both stdio and SSE transport support; first-class MCP registry integration with `MCPConfiguration`)

### 6. Tool / data connectors
Typed `Tool` factories with Zod-validated inputs; auto-generated integrations for dozens of SaaS APIs plus vector/SQL/RAG loaders.

### 7. Guardrails — response‑format safety
Input and output schemas are declared with **Zod**; every tool/step validates at runtime, returning descriptive errors on mismatch.

### 8. Enterprise safety & compliance
Completely self-hostable or deploy to **Mastra Cloud** / any serverless platform, inheriting IAM & network boundaries from your chosen infra.

### 9. Memory & state management
Built-in **Memory API** (default LibSQL + `fastembed-js`) for persistent threads, semantic recall, and cross-agent shared context; pluggable stores like Postgres, Supabase, or any vector DB.

### 10. Observability & evaluation
One-liner **OpenTelemetry** setup; official guides for Langfuse and Arize export. Each agent/tool/workflow step auto-traces.

### 11. Deployment & scaling model
`npm create mastra@latest` for local dev; deploy via **Mastra Cloud** (Git-based), or platform-specific deployers for Vercel, Cloudflare Workers, Netlify; atomic serverless snapshots with auto-scale.

### 12. Multimodal I/O
Unified **Voice** system: STT, TTS, and real-time speech-to-speech via providers like OpenAI and Deepgram; image generation handled as tools; can combine with RAG.

---

## Flowise AI (40.3k ★)

### 1. Programming model & primitives
Visual **Chatflow**, **Agentflow V2**, and **Assistant** builders; each node is a standalone LangChain‑compatible component that you wire up on the canvas

### 2. Built-in orchestration features
Drag‑and‑drop DAGs support sequential, parallel, conditional branches, loops and multi‑agent hierarchies (Agentflow V1/V2)

### 3. Model agnosticism
Out‑of‑the‑box connectors for >20 chat models (OpenAI, Anthropic, Mistral, Gemini, Ollama, Groq, Bedrock…), selectable per node; bring‑your‑own REST via Custom LLM node

### 4. Inter‑agent protocol support
A2A support is on the roadmap (GitHub issue #4283); native **MCP** tools & a "Custom MCP" node to talk to any MCP server

### 5. MCP support
**Yes** (native MCP tools & Custom MCP node)

### 6. Tool / data connectors
100+ nodes spanning Web search, Gmail, Google Sheets, shell, code‑exec, custom REST, plus vector/SQL doc loaders & RAG helpers

### 7. Guardrails — response‑format safety
Output‑parser nodes (JSON, XML, custom) enforce structured responses; moderation nodes hook to OpenAI or custom prompt filters

### 8. Enterprise safety & compliance
Self‑host anywhere (Docker, K8s, AWS, Azure, GCP); environment vars for DB, storage, SSO, rate limits; optional OpenAI moderation node

### 9. Memory & state management
Memory nodes (buffer, summary, Redis, Upstash, Zep, Mongo, DynamoDB…) plus global DB support (SQLite default, MySQL/Postgres/MariaDB)

### 10. Observability & evaluation
Toggle analytics providers (LangSmith, Langfuse, Arize Phoenix, Lunary, Opik) in settings; YouTube tutorials show trace replay inside LangSmith

### 11. Deployment & scaling model
`npm i -g flowise && flowise start` for local; official Docker images & Helm charts for prod; queue/worker pattern for horizontal scaling

### 12. Multimodal I/O
Image upload/vision prompts, STT via OpenAI/AssemblyAI/LocalAI, TTS beta, and audio uploads through the Prediction API

---

## Dify (104k ★)

### 1. Programming model & primitives
Visual **Chatflow / Workflow** canvas with drag-and-drop nodes; an **Agent** node encapsulates agent strategies, and low-code JSON prompt orchestration lives inside each node

### 2. Built-in orchestration features
Workflows are DAGs supporting sequential, parallel, conditional (`IF / ELSE`) branches, loops and (beta) multi-agent systems embedded inside the same canvas

### 3. Model agnosticism
Settings page lists **30+ model providers** (OpenAI, Anthropic, Gemini, Mistral, Groq, Ollama, Replicate, Bedrock, etc.); you can switch providers per LLM node

### 4. Inter‑agent protocol support
A plug-in turns any Dify app into an **MCP-compliant server**, so external agents can call its tools; no native A2A transport yet

### 5. MCP support
**Yes** (plug-in turns any Dify app into an MCP-compliant server)

### 6. Tool / data connectors
Marketplace hosts 100+ nodes (OpenAPI tools, DALL-E, web search, Gmail, SQL/vector loaders); advanced guides show adding custom REST tools in minutes

### 7. Guardrails — response‑format safety
Built-in **Structured Outputs** with a visual JSON-Schema editor enforce strict model output validation; released in v1.3.0

### 8. Enterprise safety & compliance
Fully **self-hostable** via Docker/K8s with environment-based secrets, or use **Dify Cloud** SaaS; you control data residency and IAM layers

### 9. Memory & state management
Supports 15+ vector stores (Qdrant, Weaviate, Milvus, Chroma, pgvector, etc.) and OceanBase by default; set via `VECTOR_STORE=` env var

### 10. Observability & evaluation
One-click integrations for **Langfuse**, **LangSmith** and other OTLP sinks capture traces, prompts and metrics for every run

### 11. Deployment & scaling model
`docker compose up` gets you local dev; official Docker Compose and Helm charts for prod; SaaS tiers range from Free Sandbox to Team

### 12. Multimodal I/O
Image generation nodes (DALL-E, Stable Diffusion), vision prompts, plus voice STT/TTS via **DupDub** and other marketplace audio plug-ins

---

## Mistral Agents API (Early-access)

### 1. Programming model & primitives
`Agent`, `Conversation`, and `Entry` objects; an Agent bundles model, instructions & a list of built-in or MCP tools, while Conversation + Entry track persistent, event-typed history

### 2. Built-in orchestration features
Server-side loop coordinates multi-step plans, with hand-offs (`server` vs `client` modes) and sequential/parallel workflows; advanced examples show swarms of agents collaborating via the Conversations API

### 3. Model agnosticism
**Vendor-locked** to Mistral models (`mistral-small`, `mistral-medium`, forthcoming `mistral-large-reasoning`) — a parity play with OpenAI Assistants rather than a bring-your-own-model SDK

### 4. Inter‑agent protocol support
First-class **MCP** support lets any Mistral agent call or expose external tools; include MCP servers inline in API calls. No formal A2A transport yet

### 5. MCP support
**Yes** (first-class MCP support; include MCP servers inline in API calls)

### 6. Tool / data connectors
Four built-ins today: `web_search`, `code_interpreter`, `image_generation`, and (beta) `document_library`; you can also register user-defined `function` tools or any MCP endpoint

### 7. Guardrails — response‑format safety
JSON-mode and **Structured Output** APIs enforce schema-aware outputs; custom structured formats are recommended for higher reliability

### 8. Enterprise safety & compliance
Data stored in the **EU by default** with optional US endpoint; GDPR-friendly, privacy-by-design positioning, plus moderation endpoints inherited from the Chat API

### 9. Memory & state management
Persistent memory across conversations is handled by the service; opt-out with `store=False` if you don't want server-side retention

### 10. Observability & evaluation
Dedicated **Observability guide** shows token/cost metrics, traces, and one-click LangSmith integration for full run replay

### 11. Deployment & scaling model
Fully-managed SaaS, but models can be **self-deployed** via vLLM/TensorRT/TGI for on-prem inference; Agents API itself is cloud-hosted

### 12. Multimodal I/O
Text and vision models plus built-in image generation tool; audio/video capabilities expected in roadmap but not GA

---

## Anthropic Claude Agents (SaaS)

### 1. Programming model & primitives
No separate SDK: you work with the plain **Messages API** (`model`, `messages[]`, `tools[]`) plus helper objects—`tool` definitions, **Files API** assets, and optional `mcp_servers`. Each request can spin up an "agent-like" loop that thinks, plans and calls tools

### 2. Built-in orchestration features
The loop runs **server-side**: Claude chooses a tool, calls it, gets results, and continues until a final answer. Examples show single agents as well as *swarms* that coordinate via multiple Conversations. Hand-off types (`server` vs `client`) let you keep control

### 3. Model agnosticism
**Vendor-locked**: only Claude models run here—Sonnet, Haiku, Opus, etc. There's no adapter to third-party LLMs

### 4. Inter‑agent protocol support
First-class **MCP connector**: pass a list of MCP servers and Claude will discover & invoke their tools; you can also expose your own via MCP. No A2A transport today

### 5. MCP support
**Yes** (first-class MCP connector with tool discovery)

### 6. Tool / data connectors
Built-ins: `web_search`, `code_execution`, `image_generation`, (beta) `document_library`; plus any **client tool** or remote MCP tool you define

### 7. Guardrails — response‑format safety
JSON-mode and the **"increase output consistency"** guide enforce schema-aware outputs; you supply a JSON Schema or XML template and Claude validates before returning

### 8. Enterprise safety & compliance
GDPR-aligned; privacy docs highlight DPA, SCCs, content-filtering refusals, and optional EU data residency via Bedrock or Vertex wrappers

### 9. Memory & state management
No user-visible vector store yet, but **extended prompt caching** keeps context for up to **1 hour**; Files API lets agents persist & reuse documents across sessions

### 10. Observability & evaluation
**OpenTelemetry** hooks built in (env vars) for metrics/logs; community recipes integrate LangSmith, Datadog LLM Observability

### 11. Deployment & scaling model
Fully-managed SaaS; you hit the HTTPS endpoint and Anthropic handles scaling. Models can be self-hosted via vLLM/TGI, but the **Agents logic lives in the cloud**

### 12. Multimodal I/O
Vision (image in), citations, PDF support, and built-in **image_generation** tool; audio/video not yet GA

---

## n8n

### 1. Programming model & primitives
Visual **Workflow** canvas with `AI Agent` node, `OpenAI Functions Agent` node, plus standard n8n nodes; each agent node wraps LangChain agents so you stay in drag-and-drop land

### 2. Built-in orchestration features
Workflows are DAGs that support sequential, parallel, conditional, and loop branches; you can mix AI Agent nodes with any other node for complex flows

### 3. Model agnosticism
Because nodes use LangChain under the hood, you can select OpenAI, Anthropic, Mistral, Groq, Ollama or provide a **Custom LLM** sub-node; community docs show custom Cloudflare model wiring

### 4. Inter‑agent protocol support
No native **A2A** or **MCP** transport yet; agents communicate inside the same workflow only (HTTP/Webhook hand-offs possible via nodes)

### 5. MCP support
**No** (no native A2A or MCP transport yet)

### 6. Tool / data connectors
400+ built-in integrations and 422+ AI Agent-compatible tools; any n8n node can serve as an external tool for the AI Agent

### 7. Guardrails — response‑format safety
`Tools Agent` node implements LangChain's tool-calling interface with improved output parsing, so JSON schema validation happens automatically

### 8. Enterprise safety & compliance
Entirely self-hostable (Docker, K8s) or n8n Cloud; you control data residency and can layer IAM, SSO, or VPC on top

### 9. Memory & state management
Dedicated Memory nodes (Simple, Redis, Postgres, Zep, etc.) let each AI Agent persist chat context; Chat Memory Manager handles load/insert/delete for vector stores

### 10. Observability & evaluation
One-click **LangSmith** tracing for self-hosted installs; community recipes integrate Langfuse and Opik via custom images or environment variables

### 11. Deployment & scaling model
Run locally, self-host via Docker Compose, Kubernetes or use n8n Cloud; **Queue mode** with Redis enables horizontal scaling and concurrent executions

### 12. Multimodal I/O
Image generation & GPT-4 Vision via OpenAI node, audio STT/Translate via Whisper operations, and you can route files, SMS/MMS or WhatsApp through Twilio
