# Exterminator — Animated Website

This repository contains a single-page prototype site for the Exterminator antivirus UI.

Files:
- `project.html` — Main HTML file (open in browser)
- `styles.css` — Styling and animated visuals
- `script.js` — Canvas animation and scan simulation

Downloads:
- `downloads/exterminator-windows-installer.bat` — harmless demo Windows batch installer (placeholder)
- `downloads/exterminator-macos-installer.sh` — harmless demo macOS shell installer (placeholder)

These files are placeholders intended to test the website's download links. They do not install software and make no changes to your system. Replace them with your real, signed installers before distributing to users.

Proof-of-Concept Scanner
- `downloads/exterminator-antivirus-poc.py` — a safe Python PoC scanner that uses heuristics to identify suspicious files and can move them to a `quarantine/` folder after user confirmation. It is non-destructive by default.
- `downloads/README_installer.txt` — instructions to run the PoC scanner and optional packaging steps (PyInstaller).

GUI PoC:
- `downloads/exterminator_gui.py` — a Tkinter-based GUI wrapper around the PoC scanner. Choose a directory to scan, review findings in the UI, and move selected items into `quarantine/` after confirmation.

Running the GUI (PowerShell):
```powershell
Set-Location "C:\Users\DELL\OneDrive\Documents\Mind_Projects\downloads"
python .\exterminator_gui.py
```

Or use the included PowerShell launcher (Windows):
```powershell
Set-Location "C:\Users\DELL\OneDrive\Documents\Mind_Projects\downloads"
.\launch_exterminator.ps1
```

Packaging note:
- You can package the GUI into a single executable with PyInstaller. Run `pyinstaller --onefile exterminator_gui.py` locally and test the generated executable before distribution.

Packaging and creating a downloadable app

1) Quick ZIP (recommended for immediate downloads):
 - Run the included `build_zip.py` from the project root. This creates `exterminator_app.zip` containing the `downloads/` folder (GUI, launcher, instructions).
	 ```powershell
	 Set-Location "C:\Users\DELL\OneDrive\Documents\Mind_Projects"
	 python .\build_zip.py
	 ```
 - After creating `exterminator_app.zip`, the site `project.html` will allow users to download that ZIP directly (the Download button links to `exterminator_app.zip`).

2) Create a single executable (Windows):
 - Run `build_exe.ps1` on a Windows machine with Python and PyInstaller installed. That script runs PyInstaller and writes `exterminator_windows.zip` (contains the `dist/` exe).
	 ```powershell
	 Set-Location "C:\Users\DELL\OneDrive\Documents\Mind_Projects"
	 .\build_exe.ps1
	 ```
 - Sign and test the produced executable before distributing widely.

Notes:
- I cannot create signed executables or run PyInstaller for you from here. The packaging scripts above must be run on your machine (or CI) to produce real app files that users can download directly from the website.
- If you want, I can also add a `exterminator_app.zip` binary to the repo if you upload the built artifact, or I can prepare CI instructions to build the executable automatically.

Important safety note:
- This PoC is for demonstration only and is not a replacement for a professional antivirus product. Test only on non-production machines and replace with signed, tested installers before distributing.

How to run:
1. Open `project.html` in your browser (double-click or use "Open with" in your OS).
2. Use the "Run Quick Scan" or "Run Full Scan" buttons to see the canvas animation and progress simulation.

Notes & next steps:
- The canvas animation is illustrative — replace with real telemetry/visuals in an actual product.
- To make the site production-ready: add build tooling, accessibility checks, real download links, and server-side delivery.
- If you want, I can add a dark/light theme switch, Lottie-based micro-animations, or an animated SVG logo.

