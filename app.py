"""
Farmer Procurement Slot Booking & Queue Management System
-----------------------------------------------------------
A working prototype: farmer registration, slot booking, live queue
tracking, mocked SMS/notifications, and procurement/payment status.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import sqlite3
from datetime import datetime, date, timedelta

from flask import Flask, g, render_template, request, redirect, url_for, flash, jsonify, session

from translations import t as translate, LANGUAGES

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel's application directory is read-only.
# /tmp is writable during a serverless execution.
if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/procurement.db"
else:
    DB_PATH = os.path.join(APP_DIR, "procurement.db")

SCHEMA_PATH = os.path.join(APP_DIR, "schema.sql")
app = Flask(__name__)
app.secret_key = "dev-secret-change-me"  # replace before any real deployment

STATUS_FLOW = ["BOOKED", "ARRIVED", "PROCURED", "PAID"]


def current_lang():
    return session.get("lang", "en")


def tr(key, **kwargs):
    """Shorthand: translate a key using the current session language."""
    return translate(key, current_lang(), **kwargs)


@app.context_processor
def inject_i18n():
    # Makes t(...) and lang available in every Jinja template automatically.
    return {"t": tr, "lang": current_lang(), "languages": LANGUAGES}


@app.context_processor
def inject_session_user():
    # Makes farmer/admin login state available in the nav on every page.
    return {
        "current_farmer_name": session.get("farmer_name"),
        "current_admin_email": session.get("admin_email"),
        "current_admin_center": session.get("admin_center_name"),
    }


@app.route("/set-language/<lang_code>")
def set_language(lang_code):
    if lang_code not in LANGUAGES:
        lang_code = "en"
    session["lang"] = lang_code
    return redirect(request.referrer or url_for("home"))


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    fresh = not os.path.exists(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    if fresh:
        with open(SCHEMA_PATH, "r") as f:
            db.executescript(f.read())
        db.commit()
    db.close()


def notify(db, farmer_id, message):
    """Mock SMS/app notification: logged to DB and printed to console.

    SWAP POINT: replace the db.execute + print below with a real call to
    Twilio / MSG91 / Fast2SMS etc. Everything else in the app already
    calls notify() at the right moments, so this is the only function
    you need to change to send real SMS.
    """
    db.execute(
        "INSERT INTO notifications (farmer_id, message) VALUES (?, ?)",
        (farmer_id, message),
    )
    print(f"[SMS MOCK] to farmer#{farmer_id}: {message}")


# ---------------------------------------------------------------------------
# Public: home / registration / booking
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    db = get_db()
    centers = db.execute("SELECT * FROM centers ORDER BY city, name").fetchall()

    # Group centres by city for a nicer home-page listing
    centers_by_city = {}
    for c in centers:
        centers_by_city.setdefault(c["city"], []).append(c)

    stats = {
        "total_farmers": db.execute("SELECT COUNT(*) c FROM farmers").fetchone()["c"],
        "total_centers": db.execute("SELECT COUNT(*) c FROM centers").fetchone()["c"],
        "total_cities": db.execute("SELECT COUNT(DISTINCT city) c FROM centers").fetchone()["c"],
        "total_bookings": db.execute("SELECT COUNT(*) c FROM bookings").fetchone()["c"],
    }

    return render_template(
        "home.html", centers_by_city=centers_by_city, stats=stats
    )


@app.route("/farmer-login", methods=["POST"])
def farmer_login():
    """Combined login/registration panel on the home page.

    If the phone number already exists, this logs the farmer in and takes
    them straight to booking. Otherwise it registers them on the spot.
    """
    db = get_db()
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    village = request.form.get("village", "").strip()

    if not (name and phone and village):
        flash(tr("flash_fill_all"), "error")
        return redirect(url_for("home") + "#farmer-panel")

    existing = db.execute("SELECT * FROM farmers WHERE phone = ?", (phone,)).fetchone()
    if existing:
        session["farmer_id"] = existing["id"]
        session["farmer_name"] = existing["name"]
        flash(tr("flash_already_registered"), "info")
        return redirect(url_for("book_slot", farmer_id=existing["id"]))

    cur = db.execute(
        "INSERT INTO farmers (name, phone, email, village) VALUES (?, ?, ?, ?)",
        (name, phone, email or None, village),
    )
    db.commit()
    farmer_id = cur.lastrowid
    session["farmer_id"] = farmer_id
    session["farmer_name"] = name
    flash(tr("flash_registered_ok"), "success")
    return redirect(url_for("book_slot", farmer_id=farmer_id))


@app.route("/farmer-logout")
def farmer_logout():
    session.pop("farmer_id", None)
    session.pop("farmer_name", None)
    return redirect(url_for("home"))


@app.route("/admin-login", methods=["POST"])
def admin_login():
    """Admin panel on the home page: identifies the admin by email + phone
    and the centre they manage (looked up by the centre's short code)."""
    db = get_db()
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    center_code = request.form.get("center_code", "").strip().upper()

    center = db.execute("SELECT * FROM centers WHERE code = ?", (center_code,)).fetchone()

    if not (email and phone and center):
        flash(tr("flash_admin_invalid"), "error")
        return redirect(url_for("home") + "#admin-panel")

    existing = db.execute(
        "SELECT * FROM admins WHERE email = ? AND center_id = ?", (email, center["id"])
    ).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO admins (name, email, phone, center_id) VALUES (?, ?, ?, ?)",
            (name or None, email, phone, center["id"]),
        )
        db.commit()

    session["admin_email"] = email
    session["admin_center_id"] = center["id"]
    session["admin_center_name"] = center["name"]
    flash(tr("flash_admin_welcome", center=center["name"]), "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_email", None)
    session.pop("admin_center_id", None)
    session.pop("admin_center_name", None)
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        email = request.form.get("email", "").strip()
        village = request.form["village"].strip()

        if not (name and phone and village):
            flash(tr("flash_fill_all"), "error")
            return redirect(url_for("register"))

        existing = db.execute(
            "SELECT * FROM farmers WHERE phone = ?", (phone,)
        ).fetchone()
        if existing:
            flash(tr("flash_already_registered"), "info")
            return redirect(url_for("book_slot", farmer_id=existing["id"]))

        cur = db.execute(
            "INSERT INTO farmers (name, phone, email, village) VALUES (?, ?, ?, ?)",
            (name, phone, email or None, village),
        )
        db.commit()
        farmer_id = cur.lastrowid
        session["farmer_id"] = farmer_id
        session["farmer_name"] = name
        flash(tr("flash_registered_ok"), "success")
        return redirect(url_for("book_slot", farmer_id=farmer_id))

    return render_template("register.html")


