# Agentic RAG-Based Customer Churn Intelligence and Retention System

## Project Overview
A software-based customer churn intelligence system combining machine learning, hybrid retrieval-augmented generation, and agentic AI.

## Core Modules
1. Customer Data Management
2. Customer Churn Prediction
3. Advanced Hybrid RAG
4. Customer Analysis Agent
5. Retention Strategy Agent
6. Verification Agent
7. Streamlit Dashboard

## Technology Stack
- Python 3.11
- Streamlit
- Scikit-learn
- Sentence Transformers
- ChromaDB
- BM25
- Nexus API (integration subject to API compatibility verification)

## Project Status
The existing Streamlit dashboard and agent workflow are integrated with
explicit ML, RAG, and Nexus extension interfaces. No teammate-owned prediction
or retrieval implementation, Nexus API documentation, or verified model ID is
currently present in the workspace. As a result, uploaded churn probabilities
can be displayed and passed through the workflow, but the application does not
run a model, retrieve real evidence, or call Nexus until those integrations are
provided. Retention generation is blocked when evidence is unavailable.

Run the app with `python -m streamlit run app.py` and the integration tests with
`python -m unittest discover -s tests -v`, using the project virtual
environment. Copy `.env.example` to `.env` and fill in Nexus values only from
verified provider documentation; do not commit `.env`.

The current verifier checks that each cited source exists and each supplied
quotation is an exact substring of its source. It does not establish semantic
entailment; human review remains required.
