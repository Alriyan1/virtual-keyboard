# Dr. Strange Mystical Shield

A real-time interactive application that creates a dynamic Dr. Strange-style mystical shield using hand gestures and computer vision. This project uses OpenCV and MediaPipe for hand tracking to generate an elaborate magical shield effect that responds to hand movements.

## Features

- Real-time hand gesture tracking
- Dynamic shield size control using two hands
- Elaborate mystical shield design including:
  - Outer and inner runic text rings
  - Concentric circles with golden patterns
  - Nested rotating squares
  - Star mandala pattern
  - Central mandala with cross patterns
  - Mystical energy particles with glow effects
- Smooth animation with continuous rotation
- Responsive shield size based on hand distance

## Requirements

```
opencv-python
mediapipe
numpy
```

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install opencv-python mediapipe numpy
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Hand Gestures:
   - Show your palm with all fingers spread to create the shield
   - Use your second hand's index finger to control the shield size:
     - Move index fingers closer together: smaller shield
     - Move index fingers apart: larger shield

3. Controls:
   - Press `ESC` to exit the application

## How it Works

The application uses:
- MediaPipe for hand landmark detection
- OpenCV for image processing and visualization
- Custom geometric patterns and animations for the shield effect
- Distance-based size control between hand landmarks

The shield consists of multiple layers:
1. Outer runic text ring with 48 characters
2. Inner runic text ring with 36 characters
3. Concentric circles with varying thicknesses
4. Nested rotating squares at different angles
5. Eight-pointed star mandala pattern
6. Central mandala with intricate details
7. Dynamic particle effects

## Files

- `main.py` - Main application script with shield generation logic
- `handtrackmodule.py` - Hand tracking module using MediaPipe

## Credits

This project is inspired by the mystical shields seen in "Doctor Strange" and implements a real-time interactive version using computer vision technology.