@app.route("/book/<int:farmer_id>", methods=["GET", "POST"])
def book_slot(farmer_id):
    db = get_db()
    farmer = db.execute("SELECT * FROM farmers WHERE id = ?", (farmer_id,)).fetchone()
    if not farmer:
        flash(tr("flash_farmer_not_found"), "error")
        return redirect(url_for("register"))

    centers = db.execute("SELECT * FROM centers").fetchall()

    if request.method == "POST":
        center_id = int(request.form["center_id"])
        slot_date = request.form["slot_date"]
        start_time = request.form["start_time"]
        crop_type = request.form["crop_type"]
        est_quantity = float(request.form["est_quantity"])

        # Find or create the slot bucket for this center/date/time
        slot = db.execute(
            """SELECT * FROM slots
               WHERE center_id=? AND slot_date=? AND start_time=?""",
            (center_id, slot_date, start_time),
        ).fetchone()

        if not slot:
            end_time = (
                datetime.strptime(start_time, "%H:%M") + timedelta(hours=1)
            ).strftime("%H:%M")
            cur = db.execute(
                """INSERT INTO slots (center_id, slot_date, start_time, end_time, capacity)
                   VALUES (?, ?, ?, ?, ?)""",
                (center_id, slot_date, start_time, end_time, 20),
            )
            slot_id = cur.lastrowid
            slot = db.execute("SELECT * FROM slots WHERE id=?", (slot_id,)).fetchone()

        booked_count = db.execute(
            "SELECT COUNT(*) c FROM bookings WHERE slot_id=? AND status != 'CANCELLED'",
            (slot["id"],),
        ).fetchone()["c"]

        if booked_count >= slot["capacity"]:
            flash(tr("flash_slot_full"), "error")
            return redirect(url_for("book_slot", farmer_id=farmer_id))

        token_number = booked_count + 1
        db.execute(
            """INSERT INTO bookings
               (farmer_id, slot_id, token_number, crop_type, est_quantity_kg, status)
               VALUES (?, ?, ?, ?, ?, 'BOOKED')""",
            (farmer_id, slot["id"], token_number, crop_type, est_quantity),
        )
        center = db.execute("SELECT * FROM centers WHERE id=?", (center_id,)).fetchone()
        notify(
            db,
            farmer_id,
            f"Slot confirmed at {center['name']} on {slot_date} {start_time}. "
            f"Your token is #{token_number}. Please arrive 10 min early.",
        )
        db.commit()
        return redirect(url_for("my_status", phone=farmer["phone"]))

    today = date.today().isoformat()
    return render_template("book_slot.html", farmer=farmer, centers=centers, today=today)


