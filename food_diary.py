import sqlite3
from datetime import datetime
import os

DB_NAME = "food_diary.db"

def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            calories INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(food_name, calories=None):
    """Log a new food entry."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (food_name, calories) VALUES (?, ?)', (food_name, calories))
    conn.commit()
    conn.close()
    print(f"Logged: {food_name} ({calories if calories else 'No'} calories)")

def view_entries():
    """Display all logged entries and show daily totals."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get all entries
    cursor.execute('SELECT id, food_name, calories, timestamp FROM entries ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    
    # Get daily totals
    cursor.execute('''
        SELECT DATE(timestamp) as day, SUM(calories) 
        FROM entries 
        WHERE calories IS NOT NULL 
        GROUP BY day 
        ORDER BY day DESC
    ''')
    totals = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("Your food diary is empty.")
        return

    print("\n--- Daily Totals ---")
    for day, total in totals:
        print(f"{day}: {total} kcal total")

    print("\n--- Food Diary Entries ---")
    for row in rows:
        dt = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        readable_time = dt.strftime('%Y-%m-%d %I:%M %p')
        print(f"ID: {row[0]} | [{readable_time}] {row[1]} - {row[2] if row[2] else 'N/A'} kcal")

def delete_entry(entry_id):
    """Delete an entry by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    if cursor.rowcount > 0:
        print(f"Entry {entry_id} deleted successfully.")
    else:
        print(f"No entry found with ID {entry_id}.")
    conn.commit()
    conn.close()

def search_entries(query):
    """Search for specific food items."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, food_name, calories, timestamp FROM entries WHERE food_name LIKE ? ORDER BY timestamp DESC', (f'%{query}%',))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print(f"No entries found matching '{query}'.")
        return

    print(f"\n--- Search Results for '{query}' ---")
    for row in rows:
        dt = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        readable_time = dt.strftime('%Y-%m-%d %I:%M %p')
        print(f"ID: {row[0]} | [{readable_time}] {row[1]} - {row[2] if row[2] else 'N/A'} kcal")

def export_report():
    """Export the diary to a text file."""
    filename = f"food_diary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, food_name, calories FROM entries ORDER BY timestamp ASC')
    rows = cursor.fetchall()
    conn.close()
    
    with open(filename, 'w') as f:
        f.write("FOOD DIARY REPORT\n")
        f.write("="*30 + "\n")
        for row in rows:
            f.write(f"[{row[0]}] {row[1]} - {row[2] if row[2] else 'N/A'} kcal\n")
    
    print(f"Report exported to {filename}")

def main():
    init_db()
    while True:
        print("\n1. Add Entry")
        print("2. View History & Totals")
        print("3. Search Food")
        print("4. Delete Entry")
        print("5. Export Report")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            food = input("What did you eat? ")
            cals = input("Calories (optional, press Enter to skip): ")
            add_entry(food, int(cals) if cals.isdigit() else None)
        elif choice == '2':
            view_entries()
        elif choice == '3':
            query = input("Search for: ")
            search_entries(query)
        elif choice == '4':
            eid = input("Enter the ID of the entry to delete: ")
            if eid.isdigit():
                delete_entry(int(eid))
            else:
                print("Invalid ID.")
        elif choice == '5':
            export_report()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
