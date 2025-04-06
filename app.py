from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename

from priority_nlp import prioritize_issue  # NLP-based priority classifier
from utils.classifier import classify_image  # Optional: image classification

# Flask App Config
app = Flask(__name__)
app.secret_key = "secret"  # Change this in production!

# Upload Config
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sql@1234',  # Update this securely in production
    'database': 'civicpulse'
}

# --------------------- Routes ---------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/report', methods=['GET', 'POST'])
def user_report():
    if request.method == 'POST':
        description = request.form.get('description', '')
        image = request.files.get('image')

        # Handle file upload
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            image_path = None
            filename = ''

        # AI logic
        issue_type = classify_image(filename) if filename else 'General'
        priority = prioritize_issue(description)

        # Insert into DB
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO issues (description, image_path, issue_type, priority, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (description, image_path, issue_type, priority, 'Pending'))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('status'))

    return render_template('user_complaint.html')

@app.route('/status')
def status():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM issues ORDER BY id DESC")
        issues = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template('status.html', issues=issues)

@app.route('/authority/dashboard', methods=['GET', 'POST'])
def authority_dashboard():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Update issue status if POST
        if request.method == 'POST':
            issue_id = request.form.get('issue_id')
            new_status = request.form.get('status')
            if issue_id and new_status:
                cursor.execute("UPDATE issues SET status = %s WHERE id = %s", (new_status, issue_id))
                conn.commit()

        # Fetch issues sorted by priority
        cursor.execute("SELECT * FROM issues ORDER BY FIELD(priority, 'Urgent', 'High', 'Medium', 'Low')")
        issues = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template('authority_dashboard.html', issues=issues)

# -------------------- Main --------------------

if __name__ == '__main__':
    app.run(debug=True)
