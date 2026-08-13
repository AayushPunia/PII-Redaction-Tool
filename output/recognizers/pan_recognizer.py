"""Custom Presidio recognizer for Indian Permanent Account Numbers (PAN).

PAN format (10 characters):
    [5 uppercase letters] [4 digits] [1 uppercase letter]
    Example: ABCPD1234E

The 4th character indicates the holder type:
    C = Company, P = Person, H = HUF, F = Firm, A = AOP,
    T = Trust, B = BOI, L = Local Authority, J = AJP, G = Government

The pattern is moderately specific — many 10-character alphanumeric codes in
financial documents could incidentally match (e.g., SEBI registration numbers
like INM000013004 do NOT match because they start with "IN" + digit). Score
is set low (0.5) without context, boosted to ~0.9 with context words like
"PAN" or "Permanent Account Number".

GSTIN embeds a full PAN as characters 3–12. The GSTINRecognizer has a higher
score (0.90) so Presidio's overlap resolution picks the longer GSTIN match
when both fire on the same span.
"""

from presidio_analyzer import Pattern, PatternRecognizer


class PANRecognizer(PatternRecognizer):
    """Detects Indian Permanent Account Numbers (PAN)."""

    PATTERNS = [
        Pattern(
            "PAN",
            r"\b[A-Z]{5}\d{4}[A-Z]\b",
            0.5,  # Low base — boosted by context
        ),
    ]

    CONTEXT = [
        "PAN",
        "Permanent Account Number",
        "permanent account",
        "income tax",
        "tax identification",
        "IT department",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="IN_PAN",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="en",
            name="PANRecognizer",
        )
