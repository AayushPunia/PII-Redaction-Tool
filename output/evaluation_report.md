# PII Redaction Evaluation Report

## Overall Metrics by PII Type

| Entity Type | Precision | Recall | F1 Score | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|
| ADDRESS | 1.00 | 1.00 | 1.00 | 2 | 0 | 0 | 0 |
| EMAIL_ADDRESS | 1.00 | 1.00 | 1.00 | 4 | 0 | 0 | 0 |
| IN_CIN | 1.00 | 1.00 | 1.00 | 1 | 0 | 0 | 0 |
| IN_DIN | 1.00 | 0.00 | 0.00 | 0 | 0 | 1 | 0 |
| LOCATION | 1.00 | 1.00 | 1.00 | 2 | 0 | 0 | 0 |
| ORGANIZATION | 1.00 | 0.50 | 0.67 | 2 | 0 | 2 | 0 |
| PERSON | 1.00 | 1.00 | 1.00 | 5 | 0 | 0 | 0 |
| PHONE_NUMBER | 1.00 | 1.00 | 1.00 | 1 | 0 | 0 | 0 |

## Global Metrics (25-Span Sample)

- **Precision:** 1.00
- **Recall:** 0.85
- **F1 Score:** 0.92

## Negative Controls Performance

These 5 spans test precision by ensuring the tool does **not** over-redact non-PII:

- `KSH International Limited`: **TN (Preserved)**
  - *Original:* KSH International Limited, a public limited company incorporated under the Companies Act, 1956, having its registered office at 11/3, 11/4 and 11/5, V...
  - *Redacted:* KSH International Limited, a public limited company incorporated under the Companies Act, 1956, having its registered office at 11/3, 11/4 and 11/5, R...

- `₹ 783.77`: **TN (Preserved)**
  - *Original:* Additionally, an amount of ₹ 783.77 million from the Net Proceeds is intended to be utilised towards the Phase II Expansion at our Supa Facility. For ...
  - *Redacted:* Additionally, an amount of ₹ 783.77 million from Koshy PLC is intended to be utilised towards Malhotra PLC at our Yagnesh Divan. For further details, ...

- `page 250`: **TN (Preserved)**
  - *Original:* or qualified replacements, our results of operations may be adversely affected. For details of changes in our key management personnel, please see “Ou...
  - *Redacted:* or qualified replacements, our results of operations may be adversely affected. For details of changes in our key management personnel, please see Kor...

- `01217000`: **TN (Preserved)**
  - *Original:* 01217000
  - *Redacted:* 01217000

- `March 31, 2024`: **TN (Preserved)**
  - *Original:* The restated financial information of our Company comprising the restated statements of assets and liabilities as on and for the three months period e...
  - *Redacted:* The restated financial information of our Company comprising the restated statements of assets and liabilities as on and for the three months period e...

## Positive Controls Performance

- `Sarthak Malvadkar` (PERSON): **TP (Redacted)**
- `cs.connect@kshinternational.com` (EMAIL_ADDRESS): **TP (Redacted)**
- `+ 91 20 45053237` (PHONE_NUMBER): **TP (Redacted)**
- `U28129PN1979PLC141032` (IN_CIN): **TP (Redacted)**
- `Kushal Subbayya Hegde` (PERSON): **TP (Redacted)**
- `Pushpa Kushal Hegde` (PERSON): **TP (Redacted)**
- `Rajesh Kushal Hegde` (PERSON): **TP (Redacted)**
- `Rohit Kushal Hegde` (PERSON): **TP (Redacted)**
- `00135070` (IN_DIN): **FN (Leaked)**
- `Sarthak.malvadkar@kshinterantional.com` (EMAIL_ADDRESS): **TP (Redacted)**
- `Nuvama Wealth Management Limited` (ORGANIZATION): **TP (Redacted)**
- `ICICI Securities Limited` (ORGANIZATION): **FN (Leaked)**
- `Trilegal` (ORGANIZATION): **FN (Leaked)**
- `Kirtane & Pandit LLP` (ORGANIZATION): **TP (Redacted)**
- `11/3, 11/4 and 11/5, Village Birdewadi, Chakan Taluka - Khed, Pune – 410 501, Maharashtra, India` (ADDRESS): **TP (Redacted)**
- `201, Tower 2, Montreal Business Centre, Off Pallod Farms, Baner, Pune – 411 045, Maharashtra, India` (ADDRESS): **TP (Redacted)**
- `Pune` (LOCATION): **TP (Redacted)**
- `Maharashtra` (LOCATION): **TP (Redacted)**
- `ksh.ipo@nuvama.com` (EMAIL_ADDRESS): **TP (Redacted)**
- `customerservice.mb@nuvama.com` (EMAIL_ADDRESS): **TP (Redacted)**