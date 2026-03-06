"""
app.py — Flask entry point for Vercel deployment
This is the file referenced in vercel.json as the WSGI handler.

HOW TO CONFIGURE YOUR BOT IDs:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. GUILD / CLAN ID  → Set GUILD_ID below (the numeric ID of your Free Fire guild)
2. GUILD / CLAN NAME → Set GUILD_NAME below
3. PLAYER IDs (bot accounts) → Edit the ACCOUNTS list below with your uid + password pairs,
   OR keep them in accs.txt / spidey.txt and they will be loaded automatically.

The bot accounts (uid + password) used by the bots are currently hard-coded
at the bottom of main.py inside the __main__ block:
    FF_CLIENT(id="4372592494", password="3082AE84...")
You can replace those values there, or set them via the ACCOUNTS list here
and the /start route will pick them up.
"""

import os
import json
import threading
from flask import Flask, jsonify, request

# ─────────────────────────────────────────────
#  ★  CONFIGURE YOUR IDs HERE  ★
# ─────────────────────────────────────────────

# Your Free Fire Guild / Clan numeric ID
# Example: GUILD_ID = "3161100693"
GUILD_ID = "3048840679"

# Your Guild / Clan display name
GUILD_NAME = "ᴾᴿᴵᴹᴱ⚡Yᴀᴅᴀᴠs"

# Bot accounts — list of {"uid": "...", "password": "..."}
# You can also leave this empty and edit accs.txt instead.
# The password here is the Garena guest-token password (hex string).
ACCOUNTS = [
     {"uid": "4356405620", "password": "4D969CF89C99524D8A24DC0F34182C68C33C61F1B86B69CA5A4A263F1DD2C42A"},
    # {"uid": "4224256579", "password": "BY_XRSUPER-GZEJNCIXA-XRRRR"},
]

# ─────────────────────────────────────────────
#  Flask app
# ─────────────────────────────────────────────
app = Flask(__name__)

# Keep track of running bot threads so we don't double-start
_bot_threads: list[threading.Thread] = []


def _load_accounts_from_file():
    """Try to load accounts from accs.txt or spidey.txt if ACCOUNTS list is empty."""
    accs = list(ACCOUNTS)  # copy configured accounts

    for filename in ("accs.txt", "spidey.txt"):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    # accs.txt format: [{"uid": "...", "password": "..."}, ...]
                    accs.extend(data)
                elif isinstance(data, dict):
                    # spidey.txt format: {"uid": "password", ...}
                    for uid, pwd in data.items():
                        accs.append({"uid": uid, "password": pwd})
            except Exception as e:
                app.logger.warning(f"Could not load {filename}: {e}")

    return accs


@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "guild_id": GUILD_ID,
        "guild_name": GUILD_NAME,
        "message": "Free Fire Guild Glory Bot is running. Use /start to launch bots.",
    })


@app.route("/start", methods=["GET", "POST"])
def start_bots():
    """Launch one bot thread per configured account."""
    # Import here so Vercel only imports when the route is hit
    try:
        from main import FF_CLIENT
    except Exception as e:
        return jsonify({"error": f"Failed to import FF_CLIENT: {e}"}), 500

    accounts = _load_accounts_from_file()
    if not accounts:
        return jsonify({
            "error": "No accounts configured. Edit ACCOUNTS in app.py or add entries to accs.txt."
        }), 400

    launched = []
    for acc in accounts:
        uid = str(acc.get("uid", ""))
        password = str(acc.get("password", ""))
        if not uid or not password:
            continue
        t = threading.Thread(
            target=_run_client,
            args=(uid, password),
            daemon=True,
            name=f"bot-{uid}",
        )
        t.start()
        _bot_threads.append(t)
        launched.append(uid)

    return jsonify({
        "status": "started",
        "guild_id": GUILD_ID,
        "guild_name": GUILD_NAME,
        "bots_launched": launched,
    })


@app.route("/status")
def status():
    alive = [t.name for t in _bot_threads if t.is_alive()]
    dead  = [t.name for t in _bot_threads if not t.is_alive()]
    return jsonify({
        "alive_bots": alive,
        "dead_bots": dead,
        "guild_id": GUILD_ID,
        "guild_name": GUILD_NAME,
    })


@app.route("/health")
def health():
    return jsonify({"ok": True})


# ─────────────────────────────────────────────
#  Internal helpers
# ─────────────────────────────────────────────

def _run_client(uid: str, password: str):
    """Target function for each bot thread."""
    try:
        from main import FF_CLIENT
        client = FF_CLIENT(id=uid, password=password)
        client.start()
    except Exception as e:
        print(f"[ERROR] Bot {uid} crashed: {e}")


# ─────────────────────────────────────────────
#  Vercel / local entry-point
# ─────────────────────────────────────────────
# Vercel looks for a module-level `app` (WSGI callable) — that's the Flask
# instance defined above. No `if __name__ == "__main__"` block needed on
# Vercel, but we keep one for local testing:

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
