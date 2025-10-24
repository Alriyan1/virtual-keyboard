# 🎹 Virtual Keyboard (hand-tracking) — README

An easy-to-run virtual keyboard that uses webcam hand tracking to type using finger gestures. The app maps fingertip presence and a simple pinch/bring-motion to hover/click keyboard keys and sends keystrokes via `pynput`.

---

## 🚀 Quick overview

- Main script: `main.py` — uses `handtrackmodule.handDetector` to get hand landmarks and bounding boxes, draws an on-screen keyboard overlay, and sends keyboard events when a click gesture is detected.
- Layout: QWERTY rows with a wide `SPACE` and enlarged backspace (`<-`) key. Visual hover and click effects are drawn with OpenCV.

## 🧩 Features

- Real-time webcam-based keyboard overlay (mirror view).
- Hover and click visual feedback for keys.
- Sends keystrokes to the OS using `pynput.keyboard.Controller`.
- Simple, readable code intended for experimentation and enhancements.

## ✅ Requirements

- Python 3.8+ (3.10 recommended)
- Packages (install with pip):
  - `opencv-python`
  - `pynput`

Note: The repository expects a `handtrackmodule.py` file that exposes a `handDetector` class with at least these methods:
- `findHands(img)` — processes the image and optionally draws landmarks.
- `findPosition(img)` — returns `(lmlist, bbox)` where `lmlist` contains landmarks indexed by landmark id and each landmark entry is indexable: `[id, x, y]` (or similar), and `bbox` is a list of bounding boxes per hand.
- `finddistance(a, b, img, lmlist, draw=True)` — returns the euclidean distance between two landmarks `a` and `b` (used for detecting the click gesture).

If your `handtrackmodule.py` differs, adapt readouts in `main.py` accordingly.

## 🛠 Installation (PowerShell)

```powershell
# Create and activate a virtual environment
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# Install runtime deps
pip install opencv-python pynput
```

Alternatively, add a `requirements.txt` file and run `pip install -r requirements.txt`.

## ▶️ Run

1. Ensure your webcam is plugged in and not used by other apps.
2. From the project folder run:

```powershell
python "d:\projects\virtual_keyboard\main.py"
```

3. Use your index fingertip (landmark 8) to hover over keys. Pinch/bring the thumb+index (or reduce the distance between landmarks 8 and 12) to trigger a click. Press `q` in the OpenCV window to exit.

Note: `pynput` sends keystrokes to the focused application. If you want to type into a text field, focus the target app (or leave a text editor open) before performing clicks.

## 🔎 How it works (technical)

1. Capture frames from webcam using OpenCV (`cv2.VideoCapture(0)`), flip horizontally for a mirror view.
2. The `handDetector` processes the frame and returns landmark lists and bounding boxes.
3. The script builds an on-screen keyboard with `Button` objects and draws them using `cv2.rectangle` + `cv2.putText`.
4. For each frame, the script checks whether landmark 8 (index fingertip) is within a button's rectangle:
   - If so, it draws a hover state.
   - It calls `finddistance(8, 12, ...)` to calculate the distance between index fingertip and middle fingertip (or whichever landmarks your detector uses). If the distance < threshold (50 px by default), this is interpreted as a click.
5. On click, the script uses `pynput.keyboard.Controller().press()` to emit the corresponding key and appends the character to `finalText` (an on-screen typed text preview).

## ⚙️ Configuration & tuning

- Click distance threshold: currently `length < 50` px. Change this value to tweak sensitivity for your camera and position.
- Key and layout size: `key_w`, `key_h`, `spacing`, and offsets at the top of `main.py` determine layout and can be adjusted to fit different camera resolutions.
- Backspace key size and SPACE bar size are configurable when creating `Button` objects.
- Add a small cooldown sleep (already present via `time.sleep(0.2)`) to avoid accidental rapid repeat clicks. Adjust if needed.

## 🧰 Troubleshooting

- No keys react / no hand detected:
  - Verify `handtrackmodule.py` is present and that `handDetector.findPosition()` returns a valid `lmlist`.
  - Ensure adequate lighting and a non-cluttered background.
- Keystrokes not sent to target app:
  - Make sure the app you want to type into has focus (click into a text editor first).
  - On Windows, UAC or elevated permissions may interfere — try running the script with the same privilege level as the target app.
- False positives or unreliable clicks:
  - Increase the click threshold, or add a requirement that the index fingertip remains inside the key for N consecutive frames.
  - Switch to a different landmark pair for click detection (e.g., index vs thumb) depending on your hand detector.
- High CPU usage / low FPS:
  - Reduce frame size (cap.set(3, ...), cap.set(4, ...)) or throttle processing (skip frames).

## ♻️ Suggested improvements (ideas)

- Add an argument parser (`argparse`) to expose options: camera index, click-threshold, cooldown, and window scale.
- Replace simple pixel-threshold click with a small gesture detector (e.g., velocity of index tip toward a key) to reduce false triggers.
- Implement a short debounce/hysteresis state machine: require the finger to be inside the key for N frames to register hover, and then a separate N' frames for a click.
- Add lowercase/uppercase toggle (Shift/Shift lock) and support for symbols.
- Add a test mode that doesn't send OS keystrokes but prints the intended key to console — useful while debugging permissions.
- Export a small calibration helper to compute a comfortable `length` threshold for your webcam and distance.

## 🔐 Security & permissions

`pynput` emits OS-level keystrokes. Be mindful of what application is focused. Never run this while a password field is focused.

## 📎 A short checklist for a reliable run

- [ ] Close other webcam-using apps
- [ ] Focus a text editor to receive keys
- [ ] Ensure `handtrackmodule.py` is compatible
- [ ] Tune the click threshold for your setup

---

