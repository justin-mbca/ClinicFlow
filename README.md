# Clinical Text De-identification & Insight Extraction Pipeline

This project demonstrates a production-ready pipeline for de-identifying clinical notes and extracting medical entities using both Azure Cognitive Services and open-source NLP models. It is designed for healthcare AI/ML engineering interviews and portfolio demonstration.

## Project Architecture

**Flow 1: Azure Native Path**
- Raw Clinical Notes → (Databricks Preprocess) → Azure Cognitive Service for Health → Entity Extraction → Azure SQL DB

**Flow 2: Open-Source Path**
- Raw Clinical Notes → (Databricks Preprocess) → Hugging Face/spaCy Model → Entity Extraction & De-identification → Azure SQL DB

## Features
- Secure secret management with Azure Key Vault
- Batch processing and cost optimization
- PHI masking and entity extraction
- SNOMED CT mapping (stubbed)
- Results stored in Azure SQL Database

## How to Use
1. Clone this repo and set up your Azure resources (see `setup_azure_cli.sh`).
2. Fill in `config.yaml` with your Azure settings.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Databricks notebook or Python modules as needed.

## Portfolio/Resume Highlights
- Designed a secure, scalable clinical NLP pipeline on Azure
- Integrated both cloud-native and open-source NLP for healthcare
- Automated PHI de-identification and medical entity extraction
- Demonstrated robust, production-ready engineering practices

## Documentation
- See `PRODUCTION_NOTES.md` for scaling, monitoring, and trade-off analysis.
- See `Clinical_NLP_Pipeline_Prototype.ipynb` for a runnable prototype and workflow demonstration.
