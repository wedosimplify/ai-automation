"""
WeDoSimplify — Python/GCP template for one client build.
Copy this folder for each new client. Do NOT edit the template itself
for a client — copy it, then edit the copy.

What this does, in plain words:
1. Reads the client's Excel / CSV export (they keep using Excel/ERP).
2. Cleans the data (removes blanks, fixes dates, fixes numbers).
3. Makes the 1-page Friday report.
4. Uploads the clean data to BigQuery (stub — fill in your GCP project first).

Run locally with sample data:
    python3 main.py
No GCP credentials are needed for the local sample run.
"""

import csv
import os
from collections import Counter, defaultdict
from datetime import date

# ---------------------------------------------------------------------------
# 1. Read the client's Excel / CSV export
# ---------------------------------------------------------------------------

def read_excel_export(path):
    """Read a CSV export. For a real .xlsx file, use pandas read_excel
    (see requirements.txt). Returns a list of dicts, one per row."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Export file not found: {path}")
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
    return rows


def read_sample_data():
    """Sample data so the template runs without a client file.
    Columns match a typical quote/order export: date, customer, item,
    quantity, amount, status."""
    return [
        {"date": "2026-11-02", "customer": "Acme Packaging", "item": "Carton 12x12", "quantity": "200", "amount": "1240.00", "status": "Shipped"},
        {"date": "2026-11-02", "customer": "Bright Foods", "item": "Tray 8x6", "quantity": "150", "amount": "690.00", "status": "Open"},
        {"date": "2026-11-03", "customer": "Acme Packaging", "item": "Carton 12x12", "quantity": "100", "amount": "620.00", "status": "Shipped"},
        {"date": "2026-11-04", "customer": "North Metal", "item": "Bracket A", "quantity": "80", "amount": "960.00", "status": "Open"},
        {"date": "2026-11-05", "customer": "Bright Foods", "item": "Tray 8x6", "quantity": "300", "amount": "1380.00", "status": "Open"},
        {"date": "2026-11-05", "customer": "Lake Plastics", "item": "Lid 90mm", "quantity": "500", "amount": "750.00", "status": "Shipped"},
        {"date": "2026-11-06", "customer": "North Metal", "item": "Bracket A", "quantity": "40", "amount": "480.00", "status": "Shipped"},
        {"date": "2026-11-06", "customer": "Acme Packaging", "item": "Carton 12x12", "quantity": "", "amount": "", "status": "Open"},
    ]


# ---------------------------------------------------------------------------
# 2. Clean the data
# ---------------------------------------------------------------------------

def clean_data(rows):
    """Clean one export. Returns (clean_rows, problems).
    - Blank quantity/amount become 0 and are flagged.
    - Amounts become floats; bad numbers become 0 and are flagged.
    - Dates are kept as text here; a real build should parse them.
    """
    clean = []
    problems = []
    for i, row in enumerate(rows, start=2):  # row 2 = first data row in Excel
        r = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        if not r.get("customer"):
            problems.append(f"Row {i}: missing customer — skipped")
            continue
        try:
            qty = int(float(r.get("quantity") or 0))
        except ValueError:
            qty = 0
            problems.append(f"Row {i}: bad quantity '{r.get('quantity')}' — set to 0")
        try:
            amount = float(r.get("amount") or 0)
        except ValueError:
            amount = 0.0
            problems.append(f"Row {i}: bad amount '{r.get('amount')}' — set to 0")
        if not r.get("quantity") or not r.get("amount"):
            problems.append(f"Row {i}: blank quantity/amount for {r.get('customer')} — needs checking")
        clean.append({
            "date": r.get("date", ""),
            "customer": r.get("customer", ""),
            "item": r.get("item", ""),
            "quantity": qty,
            "amount": amount,
            "status": r.get("status", "Open"),
        })
    return clean, problems


# ---------------------------------------------------------------------------
# 3. Make the 1-page Friday report
# ---------------------------------------------------------------------------

def make_friday_report(clean_rows, problems, week_label="Week of Nov 2, 2026"):
    """Build the Friday report as a dict. app.py shows this on screen,
    and a real build can also save it as a PDF / email it."""
    total_amount = sum(r["amount"] for r in clean_rows)
    total_qty = sum(r["quantity"] for r in clean_rows)
    open_rows = [r for r in clean_rows if r["status"].lower() == "open"]
    open_amount = sum(r["amount"] for r in open_rows)

    by_customer = defaultdict(float)
    for r in clean_rows:
        by_customer[r["customer"]] += r["amount"]
    top_customers = sorted(by_customer.items(), key=lambda x: -x[1])[:5]

    status_counts = Counter(r["status"] for r in clean_rows)

    return {
        "week": week_label,
        "generated": date.today().isoformat(),
        "total_orders": len(clean_rows),
        "total_quantity": total_qty,
        "total_amount": round(total_amount, 2),
        "open_orders": len(open_rows),
        "open_amount": round(open_amount, 2),
        "top_customers": [{"customer": c, "amount": round(a, 2)} for c, a in top_customers],
        "status_counts": dict(status_counts),
        "problems": problems,
        "rows": clean_rows,
    }


def print_report(report):
    print(f"FRIDAY REPORT — {report['week']}  (generated {report['generated']})")
    print(f"Total orders: {report['total_orders']}  |  Total qty: {report['total_quantity']}  |  Total amount: ${report['total_amount']:,.2f}")
    print(f"Open orders: {report['open_orders']}  |  Open amount: ${report['open_amount']:,.2f}")
    print("Top customers:")
    for c in report["top_customers"]:
        print(f"  - {c['customer']}: ${c['amount']:,.2f}")
    print(f"Status: {report['status_counts']}")
    if report["problems"]:
        print("Needs checking:")
        for p in report["problems"]:
            print(f"  - {p}")


# ---------------------------------------------------------------------------
# 4. Upload to BigQuery (stub — fill in before a real client run)
# ---------------------------------------------------------------------------

def upload_to_bigquery(clean_rows, project_id=None, dataset="wedosimplify", table="orders"):
    """TODO — fill this in for a real client:
    1. Set GCP_PROJECT_ID in your .env / GCP console.
    2. pip install google-cloud-bigquery (in requirements.txt).
    3. Uncomment the code below.
    4. Create the dataset/table in BigQuery first, or let load_table_from_json create it.
    Returns False for now so nothing is sent anywhere by accident.
    """
    if not project_id:
        print("BigQuery upload skipped: no GCP_PROJECT_ID set (stub).")
        print("TODO: set GCP_PROJECT_ID, then uncomment the BigQuery code in main.py.")
        return False
    # --- Uncomment for a real run ---
    # from google.cloud import bigquery
    # client = bigquery.Client(project=project_id)
    # table_id = f"{project_id}.{dataset}.{table}"
    # job = client.load_table_from_json(clean_rows, table_id)
    # job.result()
    # print(f"Uploaded {len(clean_rows)} rows to {table_id}")
    # return True
    return False


# ---------------------------------------------------------------------------
# Main — local sample run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        rows = read_excel_export(sys.argv[1])
    else:
        print("No file given — using sample data. Usage: python3 main.py export.csv")
        rows = read_sample_data()
    clean, problems = clean_data(rows)
    report = make_friday_report(clean, problems)
    print_report(report)
    upload_to_bigquery(clean, project_id=os.environ.get("GCP_PROJECT_ID"))
