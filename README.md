# Gothic II — Noc Kruka Live Stats Dashboard

A lightweight Flask web application that reads live character stats directly from the `Gothic2.exe` process memory and serves a mobile-friendly, Gothic-themed dashboard over your local network.

## Features

- **Real-Time Memory Reading:** Reads HP, Mana, Level, Experience, Next Level threshold, and Learning Points directly from `Gothic2.exe` using `pymem`.
- **Auto-Reconnect:** Automatically waits for `Gothic2.exe` on startup and reconnects if the game restarts or closes.
- **Mobile-Friendly HUD:** Styled with *Cinzel* and *IM Fell English* fonts, progress bars, and tap-to-fullscreen support for use as a second screen on your phone or tablet.
- **Instant QR Code Access:** Detects your local LAN IP and prints a scannable ASCII QR code directly in the terminal.

## Requirements

- Windows OS (required for `pymem` process memory reading)
- *Gothic II: Night of the Raven* (`Gothic2.exe`)

## Using

1. Download [Gothic2Overlay.exe](https://github.com/przemekNachel/Gothic2Overlay/releases/download/v1.0.6/Gothic2Overlay.exe) and run.
