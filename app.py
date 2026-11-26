"""
WeDoSimplify — Streamlit client report UI template.
One page, one client. Copy this file with the project folder for each
new client and change only the client name, week label, and data source.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

No GCP credentials are needed for the sample-data view.
For a real client, replace read_sample_data() with read_excel_export()
from main.py, or with a BigQuery read.
"""

import streamlit as st

from main import clean_data, make_friday_report, read_sample_data

CLIENT_NAME = "Sample Client — Acme Packaging (SAMPLE DATA)"
WEEK_LABEL = "Week of Nov 2, 2026"

st.set_page_config(page_title="Friday Report — WeDoSimplify", layout="wide")
st.title(f"Friday Report — {CLIENT_NAME}")
st.caption(f"{WEEK_LABEL}  •  Built by WeDoSimplify, Detroit  •  Your Excel / ERP stays — this reads your export")

rows = read_sample_data()
clean, problems = clean_data(rows)
report = make_friday_report(clean, problems, week_label=WEEK_LABEL)

# --- Top numbers ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total orders", report["total_orders"])
col2.metric("Total amount", f"${report['total_amount']:,.2f}")
col3.metric("Open orders", report["open_orders"])
col4.metric("Open amount", f"${report['open_amount']:,.2f}")

st.divider()

# --- Top customers (bar chart, built-in — no extra library needed) ---
st.subheader("Top customers this week")
top = {c["customer"]: c["amount"] for c in report["top_customers"]}
st.bar_chart(top)

# --- Orders table ---
st.subheader("Orders")
st.dataframe(report["rows"], use_container_width=True)

# --- Manual-work findings ---
st.subheader("Manual-work findings — what to fix first")
st.write(
    "1. **Open orders are not chased.** "
    f"{report['open_orders']} orders are still open, worth ${report['open_amount']:,.2f}. "
    "Fix first: a daily open-orders list, emailed each morning.\n\n"
    "2. **Blank quantities / amounts.** "
    "One row in the sample has a blank quantity and amount — in a real export "
    "this is the re-typing error the audit finds. Fix: flag blanks at entry, "
    "do not let the row move forward.\n\n"
    "3. **Friday report is made by hand.** "
    "This page replaces that manual copy-paste. Fix: run this report "
    "automatically every Friday from the same export."
)

if problems:
    st.subheader("Needs checking")
    for p in problems:
        st.warning(p)
else:
    st.success("No problems found in this export.")

st.divider()
st.caption(
    "Sample data only — replace with the client's export before showing a client. "
    "Generated: " + report["generated"]
)
