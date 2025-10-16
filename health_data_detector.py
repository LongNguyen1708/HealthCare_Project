import re
from tkinter import BooleanVar
from typing import List, Dict, final

class HealthDataDetector:
    def __init__(self):
        self.medical_terms = [
             'diagnosis', 'treatment', 'medication', 'prescription',
            'allergy', 'condition', 'symptom', 'patient',
            'blood pressure', 'temperature', 'heart rate',
            'diabetes', 'cancer', 'surgery', 'therapy' , ' acute' , 'chronic',
            'hypertension'
        ]
        self.icd10_pattern = r'[A-Z]\d{2}\.?\d{0,2}'
    def detect_medical_terms(self, text:str) -> Dict[str , bool]:
        text_lower_case = str(text).lower()
        findings = {
            'contain_medical_terms' : any(term in text_lower_case for term in self.medical_terms),
            'contain_icd10_code' : bool(re.search(self.icd10_pattern, str(text))),
            'medical_foudn' :[term for term in self.medical_terms if term in text_lower_case],

        }
        return findings