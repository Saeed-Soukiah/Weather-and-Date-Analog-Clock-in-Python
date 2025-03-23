# Analog Clock with Weather and Date Display

This project is a digital analog clock implemented using **Pygame**. The clock displays:
- Real-time **date**
- **Weather** information (temperature and condition)
- Smooth **second hand movement**
- **Hour** and **minute hands**
- **Light/Dark** theme switching based on time of day

## Features
- **Smooth second hand movement** using microseconds for smooth transitions.
- **Weather integration**: Fetches weather data using an external API (wttr.in).
- **Date display**: Shows the current date below the clock.
- **Customizable themes**: Automatically switches between **light** and **dark** modes based on the time of day.
- **Shadows & Glow effects**: Enhances the clock's appearance with shadows and glow effects on hands.
- **Clock hand animations**: Animated movement for hour, minute, and second hands.

## Requirements
To run this project, you'll need to install **Pygame** and **requests**.

1. Install Python 3 (if not already installed).
2. Install the required libraries:
   ```bash
   pip install pygame requests
