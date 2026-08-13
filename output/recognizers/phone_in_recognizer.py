"""Custom Presidio recognizer for Indian phone numbers.

Matches three common Indian phone number formats:

1. International format: +91 XX XXXXXXXX (with various spacing/dashes)
   Examples: +91 22 40094400, +91 8879770456, + 91 20 4505 3237

2. Landline with STD code: 0XX-XXXXXXXX
   Examples: 022-68052182, 020-67295100

3. 10-digit mobile: starts with 6/7/8/9
   Example: 9158640360

This complements Presidio's default PhoneRecognizer (which uses the
`phonenumbers` library and is more US-centric). Both recognizers fire
independently; Presidio's overlap resolution keeps the higher-scored
result when they detect the same span.
"""

from presidio_analyzer import Pattern, PatternRecognizer


class IndiaPhoneRecognizer(PatternRecognizer):
    """Detects Indian phone numbers in domestic and international formats."""

    PATTERNS = [
        # +91 prefix with flexible separators — most common in this document
        Pattern(
            "IN_PHONE_INTL",
            r"\+\s*91[\s\-]*(?:\d[\s\-]*){10}",
            0.75,
        ),
        # Landline with STD code: 0XX(X)-XXXXXXXX
        Pattern(
            "IN_PHONE_LANDLINE",
            r"\b0\d{2,4}[\s\-]+\d{6,8}\b",
            0.6,
        ),
        # 10-digit mobile starting with 6-9 (no prefix)
        Pattern(
            "IN_PHONE_MOBILE",
            r"\b[6-9]\d{9}\b",
            0.4,  # Low — 10-digit numbers can be other things
        ),
    ]

    CONTEXT = [
        "telephone",
        "phone",
        "mobile",
        "contact",
        "call",
        "tel",
        "fax",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="PHONE_NUMBER",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="en",
            name="IndiaPhoneRecognizer",
        )
