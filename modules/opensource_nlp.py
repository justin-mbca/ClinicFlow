"""
Open-Source Model Integrator
"""
import spacy
from transformers import pipeline
from functools import lru_cache

@lru_cache(maxsize=1)
def load_models():
    nlp_spacy = spacy.load("en_core_web_sm")
    nlp_hf = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")
    return nlp_spacy, nlp_hf

def extract_entities_open_source(text, model_type='spacy'):
    nlp_spacy, nlp_hf = load_models()
    results = []
    if model_type == 'spacy':
        doc = nlp_spacy(text)
        for ent in doc.ents:
            results.append({
                'text': ent.text,
                'category': ent.label_,
                'confidence_score': 1.0,
                'offset': ent.start_char
            })
    else:
        ents = nlp_hf(text)
        for ent in ents:
            # Normalize label to Azure schema where possible
            label_map = {
                'PER': 'Person',
                'ORG': 'Organization',
                'LOC': 'Location',
                'MISC': 'Miscellaneous',
                'DRUG': 'MedicationName',
                'DISEASE': 'Diagnosis'
            }
            results.append({
                'text': ent['word'],
                'category': label_map.get(ent['entity_group'], ent['entity_group']),
                'confidence_score': ent['score'],
                'offset': ent['start']
            })
    return results
