Gothic II — Noc Kruka (Live Stats Companion)
A lightweight, real-time web HUD for Gothic II: Night of the Raven (Noc Kruka) that reads your character's memory stats directly from `Gothic2.exe` and serves a mobile-friendly, Gothic-themed dashboard over your local network.
Features
Real-Time Memory Reading: Polls `Gothic2.exe` every 0.5 seconds using `pymem` without modifying game files or affecting performance.
Live Character Metrics: Displays current/max Health, current/max Mana, Level, Learning Points (LP), and Experience (EXP) progress (including percentage and points remaining to the next level).
Instant Mobile Pairing: Automatically detects your local LAN IP and prints a scannable QR code directly in your terminal on startup.
Thematic Web UI: Styled with parchment tones, gold accents, and serif typography (`Cinzel` & `IM Fell English`), complete with tap-to-fullscreen support for mobile devices.
Auto-Reconnect: Automatically waits for the game to launch and reconnects if the game is restarted.
---
Prerequisites
OS: Windows (required for `pymem` process memory reading)
Game: Gothic II: Night of the Raven (`Gothic2.exe`)
Python: Python 3.8 or higher
Required Python Packages
Install the required dependencies using `pip`:
```bash
pip install flask pymem qrcode
```
---
Usage
Launch Gothic II and load your save game (or start the script first—it will wait until `Gothic2.exe` is detected).
Run the Python script (you may need to run your terminal as Administrator if `pymem` encounters permission errors reading process memory):
```bash
   python app.py
   ```
Connect your phone or tablet:
Ensure your mobile device is connected to the same Wi-Fi/LAN network as your PC.
Scan the QR code printed in the terminal with your phone's camera, or manually navigate to `http://<YOUR_PC_LAN_IP>:5000`.
Optional: Tap the top banner area on the webpage to enter fullscreen mode.
---
Configuration & Memory Offsets
The script is configured for standard Gothic II: Night of the Raven (`2.6` / Steam / GOG versions) memory addresses:
Setting / Offset	Value	Description
`PROCESS_NAME`	`"Gothic2.exe"`	Target executable name
`STATIC_PTR`	`0x8CECBC`	Static base pointer to the player object
`hp_cur`	`0x1B8`	Current Hit Points
`hp_max`	`0x1BC`	Maximum Hit Points
`mana_cur`	`0x1C0`	Current Mana
`mana_max`	`0x1C4`	Maximum Mana
`level`	`0x234`	Character Level
`exp`	`0x42C`	Current Experience Points
`next_lvl`	`0x430`	Experience required for next level
`lp`	`0x434`	Available Learning Points
> **Note:** If you are playing heavily modified total conversions or different executable versions where the base pointer differs, you may need to update `STATIC_PTR` accordingly.
---
API Endpoint
The Flask backend exposes a simple JSON endpoint if you wish to build custom overlays (e.g., for OBS Studio):
`GET /api/stats`
Returns the cached character stats:
```json
  {
    "hp_cur": 120,
    "hp_max": 120,
    "mana_cur": 30,
    "mana_max": 30,
    "level": 5,
    "exp": 7800,
    "next_lvl": 10500,
    "prev_level_exp": 7500,
    "lp": 15
  }
  ```
(Returns `{"error": "no data"}` when the game is not running or a save is not loaded.)
---
Troubleshooting
`Could not open process` / Access Denied: Run Command Prompt or PowerShell as Administrator before executing the script.
Phone cannot load the page:
Verify both devices are on the same local network.
Check Windows Defender Firewall and allow Python / port `5000` on Private networks.
