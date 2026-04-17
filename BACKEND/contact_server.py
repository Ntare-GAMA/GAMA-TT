from flask import Flask, request, send_from_directory
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')

# -------------------------------------------------------
# DATABASE CONFIG — fill in your SmarterASP.NET MySQL details
# (found in your hosting control panel under MySQL Databases)
# -------------------------------------------------------
DB_CONFIG = {
    'host':     'mysql5045.site4now.net',          # usually localhost on SmarterASP.NET
    'user':     'ac8302_intare',
    'password': 'Zxcvbnm@12',
    'database': 'db_ac8302_intare'
}


def save_to_db(name, organisation, email, area, message):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            name         VARCHAR(255),
            organisation VARCHAR(255),
            email        VARCHAR(255),
            area         VARCHAR(255),
            message      TEXT,
            submitted_at DATETIME
        )
    """)
    cursor.execute("""
        INSERT INTO contacts (name, organisation, email, area, message, submitted_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, organisation, email, area, message, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()


def save_to_file(name, organisation, email, area, message):
    """Fallback: write submission to a plain-text log."""
    log_path = os.path.join(os.path.dirname(__file__), 'contacts_log.txt')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(
            f"{datetime.now().isoformat()} | {name} | {organisation} "
            f"| {email} | {area} | {message}\n"
        )


@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')


@app.route('/contact', methods=['POST'])
def contact():
    name         = request.form.get('name', '').strip()
    organisation = request.form.get('organisation', '').strip()
    email        = request.form.get('email', '').strip()
    area         = request.form.get('area', '').strip()
    message      = request.form.get('message', '').strip()

    # Try MySQL first; fall back to file if DB isn't configured yet
    try:
        save_to_db(name, organisation, email, area, message)
    except Exception:
        save_to_file(name, organisation, email, area, message)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta http-equiv="refresh" content="4;url=/" />
  <title>Message Sent — GAMA TT</title>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{font-family:'Inter',sans-serif;background:#0A0A0A;color:#fff;
          display:flex;align-items:center;justify-content:center;min-height:100vh;}}
    .card{{text-align:center;padding:48px 60px;border:1px solid rgba(201,168,76,0.3);border-radius:12px;}}
    h2{{font-size:28px;color:#C9A84C;margin-bottom:12px;}}
    p{{color:rgba(255,255,255,0.6);line-height:1.7;}}
  </style>
</head>
<body>
  <div class="card">
    <h2>Thank you, {name}!</h2>
    <p>Your message has been received.<br/>We'll be in touch soon.<br/><br/>
       Redirecting you back in a moment…</p>
  </div>
</body>
</html>"""


if __name__ == '__main__':
    app.run(debug=False)
