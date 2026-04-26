import pandas as pd
import sqlite3
import json
import re

# -----------------------------
# Helper functions
# -----------------------------

def clean_deal_value(val):
    """Normalize deal_value: blanks → None (NULL in SQLite)"""
    try:
        if val is None or pd.isna(val) or str(val).strip() == "":
            return None
        val_str = str(val).strip()
        val_str = re.sub(r'[\$,€£]', '', val_str).replace(',', '')
        if val_str.lower() in ["pending", "tbd", "nan", "none"]:
            return None
        num = float(val_str)
        return num if num >= 0 else None
    except:
        return None

def clean_date(val):
    if pd.isna(val) or val is None or str(val).strip() == "":
        return None
    val_str = str(val).strip()
    try:
        if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", val_str):
            parsed = pd.to_datetime(val_str, format="%Y-%m-%dT%H:%M:%S", errors="coerce")
        elif re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", val_str):
            parsed = pd.to_datetime(val_str, format="%Y-%m-%d %H:%M:%S", errors="coerce")
        elif re.match(r"\d{2}/\d{2}/\d{4}", val_str):
            parsed = pd.to_datetime(val_str, format="%d/%m/%Y", errors="coerce")
        elif re.match(r"\d{2}/\d{2}/\d{4}", val_str):
            parsed = pd.to_datetime(val_str, format="%m/%d/%Y", errors="coerce")
        else:
            parsed = pd.to_datetime(val_str, errors="coerce")
        if pd.isna(parsed):
            return None
        return parsed.strftime("%Y-%m-%d")
    except:
        return None


