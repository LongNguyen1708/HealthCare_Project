# main.py
import sys
import pandas as pd
from src.pii_scanner import PIIScanner
from src.health_data_detector import HealthDataDetector
from src.compliance_checker import ComplianceChecker


def analyze_healthcare_data(file_path: str):
    """Main function to analyze healthcare data for GDPR compliance"""

    # Initialize scanners
    pii_scanner = PIIScanner()
    health_detector = HealthDataDetector()
    compliance_checker = ComplianceChecker()

    # Load and scan data
    df = pd.read_csv(file_path)

    print("🔍 Scanning for Personal Identifiable Information...")
    pii_results = pii_scanner.scan_dataframe(df)

    print("🏥 Detecting health-related data...")
    health_data_found = False
    for column in df.columns:
        for value in df[column].dropna().unique()[:10]:  # Sample check
            if health_detector.detect_medical_content(value)['contains_medical_terms']:
                health_data_found = True
                break

    print("📋 Checking GDPR compliance...")
    # Run compliance checks
    compliance_checker.check_encryption({'encrypted': False})  # Example
    compliance_checker.check_consent_records(False)  # Example

    # Generate report
    report = compliance_checker.generate_compliance_report()

    return {
        'pii_scan': pii_results,
        'contains_health_data': health_data_found,
        'compliance_report': report
    }