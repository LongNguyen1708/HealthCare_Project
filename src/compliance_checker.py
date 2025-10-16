class ComplianceChecker:
    def __init__(self):
        self.violations = []
        self.warnings = []

    def check_encryption(self, file_info: Dict) -> None:
        """Check if sensitive data is encrypted"""
        if not file_info.get('encrypted', False):
            self.violations.append({
                'type': 'ENCRYPTION',
                'severity': 'HIGH',
                'article': 'Article 32',
                'description': 'Health data must be encrypted at rest'
            })

    def check_consent_records(self, has_consent_log: bool) -> None:
        """Check if consent is properly documented"""
        if not has_consent_log:
            self.warnings.append({
                'type': 'CONSENT',
                'severity': 'MEDIUM',
                'article': 'Article 9',
                'description': 'No consent records found for special category data'
            })

    def check_retention_period(self, data_age_days: int) -> None:
        """Check data retention compliance"""
        if data_age_days > 1825:  # 5 years
            self.warnings.append({
                'type': 'RETENTION',
                'severity': 'MEDIUM',
                'article': 'Article 5(1)(e)',
                'description': f'Data retained for {data_age_days} days - review retention policy'
            })

    def generate_compliance_report(self) -> Dict:
        """Generate compliance report"""
        return {
            'compliant': len(self.violations) == 0,
            'violations': self.violations,
            'warnings': self.warnings,
            'recommendations': self._generate_recommendations()
        }

    def _generate_recommendations(self) -> List[str]:
        recommendations = []
        if any(v['type'] == 'ENCRYPTION' for v in self.violations):
            recommendations.append("Implement AES-256 encryption for all health data storage")
        if any(w['type'] == 'CONSENT' for w in self.warnings):
            recommendations.append("Establish consent management system with audit trails")
        return recommendations