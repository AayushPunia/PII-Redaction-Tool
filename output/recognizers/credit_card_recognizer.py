"""Custom Presidio recognizer for credit card numbers with Luhn validation.

This recognizer matches 13–19 digit sequences (with optional spaces/dashes
between groups) and validates each candidate against the Luhn checksum
algorithm before flagging it as PII.

The Luhn check is the single biggest precision improvement for credit card
detection in a financial document like a prospectus:
- Without it: CINs (21 chars including digits), phone number fragments,
  registration numbers, and account references would false-positive.
- With it: only sequences that actually pass the Luhn checksum are flagged.

Known residual limitation: approximately 1 in 10 random digit strings will
pass the Luhn check by chance. So a real bank account number or reference
number could occasionally be misclassified as a credit card. This is called
out in the README as a known limitation rather than hidden.

For the KSH International RHP specifically, zero credit card numbers are
expected — this is correct behavior for an Indian public filing document,
not a detection failure.
"""

import re
from typing import List, Optional

from presidio_analyzer import EntityRecognizer, RecognizerResult


def luhn_checksum(number_str: str) -> bool:
    """Validate a digit string against the Luhn algorithm.

    The Luhn algorithm (mod-10) is the standard checksum used by all major
    credit card networks (Visa, Mastercard, Amex, etc.).

    Args:
        number_str: String of digits to validate (non-digit chars are ignored).

    Returns:
        True if the string passes the Luhn check.
    """
    digits = [int(d) for d in number_str if d.isdigit()]
    if len(digits) < 13 or len(digits) > 19:
        return False

    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


class CreditCardLuhnRecognizer(EntityRecognizer):
    """Detects credit card numbers using pattern matching + Luhn validation."""

    # Pattern: sequences of 13-19 digits with optional separators
    CARD_PATTERN = re.compile(
        r"\b"
        r"(?:\d[\s\-]*){12,18}"  # 12-18 digits with optional separators
        r"\d"                     # final digit (total 13-19)
        r"\b"
    )

    def __init__(self):
        super().__init__(
            supported_entities=["CREDIT_CARD"],
            supported_language="en",
            name="CreditCardLuhnRecognizer",
        )

    def load(self) -> None:
        """No external resources to load."""

    def analyze(
        self,
        text: str,
        entities: List[str],
        nlp_artifacts: Optional[object] = None,
        regex_flags: Optional[int] = None,
    ) -> List[RecognizerResult]:
        results: List[RecognizerResult] = []

        for match in self.CARD_PATTERN.finditer(text):
            candidate = match.group()
            digits_only = re.sub(r"[\s\-]", "", candidate)

            # Length check + Luhn validation
            if 13 <= len(digits_only) <= 19 and luhn_checksum(digits_only):
                results.append(
                    RecognizerResult(
                        entity_type="CREDIT_CARD",
                        start=match.start(),
                        end=match.end(),
                        score=0.8,
                    )
                )

        return results
