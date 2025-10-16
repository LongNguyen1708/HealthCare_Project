import re
import pandas as pd
from typing import List, Dict


class PIIScanner:
    def __init__(self):
        self.patterns = {
            'nhs_number': r'\d{3}[-\s]?\d{3}[-\s]?\d{4}',
            'ni_number': r'[A-Z]{2}\d{6}[A-Z]',
            'postcode': r'[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'(?:(?:\+44\s?|0)(?:\d\s?){10,11})',
            'date_of_birth': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        }

    def scan_text(self, text: str) -> Dict[str, List[str]]:
        """Scan text for PII patterns"""
        findings = {}
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, str(text), re.IGNORECASE)
            if matches:
                findings[pii_type] = matches
        return findings

    def scan_dataframe(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """Scan entire dataframe for PII"""
        results = {
            'summary': {'total_pii_found': 0, 'affected_columns': []},
            'details': {}
        }

        for column in df.columns:
            column_findings = []
            for idx, value in df[column].items():
                pii_found = self.scan_text(value)
                if pii_found:
                    column_findings.append({
                        'row': idx,
                        'pii_types': list(pii_found.keys())
                    })

            if column_findings:
                results['details'][column] = column_findings
                results['summary']['affected_columns'].append(column)
                results['summary']['total_pii_found'] += len(column_findings)

        return results