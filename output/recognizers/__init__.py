"""Custom Presidio recognizers for Indian corporate/financial PII types.

Each recognizer is a properly registered Presidio PatternRecognizer or
EntityRecognizer, so adding a new PII type is a single-file addition +
one import line here + one `registry.add_recognizer()` call in redact.py.
"""

from .cin_recognizer import CINRecognizer
from .pan_recognizer import PANRecognizer
from .din_recognizer import DINRecognizer
from .gstin_recognizer import GSTINRecognizer
from .phone_in_recognizer import IndiaPhoneRecognizer
from .credit_card_recognizer import CreditCardLuhnRecognizer
from .dob_recognizer import DOBRecognizer

__all__ = [
    "CINRecognizer",
    "PANRecognizer",
    "DINRecognizer",
    "GSTINRecognizer",
    "IndiaPhoneRecognizer",
    "CreditCardLuhnRecognizer",
    "DOBRecognizer",
]
