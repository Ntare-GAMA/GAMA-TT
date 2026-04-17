
# --- Imports ---
from flask import Flask, request, jsonify, send_from_directory
import pathlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# --- Flask App ---
app = Flask(__name__)

# --- Static File Routes ---
@app.route('/')
def serve_index():
    project_root = pathlib.Path(app.root_path).parent
    return send_from_directory(str(project_root), 'index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    project_root = pathlib.Path(app.root_path).parent
    assets_dir = project_root / 'assets'
    return send_from_directory(str(assets_dir), filename)

@app.route('/<path:filename>')
def serve_static(filename):
    project_root = pathlib.Path(app.root_path).parent
    return send_from_directory(str(project_root), filename)

# --- Email Configuration ---
EMAIL_ADDRESS = 'intoreestate@gmail.com'  # Your receiving email
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Set this as an environment variable for security
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# --- Contact Route ---
@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    name = data.get('name')
    organisation = data.get('organisation')
    email = data.get('email')
    area = data.get('area')
    message = data.get('message')

    # Compose email
    subject = f'New Contact Form Submission from {name}'
    body = f"""
    Name: {name}
    Organisation: {organisation}
    Email: {email}
    Area of Interest: {area}
    Message: {message}
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        if not EMAIL_PASSWORD:
            raise Exception('EMAIL_PASSWORD environment variable is not set.')
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()
        return jsonify({'success': True, 'message': 'Message sent successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# --- MySQL Database (optional, only if mysql-connector-python is installed) ---
try:
    import mysql.connector
    DB_CONFIG = {
        'host': 'mysql5045.site4now.net',
        'user': 'ac8302_intare',
        'password': 'Zxcvbnm@12',
        'database': 'db_ac8302_intare'
    }
    def get_db_connection():
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
except ImportError:
    print('mysql-connector-python is not installed. Database functions will not work.')

if __name__ == '__main__':
    app.run(debug=True)
