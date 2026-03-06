"""
config.py — Central configuration for the Free Fire Guild Glory Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHERE TO PUT YOUR IDs — SUMMARY
────────────────────────────────
| What              | Where to edit              | Variable name     |
|-------------------|----------------------------|-------------------|
| Guild / Clan ID   | this file  (config.py)     | GUILD_ID          |
| Guild / Clan Name | this file  (config.py)     | GUILD_NAME        |
| Bot account UIDs  | this file  (config.py)     | BOT_ACCOUNTS list |
|   …or in file…    | accs.txt / spidey.txt      | (JSON)            |
| Target player UID | sent at runtime via /glori | command argument  |

The bot listens in guild chat for the command:
    /glori <player_uid>
and then spams squad-join requests to that player.
The guild/clan chat channel ID is derived from GUILD_ID automatically.
"""

# ═══════════════════════════════════════════════
#  ★  PASTE YOUR GUILD ID HERE  ★
#  (the numeric ID shown in your Free Fire guild page)
# ═══════════════════════════════════════════════
GUILD_ID: str = "YOUR_GUILD_ID_HERE"
# Example: GUILD_ID = "3161100693"

# ═══════════════════════════════════════════════
#  ★  PASTE YOUR GUILD NAME HERE  ★
# ═══════════════════════════════════════════════
GUILD_NAME: str = "YOUR_GUILD_NAME_HERE"
# Example: GUILD_NAME = "XR-GLORY"

# ═══════════════════════════════════════════════
#  ★  BOT ACCOUNT UIDs & PASSWORDS  ★
#
#  Each entry must have:
#    "uid"      → Garena guest account UID  (numeric string)
#    "password" → Garena guest token password (hex string)
#
#  You can add as many accounts as you want.
#  Alternatively, keep them in accs.txt (list format) or spidey.txt (dict format).
# ═══════════════════════════════════════════════
BOT_ACCOUNTS = [
    {
        "uid": "YOUR_BOT_UID_1",
        "password": "YOUR_BOT_PASSWORD_1"
    },
    # Add more accounts below:
    # {
    #     "uid": "4224256496",
    #     "password": "BY_XRSUPER-WBKQMILV9-XRRRR"
    # },
]

# ═══════════════════════════════════════════════
#  Additional settings (optional)
# ═══════════════════════════════════════════════

# Free Fire region (IND = India, ME = Middle East, etc.)
REGION: str = "IND"

# Number of squad-join spam requests sent per /glori command
SPAM_COUNT: int = 8000

# Delay (seconds) between each spam request
SPAM_DELAY: float = 0.1