# ---------------------------------------------------------------------------
# Public: farmer self-service status lookup
# ---------------------------------------------------------------------------
@app.route("/status", methods=["GET"])
def my_status():
    db = get_db()
    phone = request.args.get("phone", "").strip()
    farmer = None
    bookings = []
    if phone:
        farmer = db.execute("SELECT * FROM farmers WHERE phone=?", (phone,)).fetchone()
        if farmer:
            bookings = db.execute(
                """SELECT b.*, s.slot_date, s.start_time, s.current_token, c.name AS center_name
                   FROM bookings b
                   JOIN slots s ON b.slot_id = s.id
                   JOIN centers c ON s.center_id = c.id
                   WHERE b.farmer_id = ?
                   ORDER BY b.created_at DESC""",
                (farmer["id"],),
            ).fetchall()
        else:
            flash(tr("flash_no_registration"), "error")

    notifications = []
    if farmer:
        notifications = db.execute(
            "SELECT * FROM notifications WHERE farmer_id=? ORDER BY id DESC LIMIT 10",
            (farmer["id"],),
        ).fetchall()

    return render_template(
        "status.html", farmer=farmer, bookings=bookings, notifications=notifications, phone=phone
    )


# ---------------------------------------------------------------------------
# Public: live queue display board (e.g. shown on a screen at the centre)
# ---------------------------------------------------------------------------
@app.route("/queue/<int:slot_id>")
def queue_board(slot_id):
    db = get_db()
    slot = db.execute(
        """SELECT s.*, c.name AS center_name FROM slots s
           JOIN centers c ON s.center_id = c.id WHERE s.id=?""",
        (slot_id,),
    ).fetchone()
    if not slot:
        flash(tr("flash_slot_not_found"), "error")
        return redirect(url_for("home"))

    bookings = db.execute(
        """SELECT b.*, f.name AS farmer_name FROM bookings b
           JOIN farmers f ON b.farmer_id = f.id
           WHERE b.slot_id=? AND b.status NOT IN ('CANCELLED')
           ORDER BY b.token_number""",
        (slot_id,),
    ).fetchall()
    return render_template("queue_board.html", slot=slot, bookings=bookings)


@app.route("/api/queue/<int:slot_id>")
def api_queue_status(slot_id):
    """JSON endpoint the queue board polls for near-real-time updates."""
    db = get_db()
    slot = db.execute("SELECT * FROM slots WHERE id=?", (slot_id,)).fetchone()
    if not slot:
        return jsonify({"error": "not found"}), 404
    bookings = db.execute(
        """SELECT b.token_number, b.status, f.name AS farmer_name
           FROM bookings b JOIN farmers f ON b.farmer_id = f.id
           WHERE b.slot_id=? AND b.status NOT IN ('CANCELLED')
           ORDER BY b.token_number""",
        (slot_id,),
    ).fetchall()
    return jsonify(
        {
            "current_token": slot["current_token"],
            "bookings": [dict(b) for b in bookings],
        }
    )


