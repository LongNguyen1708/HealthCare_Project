# test_scanner.py
import pandas as pd
from src.pii_scanner import PIIScanner
from src.health_data_detector import HealthDataDetector
import os


def test_csv_scanner():
    """Test the scanner with sample CSV file"""

    # Initialize scanners
    pii_scanner = PIIScanner()
    health_detector = HealthDataDetector()

    # Load CSV file
    csv_path = ("E:/CyberSecurity/Project/HealthCare/data/test_patient_data.csv")

    if not os.path.exists(csv_path):
        print(" CSV file not found! Make sure you created it in the data folder.")
        return

    df = pd.read_csv(csv_path)

    print(" CSV File Loaded Successfully!")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print(f"Columns: {', '.join(df.columns)}")
    print("\n" + "=" * 50 + "\n")

    # Test 1: Scan for PII
    print(" Scanning for Personal Identifiable Information (PII)...")

    pii_found = {}
    for column in df.columns:
        column_has_pii = False
        for idx, value in df[column].items():
            if pd.notna(value):  # Skip empty cells
                pii_results = pii_scanner.scan_text(str(value))
                if pii_results:
                    if column not in pii_found:
                        pii_found[column] = []
                    pii_found[column].append({
                        'row': idx,
                        'value': str(value),
                        'pii_types': list(pii_results.keys())
                    })
                    column_has_pii = True

        if column_has_pii:
            print(f" Column '{column}' contains PII")

    # Display PII findings
    if pii_found:
        print(f"\n PII found in {len(pii_found)} columns:")
        for column, findings in pii_found.items():
            print(f"\n  Column: {column}")
            for finding in findings[:2]:  # Show first 2 examples
                print(f"    Row {finding['row']}: {finding['pii_types']}")
    else:
        print(" No PII found!")

    print("\n" + "=" * 50 + "\n")

    # Test 2: Scan for Health Data
    print(" Scanning for Health Data...")

    health_data_found = False
    health_columns = []

    for column in df.columns:
        # Check column name first
        if health_detector.detect_medical_content(column)['contains_medical_terms']:
            health_columns.append(column)
            health_data_found = True

        # Check column content
        sample_values = df[column].dropna().head(5)
        for value in sample_values:
            if health_detector.detect_medical_content(str(value))['contains_medical_terms']:
                if column not in health_columns:
                    health_columns.append(column)
                health_data_found = True
                break

    if health_data_found:
        print(f"  Health data found in columns: {', '.join(health_columns)}")
        print(" This data requires Article 9 GDPR protection!")
    else:
        print(" No health data detected")

    print("\n" + "=" * 50 + "\n")

    # Test 3: Generate Compliance Report
    print(" Compliance Summary:")
    print(f"- Total rows scanned: {len(df)}")
    print(f"- Columns with PII: {len(pii_found)}")
    print(f"- Columns with health data: {len(health_columns)}")

    if pii_found and health_data_found:
        print("\n⚠️  HIGH RISK: File contains both PII and health data!")
        print("Recommendations:")
        print("1. Encrypt this file immediately")
        print("2. Implement access controls")
        print("3. Consider data minimization")
        print("4. Ensure consent documentation exists")

    # Test 4: Show specific examples
    print("\n" + "=" * 50 + "\n")
    print(" Example Findings:")

    # Show one example row
    example_row = df.iloc[0]
    print(f"\nExample from Row 0:")
    for column, value in example_row.items():
        pii = pii_scanner.scan_text(str(value))
        health = health_detector.detect_medical_content(str(value))

        if pii or health['contains_medical_terms']:
            status = []
            if pii:
                status.append(f"PII: {list(pii.keys())}")
            if health['contains_medical_terms']:
                status.append("Health Data")
            print(f"  {column}: {value} → {', '.join(status)}")


if __name__ == "__main__":
    print(" Healthcare GDPR Scanner Test")
    print("================================\n")
    test_csv_scanner()