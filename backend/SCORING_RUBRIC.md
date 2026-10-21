# Scoring rubric

The Trust Score is an evidence-based 0-100 transparency and user-protection signal. It is not a legal compliance determination.

| Category | Weight | Starting score | Evidence that changes the score |
| --- | ---: | ---: | --- |
| Data sharing | 25% | 75 | Advertising, analytics, or third-party sharing lowers the score. |
| Readability | 20% | Calculated | Sentence length and the proportion of words with eight or more characters determine the score. |
| Data collection | 20% | 70 | Location, device identifiers, and contact-data collection lower the score. |
| Legal language | 20% | 75 | Retention ambiguity, arbitration, class-action waivers, liability limits, and unilateral changes lower the score. |
| User agency | 15% | 60 | Access, deletion, consent, and sale/share opt-out controls raise the score. |

Only categories with evidence are included in the normalized score. Missing evidence is reported as partial coverage; it never means the policy is safe or compliant.

## Thresholds

- 0-39: high risk signal
- 40-64.99: moderate risk signal
- 65-100: lower risk signal
- no assessable categories: unknown

## Change record

| Date | Change | Reason and validation |
| --- | --- | --- |
| 2026-10-21 | Added analytics, contact-data, legal-clause, and consent patterns; readability complexity metric. | Expanded category tests, calibration fixtures, repeated-output tests, and the full backend suite. |
