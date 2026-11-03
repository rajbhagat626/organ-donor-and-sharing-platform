import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.get_db().execute(
                'SELECT * FROM users WHERE id = ?', (user_id,)
            ).fetchone()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            blood_type = request.form.get('blood_type')
            organ_type = request.form.get('organ_type')
            medical_history = request.form.get('medical_history')

            database = db.get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not role:
                error = 'Role is required.'

            if error is None:
                try:
                    database.execute(
                        "INSERT INTO users (username, password_hash, role, blood_type, organ_type, medical_history) VALUES (?, ?, ?, ?, ?, ?)",
                        (username, generate_password_hash(password), role, blood_type, organ_type, medical_history),
                    )
                    database.commit()
                except database.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    return redirect(url_for('login'))

            flash(error)

        return render_template('register.html')

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            database = db.get_db()
            error = None
            user = database.execute(
                'SELECT * FROM users WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password_hash'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                if user['role'] == 'donor':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('search'))

            flash(error)

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route('/dashboard', methods=('GET', 'POST'))
    def dashboard():
        if g.user is None or g.user['role'] != 'donor':
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            blood_type = request.form.get('blood_type')
            organ_type = request.form.get('organ_type')
            medical_history = request.form.get('medical_history')
            database = db.get_db()
            database.execute(
                'UPDATE users SET blood_type = ?, organ_type = ?, medical_history = ? WHERE id = ?',
                (blood_type, organ_type, medical_history, g.user['id'])
            )
            database.commit()
            flash('Profile updated successfully.')
            return redirect(url_for('dashboard'))

        return render_template('dashboard.html')

    @app.route('/search', methods=('GET', 'POST'))
    def search():
        if g.user is None or g.user['role'] != 'hospital':
            return redirect(url_for('login'))

        matches = []
        if request.method == 'POST':
            blood_type = request.form.get('blood_type')
            organ_type = request.form.get('organ_type')
            database = db.get_db()
            
            # Basic matching logic: same blood type and organ type
            # Note: In a real app, blood type compatibility (e.g., O- is universal donor) is more complex.
            query = 'SELECT * FROM users WHERE role = "donor"'
            params = []
            
            if blood_type:
                query += ' AND blood_type = ?'
                params.append(blood_type)
            if organ_type:
                query += ' AND organ_type = ?'
                params.append(organ_type)
                
            matches = database.execute(query, params).fetchall()

        return render_template('search.html', matches=matches)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
