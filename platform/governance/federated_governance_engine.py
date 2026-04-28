import logging

class FederatedGovernanceEngine:
    def __init__(self):
        self.logger = logging.getLogger("federated-governance")

    def validate_data_product(self, product_metadata: dict):
        """
        Validates a data product against federated governance standards.
        Standards include: Owner definition, PII labeling, and SLA specification.
        """
        required_metadata = ["owner_domain", "data_contract_version", "pii_labels", "sla_freshness_mins"]
        
        for field in required_metadata:
            if field not in product_metadata:
                self.logger.error(f"Validation failed: Missing required metadata field '{field}'")
                return False
        
        self.logger.info(f"Data product '{product_metadata.get('name', 'unnamed')}' passed federated governance checks.")
        return True

    def calculate_domain_maturity(self, domain_stats: dict):
        """
        Calculates the mesh maturity score for a domain based on 
        product quality, contract adherence, and documentation completeness.
        """
        # Simple weighted scoring model
        quality_score = domain_stats.get("avg_quality", 0) * 0.4
        contract_score = domain_stats.get("contract_adherence", 0) * 0.4
        docs_score = domain_stats.get("docs_complete_pct", 0) * 0.2
        
        maturity_index = (quality_score + contract_score + docs_score) * 10
        return round(maturity_index, 2)

if __name__ == "__main__":
    engine = FederatedGovernanceEngine()
    
    # Test Validation
    test_product = {
        "name": "FinanceLedger_v1",
        "owner_domain": "Finance",
        "data_contract_version": "1.0.0",
        "pii_labels": ["None"],
        "sla_freshness_mins": 60
    }
    
    is_valid = engine.validate_data_product(test_product)
    print(f"Product Valid: {is_valid}")
    
    # Test Maturity Calculation
    test_domain = {
        "avg_quality": 0.95,
        "contract_adherence": 0.98,
        "docs_complete_pct": 0.90
    }
    maturity = engine.calculate_domain_maturity(test_domain)
    print(f"Domain Maturity Score (0-10): {maturity}")
