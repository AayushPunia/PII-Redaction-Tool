"""Custom Presidio recognizer for Indian GSTIN (Goods and Services Tax
Identification Number).

GSTIN format (15 characters):
    [2-digit state code] [PAN (10 chars)] [1 digit] [Z] [check char]
    Example: 27AABCU9603R1ZP

GSTIN embeds a full PAN as characters 3–12. This recognizer has a
deliberately higher score (0.90) than PANRecognizer (0.50) so that
Presidio's overlap resolution picks the GSTIN (longer, more specific)
match when both recognizers fire on the same span, rather than
reporting both or only the PAN.
"""

from presidio_analyzer import Pattern, PatternRecognizer


class GSTINRecognizer(PatternRecognizer):
    """Detects Indian Goods and Services Tax Identification Numbers (GSTIN)."""

    PATTERNS = [
        Pattern(
            "GSTIN",
            r"\b\d{2}[A-Z]{5}\d{4}[A-Z]\d[A-Z\d][A-Z\d]\b",
            0.90,  # Higher than PAN to win overlap resolution
        ),
    ]

    CONTEXT = [
        "GSTIN",
        "GST",
        "Goods and Services Tax",
        "GST registration",
        "GST number",
        "tax identification",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="IN_GSTIN",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="en",
            name="GSTINRecognizer",
        )
