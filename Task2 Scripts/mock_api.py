import pandas as pd

def fetch_data():
    # Simulated API response with 20 rows
    data = [
        {"id": "U001", "name": "Alice", "email": "alice@example.com", "address": "123 Main St", "createdAt": "2024-01-01"},
        {"id": "U002", "name": "Bob", "email": "bob@example.com", "address": "456 Oak Ave", "createdAt": "2024-02-01"},
        {"id": "U003", "name": "Charlie", "email": "charlie@example.com", "address": "789 Pine Rd", "createdAt": "2024-03-01"},
        {"id": "U004", "name": "Diana", "email": "diana@example.com", "address": "101 Maple Blvd", "createdAt": "2024-04-01"},
        {"id": "U005", "name": "Ethan", "email": "ethan@example.com", "address": "202 Birch Ln", "createdAt": "2024-05-01"},
        {"id": "U006", "name": "Fiona", "email": "fiona@example.com", "address": "303 Cedar Ct", "createdAt": "2024-06-01"},
        {"id": "U007", "name": "George", "email": "george@example.com", "address": "404 Walnut St", "createdAt": "2024-07-01"},
        {"id": "U008", "name": "Hannah", "email": "hannah@example.com", "address": "505 Chestnut Ave", "createdAt": "2024-08-01"},
        {"id": "U009", "name": "Ian", "email": "ian@example.com", "address": "606 Spruce Dr", "createdAt": "2024-09-01"},
        {"id": "U010", "name": "Julia", "email": "julia@example.com", "address": "707 Elm St", "createdAt": "2024-10-01"},
        {"id": "U011", "name": "Kevin", "email": "kevin@example.com", "address": "808 Poplar Rd", "createdAt": "2024-11-01"},
        {"id": "U012", "name": "Laura", "email": "laura@example.com", "address": "909 Magnolia Blvd", "createdAt": "2024-12-01"},
        {"id": "U013", "name": "Michael", "email": "michael@example.com", "address": "111 Cypress Ln", "createdAt": "2025-01-01"},
        {"id": "U014", "name": "Nina", "email": "nina@example.com", "address": "222 Redwood Ct", "createdAt": "2025-02-01"},
        {"id": "U015", "name": "Oscar", "email": "oscar@example.com", "address": "333 Palm St", "createdAt": "2025-03-01"},
        {"id": "U016", "name": "Paula", "email": "paula@example.com", "address": "444 Willow Ave", "createdAt": "2025-04-01"},
        {"id": "U017", "name": "Quentin", "email": "quentin@example.com", "address": "555 Fir Dr", "createdAt": "2025-05-01"},
        {"id": "U018", "name": "Rachel", "email": "rachel@example.com", "address": "666 Aspen St", "createdAt": "2025-06-01"},
        {"id": "U019", "name": "Sam", "email": "sam@example.com", "address": "777 Oakwood Rd", "createdAt": "2025-07-01"},
        {"id": "U020", "name": "Tina", "email": "tina@example.com", "address": "888 Maplewood Blvd", "createdAt": "2025-08-01"},
    ]
    return pd.DataFrame(data)
