# Deploy — GCP Cloud Run / Cloud Functions

Read this before deploying anything for a real client. Nothing here is
deployed yet — this is the plan, ready to follow.

## Before you deploy — checklist

- [ ] Client paid 50% upfront, in writing, for a fixed-price build.
- [ ] Scope approved in writing after the $750 audit.
- [ ] GCP project created for WeDoSimplify (one project; one dataset per client later).
- [ ] Billing alert set — see below. **Do this first, before any run.**
- [ ] No secrets in Git (check `.gitignore` — `.env`, `*-key.json`, client exports).

## Billing alert — $50 (do this first)

1. GCP Console → Billing → Budgets & alerts.
2. Create a budget: **$50/month** for the WeDoSimplify project.
3. Alert at 50%, 90%, and 100% — email to yusuf@wedosimplify.com.
4. Expected real cost per client: about $20–$50/month (Cloud Functions + BigQuery + Cloud Run free tier). If a client goes over $50, stop and check — do not let it run.

## Option A — Streamlit UI on Cloud Run (best first for the Friday report)

1. Add a `Dockerfile` in the client copy (not in this template yet — add it when the first client is signed):
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
   ```
2. Build and deploy:
   ```bash
   gcloud run deploy wedosimplify-<clientname> \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```
   Note: `--allow-unauthenticated` is for the first demo only. Add login
   (Google sign-in / Cloud Run IAM) before a real client uses it daily.
3. Cost: Cloud Run free tier covers a small weekly report. Expect $0–$20/month.

## Option B — Friday report as a Cloud Function (scheduled, no UI)

1. Wrap `make_friday_report()` in a function with this signature:
   ```python
   def friday_report(request):
       # read export from Cloud Storage, clean, make report, email it
       return "OK", 200
   ```
2. Deploy:
   ```bash
   gcloud functions deploy friday-report \
     --runtime python312 \
     --trigger-http \
     --region us-central1
   ```
3. Schedule it with Cloud Scheduler — every Friday, 7:00 AM America/Detroit.
4. Cost: pennies per run, plus BigQuery storage.

## BigQuery — fill in the stub in main.py

1. In GCP Console → BigQuery, create dataset `wedosimplify`, table `orders`.
2. In the client copy only, set `GCP_PROJECT_ID` in `.env`:
   ```
   GCP_PROJECT_ID=your-project-id-here
   ```
3. Uncomment the BigQuery code in `upload_to_bigquery()` in `main.py`.
4. Test with sample data first, then with a copy of the client's export — never test with the only copy of their data.

## What NOT to deploy yet

- No login / multi-client portal — add it only after the first paid build.
- No payment collection in the app — invoice by email first.
- No ERP integration — Friday report first.
