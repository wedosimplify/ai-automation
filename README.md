# WeDoSimplify — Python / GCP Template

One template project. **Copy this folder for each new client. Do not edit the
template itself for a client.**

## What it is

- **Client:** small Michigan manufacturer, 10–30 staff, runs on Excel / email.
- **Offer:** $750 written audit in 7 days → $3,000–$4,000 fixed-price build → $500–$750/month retainer.
- **Rule:** the client's Excel / ERP stays. We read their export. We do not replace anything.

## Files

| File | What it does |
|---|---|
| `main.py` | Read export → clean data → make Friday report → upload to BigQuery (stub) |
| `app.py` | Streamlit UI — 1-page Friday report with charts and manual-work findings |
| `sample-data.csv` | Sample export, so the template runs with no client data |
| `requirements.txt` | pandas, openpyxl, google-cloud-bigquery, google-cloud-functions, streamlit |
| `.gitignore` | Blocks secrets and client data from Git — do not weaken it |
| `DEPLOY.md` | How to deploy to GCP Cloud Run / Cloud Functions, billing alert $50 |

## Setup — local, 5 steps

1. **Python 3.11 or 3.12** — check: `python3 --version`
2. **Make a virtual environment (do this, do not install globally):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Test with sample data:**
   ```bash
   python3 main.py
   python3 main.py sample-data.csv
   ```
   Both should print the Friday report. No GCP account is needed for this.
5. **Test the UI:**
   ```bash
   streamlit run app.py
   ```
   Open the link Streamlit prints (usually http://localhost:8501).

## Setup — for a real client

1. Copy this folder: `cp -r wedosimplify-template clients/<ClientName>/`
2. In the copy only, change in `app.py`: `CLIENT_NAME` and `WEEK_LABEL`.
3. Put the client's export in the copy (never in the template, never in Git).
4. Run `python3 main.py <client-export.csv>` — check the "Needs checking" list first.
5. Fill in the BigQuery stub in `main.py` (`upload_to_bigquery`) — see `DEPLOY.md`.
   Do not set a real GCP project ID in the template. Set it in the client copy
   only, or in an `.env` file (which `.gitignore` blocks from Git).

## AI tools

- **Claude — $20/month (Pro), best first:** writing the audit, writing and fixing this code.
- **Gemini — in GCP, for client builds:** the AI inside the client's automation, so client data stays in GCP.
- **n8n — free self-hosted, or $20/month hosted:** glue only — email to Sheet, Sheet to report, trigger Python. Do not build the whole job in n8n.

## Costs to remember (per client)

- GCP run cost: about $20–$50/month per client — the client pays this inside the retainer.
- Claude: about $1–$2 per audit in API use, or $20/month flat Pro.
- Do not start a client build without the 50% upfront payment in writing.

## What NOT to do

- Do not commit `.env`, service-account JSON, or any client export to Git.
- Do not replace a client's ERP.
- Do not promise a price before the $750 audit is done and the scope is approved in writing.
- Do not build an ERP integration first — Friday report first, then quote/order intake, then AI document reading.
