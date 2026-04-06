# EthosAI: Autonomous Governance & Research Suite

## Overview

This application hosts a specialized Multi-Agent simulation designed to audit proposed AI architectures against internal business rules and wide industry regulations (like the EU AI Act or NIST AI Risk Management Framework). It showcases the combination of **CrewAI Agentic Orchestration** with local **Retrieval-Augmented Generation (RAG)**.

## Architecture

This system avoids the "Lost in the Middle" contextual limitations of giant single-prompt LLMs by breaking the evaluation process down chronologically across three specialized agent personas.

### The CrewAI Agents
- **Lead AI Compliance Researcher**: Equipped with dual-tooling. 
  1. `Local Policy DB Search`: Pulls local private Chroma embeddings chunks.
  2. `Serper API`: Fetches live web resources regarding up-to-the-minute global AI compliance modifications.
- **Senior AI Risk Analyst**: Consumes the raw research regulations and critically scrutinizes the provided engineering architectural outline to identify legal loopholes or vulnerabilities.
- **Governance Report Writer**: Responsible strictly for formatting. It distills complex legal liability arguments into cleanly structured executive Markdown briefings.

### Local RAG Pipeline 
To prevent enterprise PII or confidential company architecture from leaking, the vector store (`rag_pipeline.py`) relies entirely on local **Sentence-Transformer embeddings (`all-MiniLM-L6-v2`)**, storing semantic document chunks in **ChromaDB**.

## How to Run

1. Navigate to the folder. Dependencies are managed via the `uv` tool environment:
   ```bash
   cd EthosAI
   uv sync  # (or install dependencies if not loaded)
   ```
2. Prime the compliance Vector Database. Place your compliance PDFs into the `/docs/` folder, then run:
   ```bash
   uv run python rag_pipeline.py
   ```
3. Pass in your execution environment API configurations for the LLMs and Web Scraper:
   ```bash
   export OPENAI_API_KEY="sk-..."
   export SERPER_API_KEY="your-serper-key"
   ```
4. Start the interactive evaluator UI:
   ```bash
   uv run streamlit run app.py
   ```

*Upon execution, the system will output a compiled evaluation report titled `final_governance_report.md` capturing the Agents' coordinated evaluation.*
