## Task 0: Clarifying Questions

### Needs Stakeholder Input
1. **Duplicate Deals**: Several deal_ids appear multiple times (e.g., `D000017`, `D001523-R`, `D001976`). Should duplicates be removed, merged, or preserved as separate records?
2. **Deal Values**: Some deal_value entries are inconsistent — “Pending”, “TBD”, negative values, and mixed currencies ($, €, £). Should we standardize to USD or preserve original values?
3. **Customer Matching**: 162 deals have no matching customer record due to inconsistent naming (e.g., `Harvest Culinary LLC` vs `HARVEST CULINARY LLC`). Should we apply fuzzy matching or leave them orphaned?
4. **Contacts Structure**: Customers.json mixes `contacts` arrays, single `contact` objects, and `primary_contact_*` fields. Should we assume one primary contact per company or preserve all contacts?
5. **Blank Rows**: 12 rows in sales_pipeline.xlsx are completely empty. Should these be dropped or treated as placeholders?

### Derived from Dataset
- **Row Count**: 2,588 rows in sales_pipeline.xlsx after dropping blank rows.
- **Duplicates**: 61 duplicate deal_ids detected (some exact, some with suffixes like `-R`).
- **Dates**: Mixed formats — Excel serials, ISO strings, US/EU styles, and free‑text dates.
- **Customer Names**: Inconsistent casing in `customer_name` (e.g., `Harvest Culinary LLC` vs `HARVEST CULINARY LLC`).
- **Contacts**: Missing emails/phones in several customer records.

### Notes
- These clarifying questions were drafted after exploratory data checks.  
- Some questions (duplicates, currency standardization, orphaned deals) require stakeholder input.  
- Others (blank rows, date normalization, casing) were answered directly from the dataset and addressed in the ETL pipeline.
