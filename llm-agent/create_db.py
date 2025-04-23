import sqlite3


# ----- Step 1: Build SQLite Database -----
db_file = "demo_db.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create 'employees' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary REAL NOT NULL,
    department TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    performance_rating INTEGER NOT NULL CHECK(performance_rating BETWEEN 1 AND 10)
)
""")

# Insert sample employee data
employees = [
    ("Alice Johnson", 75000, "Engineering", "2018-06-15", 9),
    ("Bob Smith", 80000, "Marketing", "2019-09-23", 7),
    ("Charlie Evans", 65000, "Sales", "2020-01-10", 6),
    ("David Brown", 90000, "Engineering", "2016-12-05", 10),
    ("Eva Davis", 72000, "HR", "2021-05-30", 8),
    ("Frank Moore", 85000, "Finance", "2017-03-25", 9),
    ("Grace Lee", 78000, "IT", "2015-11-12", 7),
    ("Hannah Wilson", 82000, "Engineering", "2022-08-18", 8),
    ("Isaac Turner", 87000, "Marketing", "2014-07-02", 10),
    ("Jackie Harris", 66000, "Sales", "2023-02-01", 5)
]
cursor.executemany(
    "INSERT INTO employees (name, salary, department, hire_date, performance_rating) VALUES (?, ?, ?, ?, ?)",
    employees
)
conn.commit()
conn.close()

print(f"Created SQLite database '{db_file}' with employee data.")