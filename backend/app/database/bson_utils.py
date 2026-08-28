"""
BSON/ObjectId sanitization utilities.

Converts any BSON ObjectId (and other non-JSON-serializable types)
to plain strings before returning documents to FastAPI response handlers.
"""
from typing import Any, Dict, List, Optional

def sanitize_doc(doc: Any) -> Any:
    """Recursively convert ObjectId / non-serializable BSON types to str."""
    if doc is None:
        return None
    if isinstance(doc, dict):
        result = {}
        for k, v in doc.items():
            result[k] = sanitize_doc(v)
        return result
    if isinstance(doc, list):
        return [sanitize_doc(item) for item in doc]
    # Check for BSON ObjectId without importing bson at module level
    # (works whether or not pymongo is installed)
    type_name = type(doc).__name__
    if type_name == "ObjectId":
        return str(doc)
    # Datetime objects are fine for JSON encoding via FastAPI
    return doc


def sanitize_docs(docs: List[Dict]) -> List[Dict]:
    return [sanitize_doc(d) for d in docs]
