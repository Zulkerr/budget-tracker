import sqlite3

def calculate_total_expenses():
    # Verbindung zur Datenbank öffnen
    connection = sqlite3.connect("budget_tracker.db")
    cursor = connection.cursor()

    # Gesamtausgaben berechnen
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    # Verbindung schließen
    connection.close()

    # Falls keine Ausgaben vorhanden sind, total auf 0 setzen
    if total is None:
        total = 0.0

    return total

if __name__ == "__main__":
    total = calculate_total_expenses()
    print(f"Die Gesamtausgaben betragen: {total} EUR")