def normalize_name(name):
    """Normalize abbreviations, blanks → None (NULL in SQLite)"""
    if not name or str(name).strip() == "":
        return None
    name = str(name).strip().title()
    replacements = {
        r"\bCo\b": "Company",
        r"\bInc\b\.?": "Incorporated",
        r"\bLlc\b\.?": "Limited Liability Company",
        r"\bLtd\b\.?": "Limited",
        r"& Sons": "And Sons"
    }
    for pattern, repl in replacements.items():
        name = re.sub(pattern, repl, name, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", name).strip()

# -----------------------------
# Load raw data
# -----------------------------

sales_df = pd.read_excel("sales_pipeline.xlsx")
customers_raw = json.load(open("customers.json"))

# Drop fully blank rows
sales_df = sales_df.dropna(how="all")

# -----------------------------
# Clean sales pipeline
# -----------------------------

deals_list = []
for _, row in sales_df.iterrows():
    prob_val = row.get("probability")
    if prob_val is None or pd.isna(prob_val) or str(prob_val).strip() == "":
        prob_clean = None
    else:
        try:
            prob_clean = int(prob_val)
        except (ValueError, TypeError):
            prob_clean = None

    cust_name_clean = normalize_name(row.get("customer_name"))

    deals_list.append((
        str(row.get("deal_id")) if row.get("deal_id") else None,
        cust_name_clean,
        row.get("rep_name") if row.get("rep_name") else None,
        clean_deal_value(row.get("deal_value")),
        row.get("stage") if row.get("stage") else None,
        prob_clean,
        clean_date(row.get("created_date")),
        clean_date(row.get("expected_close_date")),
        row.get("region") if row.get("region") else None,
        row.get("product_sku") if row.get("product_sku") else None,
    ))

# -----------------------------
# Clean customers.json
# -----------------------------

customers_list = []
contacts_list = []

for cust in customers_raw:
    company_name_clean = normalize_name(cust.get("company_name"))

    customers_list.append((
        cust.get("id") if cust.get("id") else None,
        company_name_clean,
        cust.get("tier") if cust.get("tier") else None,
        clean_date(cust.get("created_at")),
        cust.get("street") if cust.get("street") else None,
        cust.get("city") if cust.get("city") else None,
        cust.get("state") if cust.get("state") else None,
        cust.get("zip") if cust.get("zip") else None
    ))

    if "contacts" in cust and isinstance(cust["contacts"], list):
        for c in cust["contacts"]:
            contacts_list.append((
                cust.get("id") if cust.get("id") else None,
                c.get("name") if c.get("name") else None,
                c.get("email") if c.get("email") else None,
                c.get("phone") if c.get("phone") else None,
                c.get("title") if c.get("title") else None
            ))
    elif "contact" in cust and isinstance(cust["contact"], dict):
        c = cust["contact"]
        contacts_list.append((
            cust.get("id") if cust.get("id") else None,
            c.get("name") if c.get("name") else None,
            c.get("email") if c.get("email") else None,
            c.get("phone") if c.get("phone") else None,
            c.get("title") if c.get("title") else None
        ))
    elif "primary_contact_name" in cust:
        contacts_list.append((
            cust.get("id") if cust.get("id") else None,
            cust.get("primary_contact_name") if cust.get("primary_contact_name") else None,
            cust.get("primary_contact_email") if cust.get("primary_contact_email") else None,
            cust.get("primary_contact_phone") if cust.get("primary_contact_phone") else None,
            "Primary"
        ))

# -----------------------------
# Create SQLite schema
# -----------------------------

conn = sqlite3.connect("sales_customers.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    tier TEXT,
    created_at TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    name TEXT,
    email TEXT,
    phone TEXT,
    title TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS deals (
    deal_id TEXT PRIMARY KEY,
    customer_name TEXT,
    rep_name TEXT,
    deal_value REAL,
    stage TEXT,
    probability INTEGER,
    created_date TEXT,
    expected_close_date TEXT,
    region TEXT,
    product_sku TEXT
)
""")

cur.executemany("INSERT OR REPLACE INTO customers VALUES (?,?,?,?,?,?,?,?)", customers_list)
cur.executemany("INSERT INTO contacts (customer_id, name, email, phone, title) VALUES (?,?,?,?,?)", contacts_list)
cur.executemany("INSERT OR REPLACE INTO deals VALUES (?,?,?,?,?,?,?,?,?,?)", deals_list)

conn.commit()

# -----------------------------
# Export distinct orphaned customer names
# -----------------------------

query = """
SELECT DISTINCT d.customer_name AS excel_customer_name
FROM deals d
LEFT JOIN customers c
       ON d.customer_name = c.company_name
WHERE c.id IS NULL
"""

orphaned_names_df = pd.read_sql_query(query, conn)

output_path = r"C:/Users/vaish/Downloads/Advenshure Projects/orphaned_deals_distinct.xlsx"
orphaned_names_df.to_excel(output_path, index=False)

print(f"Distinct orphaned customer names exported to: {output_path}")

# -----------------------------
# Validation queries
# -----------------------------

# Orphaned deals (row count)
cur.execute("""
SELECT COUNT(*) 
FROM deals d
LEFT JOIN customers c 
       ON d.customer_name = c.company_name
WHERE c.id IS NULL
""")
orphaned_count = cur.fetchone()[0]

# Invalid probabilities
cur.execute("""
SELECT COUNT(*) 
FROM deals 
WHERE probability NOT IN (0,10,25,50,75,100) 
  AND probability IS NOT NULL
""")
invalid_prob_count = cur.fetchone()[0]

# Deals by stage
cur.execute("""
SELECT stage, COUNT(*) 
FROM deals 
GROUP BY stage
""")
stage_counts = cur.fetchall()

print("Validation Results:")
print("Orphaned deals:", orphaned_count)
print("Invalid probabilities:", invalid_prob_count)
print("Deals by stage:", stage_counts)

# Export validation results to Excel
validation_df = pd.DataFrame({
    "Metric": ["Orphaned deals", "Invalid probabilities"] + [f"Stage: {s[0]}" for s in stage_counts],
    "Count": [orphaned_count, invalid_prob_count] + [s[1] for s in stage_counts]
})

validation_output = r"C:/Users/vaish/Downloads/Advenshure Projects/validation_results.xlsx"
validation_df.to_excel(validation_output, index=False)

print(f"Validation results exported to: {validation_output}")


conn.close()
