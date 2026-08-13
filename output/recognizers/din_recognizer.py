"""Custom Presidio recognizer for Indian Director Identification Numbers (DIN).

DIN format: 8 digits (zero-padded)
    Example: 00135070

The pattern is extremely generic — bare 8-digit numbers appear frequently in
financial documents as amounts, reference numbers, phone fragments, etc.
Score is deliberately set very low (0.3 bare) and relies heavily on context
words ("DIN", "Director Identification Number", "designation") to boost to
a usable confidence level (~0.85 with context).

This design prevents false-positive redaction of monetary amounts,
registration numbers, and other 8-digit values that happen to appear in
the same document.
"""

from presidio_analyzer import Pattern, PatternRecognizer


class DINRecognizer(PatternRecognizer):
    """Detects Indian Director Identification Numbers (DIN)."""

    PATTERNS = [
        Pattern(
            "DIN (8 digits)",
            r"\b\d{8}\b",
            0.3,  # Very low — 8-digit numbers are common
        ),
    ]

    CONTEXT = [
        "DIN",
        "Director Identification Number",
        "director identification",
        "director",
        "designation",
        "Board of Directors",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="IN_DIN",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="en",
            name="DINRecognizer",
        )
