from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route("/")
def index():
       # Verbindung zur Datenbank öffnen
       connection = sqlite3.connect("budget_tracker.db")
       cursor = connection.cursor()

       # Daten abrufen
       cursor.execute("SELECT * FROM expenses")
       rows = cursor.fetchall()

       # Verbindung schließen
       connection.close()

       return f"<h1>Ausgaben</h1><ul>{''.join([f'<li>{row[1]}: {row[2]} EUR am {row[3]}</li>' for row in rows])}</ul>"

if __name__ == "__main__":
       app.run(debug=True)