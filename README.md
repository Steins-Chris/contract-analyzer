
# Contract Analysis & Risk Assessment Bot

## Problem Statement
Build a GenAI-powered legal assistant for SMEs to analyze contracts, identify risks, and provide actionable advice.

## Features
- Contract Type Classification
- Clause & Sub-Clause Extraction
- Named Entity Recognition (Parties, Dates, Amounts, Jurisdiction)
- Risk & Compliance Detection
- Ambiguity Detection & Flagging
- Risk Scoring (Low/Medium/High)
- Plain-language explanations
- PDF export capability

## Tech Stack
- Python 3.9+
- Streamlit (UI)
- spaCy (NLP)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- OpenAI GPT-4 (optional for advanced analysis)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/contract-analyzer.git
cd contract-analyzer
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open browser at `http://localhost:8501`

3. Upload a contract (PDF, DOCX, or TXT)

4. Explore analysis across different tabs

## Supported File Formats
- PDF (text-based)
- DOCX
- TXT

## Languages
- English
- Hindi (basic support)

## Author
Built for Career Carnival Hackathon 2026 - Data Science
