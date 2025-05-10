import sqlite3
from datetime import datetime

# Funktion: Verbindung zur Datenbank herstellen
def connect_to_db():
    connection = sqlite3.connect("budget_tracker.db")
    return connection

# Funktion: Tabellen erstellen
def create_tables():
    connection = connect_to_db()
    cursor = connection.cursor()

    # Tabelle expenses erstellen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()
    print("Tabellen wurden erfolgreich erstellt!")

# Duplikation checken
def expense_exists(description, amount, date):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM expenses 
    WHERE description = ? AND amount = ? AND date = ?
    """, (description, amount, date))
    exists = cursor.fetchone()[0] > 0
    connection.close()
    return exists

# Funktion: Daten einfügen
def insert_expense(description, amount, date):
    if expense_exists(description, amount, date):
        print(f"Die Ausgabe '{description}' existiert bereits!")
        return
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO expenses (description, amount, date)
    VALUES (?, ?, ?)
    """, (description, amount, date))

    connection.commit()
    connection.close()
    print(f"Ausgabe '{description}' wurde erfolgreich hinzugefügt!")

# Funktion: Gesamtausgaben berechnen
def calculate_total_expenses():
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    connection.close()
    return total

# Funktion: Alle Ausgaben anzeigen
def fetch_expenses():
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    connection.close()
    return rows

# Funktion zur Eingabe des Datums
def get_input_date():
    today = datetime.now().date()
    date_input = input(f"Datum der Ausgabe (YYYY-MM-DD, Standard ist heute: {today}): ")
    if not date_input:
        return today.strftime("%Y-%m-%d")  # Standard auf heute setzen
    return date_input

# Funktion zur Eingabe der Ausgaben mit Kategorie
def insert_expense_with_category():
    categories = ["Einkauf", "Miete", "Unterhaltung", "Sonstiges"]
    print("Wähle eine Kategorie:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    category_choice = int(input("Gib die Nummer der Kategorie ein: ")) - 1
    description = categories[category_choice]
    amount = float(input("Betrag der Ausgabe: "))
    date = get_input_date()
    insert_expense(description, amount, date)

# Hauptprogramm
if __name__ == "__main__":
    create_tables()
    
    while True:
        insert_expense_with_category()
        if input("Möchtest du eine weitere Ausgabe hinzufügen? (j/n): ").lower() != 'j':
            break

    # Alle Ausgaben anzeigen
    print("Liste der Ausgaben:")
    for row in fetch_expenses():
        print(f"ID: {row[0]}, Beschreibung: {row[1]}, Betrag: {row[2]}, Datum: {row[3]}")

