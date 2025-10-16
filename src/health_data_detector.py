import re
from typing import Dict
class HealthDataDetector:
    def __init__(self):
        # Common medical terms indicating health data
        self.medical_terms = [
            'diagnosis', 'treatment', 'medication', 'prescription',
            'allergy', 'condition', 'symptom', 'patient',
            'blood pressure', 'temperature', 'heart rate',
            'diabetes', 'cancer', 'surgery', 'therapy'
        ]

        # ICD-10 code pattern
        self.icd10_pattern = r'[A-Z]\d{2}\.?\d{0,2}'

    def detect_medical_content(self, text: str) -> Dict[str, bool]:
        """Check if text contains medical/health information"""
        text_lower = str(text).lower()

        findings = {
            'contains_medical_terms': any(term in text_lower for term in self.medical_terms),
            'contains_icd10_codes': bool(re.search(self.icd10_pattern, str(text))),
            'medical_terms_found': [term for term in self.medical_terms if term in text_lower]
        }

        return findings