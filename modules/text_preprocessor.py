"""
Core Processing Module - Text Preprocessor
"""
import re
import unicodedata
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def clean_clinical_text(text):
    """
    Remove extra whitespace, non-ASCII chars, mask PHI (dates, IDs, phone numbers).
    """
    if not text:
        return ""
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII except basic punctuation
    text = re.sub(r"[^\w\s.,;:!?()\[\]'-]", '', text)
    # Mask dates (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD)
    text = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "[DATE]", text)
    # Mask MRN/ID
    text = re.sub(r"MRN:\d+", "[ID]", text)
    text = re.sub(r"ID:\d+", "[ID]", text)
    # Mask phone numbers
    text = re.sub(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def prepare_batch_for_api(df, text_column, batch_size=10):
    """
    Group Spark DataFrame rows into batches for API calls.
    """
    texts = [row[text_column] for row in df.collect()]
    return [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
