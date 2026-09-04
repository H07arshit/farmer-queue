"""
Simple in-memory translation store for the Farmer Procurement Portal.
No external i18n library needed for a prototype of this size — just a
dict-of-dicts and a t(key, lang, **kwargs) lookup with .format() support.

To add a new language: copy the "en" block, translate every value, and
add the language code to LANGUAGES below + the toggle in base.html.
"""

LANGUAGES = {"en": "English", "hi": "हिंदी"}

TRANSLATIONS = {
    "en": {
        # common / nav
        "brand": "🌾 Kisan Procurement Portal",
        "nav_register": "Register & Book",
        "nav_status": "My Status",
        "nav_admin": "Admin",
        "footer_note": "Prototype — SMS notifications are simulated (see server console).",

        # home
        "hero_title": "Skip the line at the procurement centre",
        "hero_desc": "Register once, book a slot at your nearest centre, and track your queue position, procurement, and payment — all in one place.",
        "btn_register": "Register & Book a Slot",
        "btn_status": "Check My Status",
        "centres_heading": "Procurement Centres",
        "accepts_label": "Accepts",

        # register
        "register_heading": "Farmer Registration",
        "label_name": "Full Name",
        "label_phone": "Phone Number",
        "label_village": "Village / Town",
        "placeholder_phone": "10-digit mobile number",
        "btn_continue": "Continue to Slot Booking",
        "already_registered_note": "Already registered? Just enter your phone number on the My Status page instead.",

        # booking
        "book_heading": "Book a Procurement Slot",
        "welcome": "Welcome",
        "label_centre": "Procurement Centre",
        "label_date": "Date",
        "label_time": "Preferred Time Slot",
        "label_crop": "Crop Type",
        "crop_placeholder": "e.g. Wheat",
        "label_qty": "Estimated Quantity (kg)",
        "btn_confirm": "Confirm Booking",
        "slot_note": "Each slot has a capacity of 20 farmers. If a slot is full, pick another time — this is what keeps the centre from getting crowded.",

        # status
        "status_heading": "Check My Status",
        "btn_lookup": "Look Up",
        "bookings_heading": "Bookings for {name}",
        "th_centre": "Centre",
        "th_date": "Date",
        "th_time": "Time",
        "th_your_token": "Your Token",
        "th_now_serving": "Now Serving",
        "th_crop": "Crop",
        "th_status": "Status",
        "th_queue_board": "Queue Board",
        "view_link": "View",
        "no_bookings": "No bookings yet.",
        "notifications_heading": "Recent Notifications",
        "no_notifications": "No notifications yet.",

        # queue board
        "now_serving": "Now Serving",
        "th_token": "Token",
        "th_farmer": "Farmer",

        # admin dashboard
        "admin_heading": "Admin Dashboard",
        "th_booked_capacity": "Booked / Capacity",
        "btn_manage": "Manage",
        "btn_queue_board_link": "Queue Board",
        "no_slots": "No slots booked for this date yet.",

        # admin slot
        "call_next_btn": "Call Next Token (now #{n})",
        "th_phone": "Phone",
        "th_est_qty": "Est. Qty",
        "th_actual_qty": "Actual Qty (kg)",
        "th_amount": "Amount (₹)",
        "th_update": "Update",
        "btn_mark_arrived": "Mark Arrived",
        "btn_mark_procured": "Mark Procured",
        "btn_mark_paid": "Mark Paid",
        "placeholder_actual_qty": "Actual kg",
        "placeholder_amount": "Amount ₹",
        "complete_label": "Complete",

        # flash messages
        "flash_fill_all": "Please fill all fields.",
        "flash_already_registered": "You're already registered — proceeding to slot booking.",
        "flash_registered_ok": "Registered successfully!",
        "flash_farmer_not_found": "Farmer not found. Please register again.",
        "flash_slot_full": "That slot is full. Please pick a different time — this keeps crowding at the centre under control.",
        "flash_no_registration": "No registration found for that phone number.",
        "flash_slot_not_found": "Slot not found.",
        "flash_admin_invalid": "Please enter a valid email, phone, and centre ID.",
        "flash_admin_welcome": "Logged in as admin for {center}.",

        # home page: stats + login panels
        "stats_farmers": "Registered Farmers",
        "stats_centers": "Procurement Centres",
        "stats_cities": "Cities Covered",
        "stats_bookings": "Slots Booked",
        "farmer_panel_heading": "Farmer Login / Register",
        "farmer_panel_desc": "Enter your details to book a slot or check your queue status. New here? This also registers you.",
        "admin_panel_heading": "Admin Login",
        "admin_panel_desc": "Centre staff: enter your details and your centre ID to manage today's queue.",
        "label_email": "Email Address",
        "placeholder_email": "you@example.com",
        "label_center_name": "Centre",
        "label_center_id": "Centre ID",
        "placeholder_center_id": "e.g. LKO-01",
        "btn_farmer_continue": "Continue",
        "btn_admin_continue": "Login to Dashboard",
        "logged_in_as": "Logged in as",
        "logout": "Logout",
        "nearby_centers_heading": "Our Procurement Centres",
    },
    "hi": {
        # common / nav
        "brand": "🌾 किसान खरीद पोर्टल",
        "nav_register": "पंजीकरण करें",
        "nav_status": "मेरी स्थिति",
        "nav_admin": "एडमिन",
        "footer_note": "प्रोटोटाइप — SMS सूचनाएं सिम्युलेट की गई हैं (सर्वर कंसोल देखें)।",

        # home
        "hero_title": "खरीद केंद्र पर लाइन में लगने से बचें",
        "hero_desc": "एक बार पंजीकरण करें, अपने नज़दीकी केंद्र पर स्लॉट बुक करें, और अपनी कतार की स्थिति, खरीद और भुगतान — सब कुछ एक ही जगह ट्रैक करें।",
        "btn_register": "पंजीकरण करें और स्लॉट बुक करें",
        "btn_status": "मेरी स्थिति जांचें",
        "centres_heading": "खरीद केंद्र",
        "accepts_label": "स्वीकार्य फसलें",

        # register
        "register_heading": "किसान पंजीकरण",
        "label_name": "पूरा नाम",
        "label_phone": "फ़ोन नंबर",
        "label_village": "गांव / कस्बा",
        "placeholder_phone": "10 अंकों का मोबाइल नंबर",
        "btn_continue": "स्लॉट बुकिंग जारी रखें",
        "already_registered_note": "पहले से पंजीकृत हैं? बस 'मेरी स्थिति' पेज पर अपना फ़ोन नंबर दर्ज करें।",

        # booking
        "book_heading": "खरीद स्लॉट बुक करें",
        "welcome": "स्वागत है",
        "label_centre": "खरीद केंद्र",
        "label_date": "तारीख",
        "label_time": "पसंदीदा समय स्लॉट",
        "label_crop": "फसल का प्रकार",
        "crop_placeholder": "जैसे गेहूं",
        "label_qty": "अनुमानित मात्रा (किलो)",
        "btn_confirm": "बुकिंग की पुष्टि करें",
        "slot_note": "प्रत्येक स्लॉट में 20 किसानों की क्षमता है। यदि कोई स्लॉट भरा हुआ है, तो कृपया दूसरा समय चुनें — इससे केंद्र पर भीड़ नियंत्रित रहती है।",

        # status
        "status_heading": "मेरी स्थिति जांचें",
        "btn_lookup": "खोजें",
        "bookings_heading": "{name} की बुकिंग",
        "th_centre": "केंद्र",
        "th_date": "तारीख",
        "th_time": "समय",
        "th_your_token": "आपका टोकन",
        "th_now_serving": "अभी सेवा में",
        "th_crop": "फसल",
        "th_status": "स्थिति",
        "th_queue_board": "कतार बोर्ड",
        "view_link": "देखें",
        "no_bookings": "अभी तक कोई बुकिंग नहीं।",
        "notifications_heading": "हाल की सूचनाएं",
        "no_notifications": "अभी तक कोई सूचना नहीं।",

        # queue board
        "now_serving": "अभी सेवा में",
        "th_token": "टोकन",
        "th_farmer": "किसान",

        # admin dashboard
        "admin_heading": "एडमिन डैशबोर्ड",
        "th_booked_capacity": "बुक / क्षमता",
        "btn_manage": "प्रबंधित करें",
        "btn_queue_board_link": "कतार बोर्ड",
        "no_slots": "इस तारीख के लिए अभी तक कोई स्लॉट बुक नहीं हुआ।",

        # admin slot
        "call_next_btn": "अगला टोकन बुलाएं (अभी #{n})",
        "th_phone": "फ़ोन",
        "th_est_qty": "अनुमानित मात्रा",
        "th_actual_qty": "वास्तविक मात्रा (किलो)",
        "th_amount": "राशि (₹)",
        "th_update": "अपडेट करें",
        "btn_mark_arrived": "पहुंचा हुआ चिह्नित करें",
        "btn_mark_procured": "खरीदा हुआ चिह्नित करें",
        "btn_mark_paid": "भुगतान हुआ चिह्नित करें",
        "placeholder_actual_qty": "वास्तविक किलो",
        "placeholder_amount": "राशि ₹",
        "complete_label": "पूर्ण",

        # flash messages
        "flash_fill_all": "कृपया सभी फ़ील्ड भरें।",
        "flash_already_registered": "आप पहले से पंजीकृत हैं — स्लॉट बुकिंग की ओर बढ़ रहे हैं।",
        "flash_registered_ok": "सफलतापूर्वक पंजीकृत!",
        "flash_farmer_not_found": "किसान नहीं मिला। कृपया फिर से पंजीकरण करें।",
        "flash_slot_full": "यह स्लॉट भरा हुआ है। कृपया दूसरा समय चुनें — इससे केंद्र पर भीड़ नियंत्रित रहती है।",
        "flash_no_registration": "उस फ़ोन नंबर के लिए कोई पंजीकरण नहीं मिला।",
        "flash_slot_not_found": "स्लॉट नहीं मिला।",
        "flash_admin_invalid": "कृपया मान्य ईमेल, फ़ोन और सेंटर ID दर्ज करें।",
        "flash_admin_welcome": "{center} के एडमिन के रूप में लॉगिन हुआ।",

        # home page: stats + login panels
        "stats_farmers": "पंजीकृत किसान",
        "stats_centers": "खरीद केंद्र",
        "stats_cities": "शहर शामिल",
        "stats_bookings": "बुक किए गए स्लॉट",
        "farmer_panel_heading": "किसान लॉगिन / पंजीकरण",
        "farmer_panel_desc": "स्लॉट बुक करने या अपनी कतार स्थिति जांचने के लिए विवरण दर्ज करें। नए हैं? इससे आपका पंजीकरण भी हो जाएगा।",
        "admin_panel_heading": "एडमिन लॉगिन",
        "admin_panel_desc": "केंद्र कर्मचारी: आज की कतार प्रबंधित करने के लिए अपना विवरण और सेंटर ID दर्ज करें।",
        "label_email": "ईमेल पता",
        "placeholder_email": "you@example.com",
        "label_center_name": "केंद्र",
        "label_center_id": "सेंटर ID",
        "placeholder_center_id": "जैसे LKO-01",
        "btn_farmer_continue": "जारी रखें",
        "btn_admin_continue": "डैशबोर्ड में लॉगिन करें",
        "logged_in_as": "इस रूप में लॉगिन",
        "logout": "लॉगआउट",
        "nearby_centers_heading": "हमारे खरीद केंद्र",
    },
}


def t(key, lang="en", **kwargs):
    """Look up `key` in the given language, falling back to English,
    then to the raw key itself if truly missing. Supports .format(**kwargs)
    for strings with placeholders like {name} or {n}."""
    text = TRANSLATIONS.get(lang, {}).get(key)
    if text is None:
        text = TRANSLATIONS["en"].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
