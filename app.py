from flask import Flask, render_template, request, redirect, session, url_for, flash, abort, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def require_login():
    return "user_id" in session

@app.route("/")
def index():
    db = get_db()
    # Include reviews.user_id so we can show edit/delete only to the owner
    reviews = db.execute("""
        SELECT reviews.id, reviews.title, reviews.rating, reviews.content, reviews.date,
               reviews.user_id, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        ORDER BY reviews.id DESC
    """).fetchall()
    return render_template("index.html", reviews=reviews)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if len(username) < 3:
            flash("Username is too short.")
            return redirect(url_for("register"))
        if len(password) < 6:
            flash("Password is too short.")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("That username is taken.")
            return redirect(url_for("register"))

        flash("Account created. Log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welcome, {user['username']}!")
            return redirect(url_for("index"))


        flash("Wrong username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/add", methods=["GET", "POST"])
def add_review():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        try:
            rating = int(request.form["rating"])
        except ValueError:
            rating = 0

        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.")
            return redirect(url_for("add_review"))

        db = get_db()
        db.execute("""
            INSERT INTO reviews (title, rating, content, date, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (title, rating, content, date.today().isoformat(), session["user_id"]))
        db.commit()

        return redirect(url_for("index"))

    return render_template("add_review.html")

# --- Edit review (owner only) ---
@app.route("/review/<int:review_id>/edit", methods=["GET", "POST"])
def edit_review(review_id):
    if not require_login():
        return redirect(url_for("login"))

    db = get_db()
    review = db.execute("""
        SELECT id, title, rating, content, date, user_id
        FROM reviews
        WHERE id = ?
    """, (review_id,)).fetchone()

    if not review:
        abort(404)

    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        try:
            rating = int(request.form["rating"])
        except ValueError:
            rating = 0

        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.")
            return redirect(url_for("edit_review", review_id=review_id))

        db.execute("""
            UPDATE reviews
            SET title = ?, rating = ?, content = ?
            WHERE id = ? AND user_id = ?
        """, (title, rating, content, review_id, session["user_id"]))
        db.commit()

        flash("Review updated.")
        return redirect(url_for("index"))

    return render_template("edit_review.html", review=review)

# --- Delete review (owner only) ---
@app.route("/review/<int:review_id>/delete", methods=["POST"])
def delete_review(review_id):
    if not require_login():
        return redirect(url_for("login"))

    db = get_db()
    db.execute("DELETE FROM reviews WHERE id = ? AND user_id = ?", (review_id, session["user_id"]))
    db.commit()

    flash("Review deleted.")
    return redirect(url_for("index"))

@app.route("/offline")
def offline():
    return render_template("offline.html")

@app.route("/manifest.webmanifest")
def manifest():
    return send_from_directory("static", "manifest.webmanifest", mimetype="application/manifest+json")


if __name__ == "__main__":
    app.run(debug=True)
