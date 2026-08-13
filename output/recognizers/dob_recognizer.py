"""Custom Presidio recognizer for dates of birth (context-dependent).

This recognizer ONLY flags date-like patterns that appear within a configurable
proximity window of contextual cue words: "born", "date of birth", "DOB",
"age of", "aged", "birthday".

This context-gating is critical in a legal/financial document like a Red
Herring Prospectus, which contains hundreds of dates (filing dates, fiscal
year ends, resolution dates, regulatory deadlines) that are emphatically NOT
dates of birth. Without context gating, virtually every date in the document
would be a false positive.

For the KSH International RHP specifically: no literal "date of birth", "DOB",
"born", or "aged" language was found attached to any name in the document
(verified by XML-level search). This recognizer is therefore expected to fire
zero times — this is correct behavior and is stated explicitly in the
evaluation report rather than being reported as a detection gap.
"""

import re
from typing import List, Optional

from presidio_analyzer import EntityRecognizer, RecognizerResult


class DOBRecognizer(EntityRecognizer):
    """Detects dates of birth by requiring proximity to contextual cue words."""

    # Date patterns covering common formats
    DATE_PATTERNS = [
        # DD/MM/YYYY or MM/DD/YYYY or DD-MM-YYYY etc.
        re.compile(r"\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b"),
        # "Month DD, YYYY"
        re.compile(
            r"\b(?:January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
            re.IGNORECASE,
        ),
        # "DD Month YYYY"
        re.compile(
            r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|"
            r"September|October|November|December),?\s+\d{4}\b",
            re.IGNORECASE,
        ),
    ]

    # Cue words that indicate a nearby date is a date of birth
    CUE_WORDS = re.compile(
        r"\b(?:born|date\s+of\s+birth|d\.?o\.?b\.?|birthday|"
        r"age\s+of|aged\s+\d|years?\s+old)\b",
        re.IGNORECASE,
    )

    # Maximum character distance between a date and a cue word
    CONTEXT_WINDOW = 120

    def __init__(self):
        super().__init__(
            supported_entities=["DATE_OF_BIRTH"],
            supported_language="en",
            name="DOBRecognizer",
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

        # Step 1: find all cue-word positions
        cue_positions = [m.start() for m in self.CUE_WORDS.finditer(text)]
        if not cue_positions:
            return results  # No cue words → no DOBs to find

        # Step 2: find all date candidates and check proximity to cue words
        for pattern in self.DATE_PATTERNS:
            for match in pattern.finditer(text):
                for cue_pos in cue_positions:
                    distance = min(
                        abs(match.start() - cue_pos),
                        abs(match.end() - cue_pos),
                    )
                    if distance <= self.CONTEXT_WINDOW:
                        results.append(
                            RecognizerResult(
                                entity_type="DATE_OF_BIRTH",
                                start=match.start(),
                                end=match.end(),
                                score=0.75,
                            )
                        )
                        break  # Don't double-count from multiple cues

        return results
