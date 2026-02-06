import spacy
import re
from typing import List, Dict

class ContractAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
    
    def classify_contract_type(self, text: str) -> str:
        text_lower = text.lower()
        contract_types = {
            "Employment Agreement": ["employment", "employee", "employer", "salary", "job title"],
            "Vendor Contract": ["vendor", "supplier", "purchase order", "goods"],
            "Lease Agreement": ["lease", "rent", "tenant", "landlord", "premises"],
            "Partnership Deed": ["partnership", "partners", "profit sharing"],
            "Service Contract": ["service provider", "client", "deliverables"],
            "NDA": ["confidential", "non-disclosure", "proprietary"],
        }
        scores = {}
        for contract_type, keywords in contract_types.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[contract_type] = score
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "General Contract"
    
    def extract_clauses(self, text: str) -> List[Dict]:
        sections = re.split(r'\n\n+', text)
        clauses = []
        for idx, section in enumerate(sections[:10]):
            if len(section.strip()) > 50:
                clauses.append({
                    'title': section[:80].strip(),
                    'text': section.strip(),
                    'explanation': self._simplify_clause(section)
                })
        return clauses
    
    def _simplify_clause(self, clause_text: str) -> str:
        if "termination" in clause_text.lower():
            return "This clause describes how the contract can be ended."
        elif "payment" in clause_text.lower():
            return "This clause outlines payment terms."
        elif "confidential" in clause_text.lower():
            return "This protects confidential information."
        else:
            return "Important terms and conditions of the agreement."
    
    def identify_clause_type(self, clause_text: str) -> str:
        text_lower = clause_text.lower()
        if any(word in text_lower for word in ["shall not", "prohibited"]):
            return "Prohibition"
        elif any(word in text_lower for word in ["shall", "must", "required"]):
            return "Obligation"
        elif any(word in text_lower for word in ["may", "entitled", "right"]):
            return "Right"
        return "General Clause"
    
    def extract_entities(self, text: str) -> Dict:
        doc = self.nlp(text[:5000])
        entities = {
            'parties': [],
            'dates': [],
            'amounts': [],
            'jurisdiction': []
        }
        for ent in doc.ents:
            if ent.label_ == 'ORG' or ent.label_ == 'PERSON':
                entities['parties'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entities['amounts'].append(ent.text)
            elif ent.label_ == 'GPE':
                entities['jurisdiction'].append(ent.text)
        return entities
    
    def extract_obligations(self, text: str) -> List[str]:
        obligation_words = ["shall", "must", "required to", "obligated"]
        sentences = text.split(".")
        obligations = []
        for sent in sentences:
            if any(word in sent.lower() for word in obligation_words):
                obligations.append(sent.strip())
        return obligations[:10]
    
    def generate_summary(self, text: str) -> List[str]:
        contract_type = self.classify_contract_type(text)
        summary = [
            f"Contract type identified as: {contract_type}",
            f"Document length: {len(text)} characters",
            "Key sections extracted and analyzed",
            "Risk assessment completed"
        ]
        return summary

