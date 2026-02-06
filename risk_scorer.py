import re
from typing import List, Dict

class RiskAssessment:
    def __init__(self):
        self.high_risk_keywords = [
            'penalty', 'indemnity', 'termination without cause', 
            'unilateral', 'non-compete', 'auto-renewal',
            'lock-in', 'exclusive', 'unlimited liability'
        ]
        self.medium_risk_keywords = [
            'arbitration', 'jurisdiction', 'confidential',
            'force majeure', 'assignment'
        ]
    
    def assess_contract_risk(self, text: str, analyzer) -> Dict:
        text_lower = text.lower()
        
        # Count risk factors
        high_risk_count = sum(1 for keyword in self.high_risk_keywords if keyword in text_lower)
        medium_risk_count = sum(1 for keyword in self.medium_risk_keywords if keyword in text_lower)
        
        # Calculate risk score
        risk_score = (high_risk_count * 15) + (medium_risk_count * 5)
        risk_score = min(risk_score, 100)
        
        # Determine overall risk level
        if risk_score >= 60:
            overall_risk = "High"
        elif risk_score >= 30:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"
        
        # Identify specific risk factors
        risk_factors = []
        
        if 'penalty' in text_lower:
            risk_factors.append({
                'severity': 'HIGH',
                'type': 'Penalty Clause',
                'description': 'Contract contains penalty provisions',
                'impact': 'May result in financial penalties',
                'clause_reference': 'Penalty section'
            })
        
        if 'indemnity' in text_lower or 'indemnification' in text_lower:
            risk_factors.append({
                'severity': 'HIGH',
                'type': 'Indemnity Clause',
                'description': 'Indemnification obligations present',
                'impact': 'May require you to cover third-party losses',
                'clause_reference': 'Indemnity section'
            })
        
        if 'non-compete' in text_lower or 'non compete' in text_lower:
            risk_factors.append({
                'severity': 'HIGH',
                'type': 'Non-Compete Clause',
                'description': 'Non-compete restrictions found',
                'impact': 'Limits business activities after contract ends',
                'clause_reference': 'Non-compete section'
            })
        
        if 'auto-renewal' in text_lower or 'automatically renew' in text_lower:
            risk_factors.append({
                'severity': 'MEDIUM',
                'type': 'Auto-Renewal',
                'description': 'Contract auto-renews without action',
                'impact': 'May continue indefinitely if not cancelled',
                'clause_reference': 'Renewal section'
            })
        
        if 'unilateral' in text_lower and 'termination' in text_lower:
            risk_factors.append({
                'severity': 'HIGH',
                'type': 'Unilateral Termination',
                'description': 'One party can terminate without cause',
                'impact': 'Contract can be ended suddenly',
                'clause_reference': 'Termination clause'
            })
        
        return {
            'overall_risk': overall_risk,
            'risk_score': risk_score,
            'high_risk_count': high_risk_count,
            'risk_factors': risk_factors
        }
    
    def identify_unfavorable_clauses(self, text: str) -> List[Dict]:
        unfavorable = []
        text_lower = text.lower()
        
        if 'unlimited liability' in text_lower:
            unfavorable.append({
                'title': 'Unlimited Liability',
                'issue': 'You may have unlimited financial exposure',
                'alternative': 'Negotiate for liability cap or limited liability clause'
            })
        
        if 'exclusive' in text_lower and 'vendor' in text_lower:
            unfavorable.append({
                'title': 'Exclusivity Provision',
                'issue': 'Restricted from working with other parties',
                'alternative': 'Request non-exclusive arrangement or limited exclusivity period'
            })
        
        if 'no warranty' in text_lower or 'as-is' in text_lower:
            unfavorable.append({
                'title': 'No Warranty',
                'issue': 'No guarantees on quality or performance',
                'alternative': 'Negotiate for express warranties or performance guarantees'
            })
        
        return unfavorable
