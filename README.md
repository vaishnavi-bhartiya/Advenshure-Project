## Task 0: Clarifying Questions

### Needs Stakeholder Input
1. Duplicate deals (e.g., `D000017`, `D001523-R`, `D001976`) — should they be removed, merged, or preserved?  
2. Deal values include “Pending”, “TBD”, negative numbers, and mixed currencies ($, €, £). Should we standardize to USD or preserve original?  
3. 162 orphaned deals exist due to inconsistent naming (e.g., `Harvest Culinary LLC` vs `HARVEST CULINARY LLC`). Should we apply fuzzy matching or leave them unmatched?  
4. Customers.json mixes `contacts` arrays, single `contact` objects, and `primary_contact_*` fields. Should we assume one primary contact per company or preserve all?  
5. 12 blank rows in sales_pipeline.xlsx — should these be dropped or treated as placeholders?  

### Derived from Dataset
- **Row Count**: 2,588 rows in sales_pipeline.xlsx after dropping blank rows.
- **Duplicates**: 61 duplicate deal_ids detected (some exact, some with suffixes like `-R`).
- **Dates**: Mixed formats — Excel serials, ISO strings, US/EU styles, and free‑text dates.
- **Customer Names**: Inconsistent casing in `customer_name` (e.g., `Harvest Culinary LLC` vs `HARVEST CULINARY LLC`).
- **Contacts**: Missing emails/phones in several customer records.  
