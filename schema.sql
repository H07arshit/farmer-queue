-- Farmer Procurement Slot Booking & Queue Management
-- SQLite schema

DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS slots;
DROP TABLE IF EXISTS farmers;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS centers;

CREATE TABLE centers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,      -- short public ID, e.g. 'LKO-01', used by admins to log in
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    location TEXT NOT NULL,
    crop_types TEXT NOT NULL DEFAULT 'Wheat,Paddy,Maize'
);

CREATE TABLE farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT,
    village TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    center_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(email, center_id),
    FOREIGN KEY (center_id) REFERENCES centers(id)
);

CREATE TABLE slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_id INTEGER NOT NULL,
    slot_date TEXT NOT NULL,        -- 'YYYY-MM-DD'
    start_time TEXT NOT NULL,       -- 'HH:MM'
    end_time TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 20,
    current_token INTEGER NOT NULL DEFAULT 0,   -- last token called by admin ("now serving")
    FOREIGN KEY (center_id) REFERENCES centers(id)
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    token_number INTEGER NOT NULL,
    crop_type TEXT NOT NULL,
    est_quantity_kg REAL NOT NULL,
    actual_quantity_kg REAL,
    amount_paid REAL,
    status TEXT NOT NULL DEFAULT 'BOOKED',
    -- BOOKED -> ARRIVED -> PROCURED -> PAID  (or CANCELLED / NO_SHOW)
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (farmer_id) REFERENCES farmers(id),
    FOREIGN KEY (slot_id) REFERENCES slots(id)
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (farmer_id) REFERENCES farmers(id)
);

-- Seed 10 procurement centres across 3 cities so the app is realistic out of the box
INSERT INTO centers (code, name, city, location, crop_types) VALUES
    ('LKO-01', 'Chinhat Mandi',                  'Lucknow',  'Chinhat, Lucknow, UP',        'Wheat,Paddy,Sugarcane'),
    ('LKO-02', 'Malihabad Procurement Centre',   'Lucknow',  'Malihabad, Lucknow, UP',      'Mango,Wheat,Maize'),
    ('LKO-03', 'Alambagh Krishi Kendra',         'Lucknow',  'Alambagh, Lucknow, UP',       'Wheat,Paddy'),
    ('LKO-04', 'Gomti Nagar Extension Centre',   'Lucknow',  'Gomti Nagar, Lucknow, UP',    'Paddy,Maize,Pulses'),
    ('KNP-01', 'Kalyanpur Mandi',                'Kanpur',   'Kalyanpur, Kanpur, UP',       'Wheat,Paddy'),
    ('KNP-02', 'Ghatampur Procurement Centre',   'Kanpur',   'Ghatampur, Kanpur, UP',       'Sugarcane,Wheat'),
    ('KNP-03', 'Bilhaur Krishi Kendra',          'Kanpur',   'Bilhaur, Kanpur, UP',         'Maize,Pulses,Wheat'),
    ('VNS-01', 'Pindra Mandi',                   'Varanasi', 'Pindra, Varanasi, UP',        'Wheat,Paddy'),
    ('VNS-02', 'Ramnagar Procurement Centre',    'Varanasi', 'Ramnagar, Varanasi, UP',      'Paddy,Vegetables'),
    ('VNS-03', 'Rohania Krishi Kendra',          'Varanasi', 'Rohania, Varanasi, UP',       'Wheat,Maize');
