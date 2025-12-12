"""
Azure Cognitive Services Integrator
"""
import time
import logging
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from .azure_connector import get_key_vault_secret

class HealthcareEntityExtractor:
    def __init__(self, key_vault_url=None):
        self.endpoint = get_key_vault_secret('cog-service-endpoint', key_vault_url)
        self.key = get_key_vault_secret('cog-service-key', key_vault_url)
        self.client = TextAnalyticsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))

    def extract_entities_batch(self, text_list, max_retries=5):
        results = []
        for attempt in range(max_retries):
            try:
                poller = self.client.begin_analyze_healthcare_entities(text_list)
                response = poller.result()
                for doc, text in zip(response, text_list):
                    if not doc.is_error:
                        for ent in doc.entities:
                            results.append({
                                'text': ent.text,
                                'category': ent.category,
                                'confidence_score': ent.confidence_score,
                                'offset': ent.offset
                            })
                    else:
                        logging.warning(f"Error in document: {doc.error}")
                return results
            except Exception as e:
                if hasattr(e, 'status_code') and e.status_code in [429, 503]:
                    wait = 2 ** attempt
                    logging.warning(f"Rate limited or service unavailable, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    logging.error(f"Unrecoverable error: {e}")
                    break
        return results

    def map_to_snomed_code(self, entity_text, category):
        """
        Stub: Map common terms to SNOMED CT codes. In production, use FHIR terminology service.
        """
        snomed_map = {
            ("aspirin", "MedicationName"): "1191",
            ("Type 2 Diabetes", "Diagnosis"): "44054006",
            ("hypertension", "Diagnosis"): "38341003"
        }
        return snomed_map.get((entity_text, category), None)