# ---------------------------------------------------------------------------
# Admin: dashboard, advance queue, update procurement/payment status
# ---------------------------------------------------------------------------
@app.route("/admin")
def admin_dashboard():
    db = get_db()
    slot_date = request.args.get("date", date.today().isoformat())
    admin_center_id = session.get("admin_center_id")

    if admin_center_id:
        # Logged-in admins only see slots for the centre they registered with.
        slots = db.execute(
            """SELECT s.*, c.name AS center_name,
                      (SELECT COUNT(*) FROM bookings b WHERE b.slot_id = s.id AND b.status != 'CANCELLED') AS booked_count
               FROM slots s JOIN centers c ON s.center_id = c.id
               WHERE s.slot_date = ? AND s.center_id = ?
               ORDER BY s.start_time""",
            (slot_date, admin_center_id),
        ).fetchall()
    else:
        # No admin session (e.g. direct nav during a demo) — show everything.
        slots = db.execute(
            """SELECT s.*, c.name AS center_name,
                      (SELECT COUNT(*) FROM bookings b WHERE b.slot_id = s.id AND b.status != 'CANCELLED') AS booked_count
               FROM slots s JOIN centers c ON s.center_id = c.id
               WHERE s.slot_date = ?
               ORDER BY c.name, s.start_time""",
            (slot_date,),
        ).fetchall()
    return render_template("admin_dashboard.html", slots=slots, slot_date=slot_date)


@app.route("/admin/slot/<int:slot_id>")
def admin_slot(slot_id):
    db = get_db()
    slot = db.execute(
        """SELECT s.*, c.name AS center_name FROM slots s
           JOIN centers c ON s.center_id = c.id WHERE s.id=?""",
        (slot_id,),
    ).fetchone()
    bookings = db.execute(
        """SELECT b.*, f.name AS farmer_name, f.phone FROM bookings b
           JOIN farmers f ON b.farmer_id = f.id
           WHERE b.slot_id=?
           ORDER BY b.token_number""",
        (slot_id,),
    ).fetchall()
    return render_template("admin_slot.html", slot=slot, bookings=bookings)


@app.route("/admin/slot/<int:slot_id>/call-next", methods=["POST"])
def call_next(slot_id):
    db = get_db()
    slot = db.execute("SELECT * FROM slots WHERE id=?", (slot_id,)).fetchone()
    next_token = slot["current_token"] + 1
    db.execute("UPDATE slots SET current_token=? WHERE id=?", (next_token, slot_id))

    # Mark the called farmer ARRIVED-ready, and give a heads-up to the next 2 in line
    current_booking = db.execute(
        "SELECT * FROM bookings WHERE slot_id=? AND token_number=?",
        (slot_id, next_token),
    ).fetchone()
    if current_booking:
        notify(
            db,
            current_booking["farmer_id"],
            f"It's your turn now (token #{next_token}). Please proceed to the counter.",
        )
    upcoming = db.execute(
        "SELECT * FROM bookings WHERE slot_id=? AND token_number=?",
        (slot_id, next_token + 2),
    ).fetchone()
    if upcoming:
        notify(
            db,
            upcoming["farmer_id"],
            f"Heads up: 2 tokens ahead of you (#{next_token}) now being served.",
        )
    db.commit()
    return redirect(url_for("admin_slot", slot_id=slot_id))


@app.route("/admin/booking/<int:booking_id>/status", methods=["POST"])
def update_booking_status(booking_id):
    db = get_db()
    new_status = request.form["status"]
    booking = db.execute("SELECT * FROM bookings WHERE id=?", (booking_id,)).fetchone()

    if new_status == "PROCURED":
        actual_qty = request.form.get("actual_quantity_kg")
        db.execute(
            "UPDATE bookings SET status=?, actual_quantity_kg=? WHERE id=?",
            (new_status, actual_qty, booking_id),
        )
        notify(
            db,
            booking["farmer_id"],
            f"Procurement done: {actual_qty} kg recorded for token #{booking['token_number']}. Payment pending.",
        )
    elif new_status == "PAID":
        amount = request.form.get("amount_paid")
        db.execute(
            "UPDATE bookings SET status=?, amount_paid=? WHERE id=?",
            (new_status, amount, booking_id),
        )
        notify(
            db,
            booking["farmer_id"],
            f"Payment of Rs. {amount} processed for token #{booking['token_number']}. Thank you!",
        )
    else:
        db.execute("UPDATE bookings SET status=? WHERE id=?", (new_status, booking_id))
        notify(db, booking["farmer_id"], f"Your booking status is now: {new_status}.")

    db.commit()
    return redirect(url_for("admin_slot", slot_id=booking["slot_id"]))


# ---------------------------------------------------------------------------
# Initialize the database when the application starts.
# This is required on Vercel because __main__ is not executed there.
init_db()

if __name__ == "__main__":
    app.run(debug=True)