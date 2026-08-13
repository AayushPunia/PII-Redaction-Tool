"""Custom Presidio recognizer for Indian Corporate Identity Numbers (CIN).

CIN format (21 characters):
    [U/L] [5 digits] [2-letter state code] [4-digit year] [PLC/PTC/GAP/NPL/OPC] [6 digits]
    Example: U28129PN1979PLC141032
        U       = Unlisted (L = Listed)
        28129   = Industry sub-classification (NIC code)
        PN      = State code (Pune/Maharashtra)
        1979    = Year of incorporation
        PLC     = Public Limited Company
        141032  = Registration number

The pattern is highly specific — false positives are rare because the fixed
structure (U/L prefix, state code, entity-type suffix) constrains matches
heavily. Score is set at 0.85 (high confidence).
"""

from presidio_analyzer import Pattern, PatternRecognizer


class CINRecognizer(PatternRecognizer):
    """Detects Indian Corporate Identity Numbers (CIN)."""

    PATTERNS = [
        Pattern(
            "CIN (full format)",
            r"\b[UL]\d{5}[A-Z]{2}\d{4}(?:PLC|PTC|GAP|NPL|OPC)\d{6}\b",
            0.85,
        ),
    ]

    CONTEXT = [
        "CIN",
        "Corporate Identity Number",
        "corporate identity",
        "incorporated",
        "registration number",
        "certificate of incorporation",
    ]

    def __init__(self):
        super().__init__(
            supported_entity="IN_CIN",
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            supported_language="en",
            name="CINRecognizer",
        )
