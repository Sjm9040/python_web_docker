from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword",
    port="5433"
)
cur = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")

        try:
            # Start a new transaction
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()  # Commit the transaction if no errors
        except Exception as e:
            conn.rollback()  # Roll back the transaction if an error occurs
            print(f"An error occurred: {e}")
            return "Registration failed. Please try again."  # Return an error message

        return redirect(url_for('login'))  # Redirect to the login page after successful registration

    return render_template('register.html')  # Render the registration form


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")

        try:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return "Invalid credentials"  # Return an error message
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred during login. Please try again later."  # Return a generic error message

    return render_template('login.html')  # Render the login form


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
