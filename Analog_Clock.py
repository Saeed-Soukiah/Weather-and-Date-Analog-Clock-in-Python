# ===========================================================
# Author: Saeed Soukiah
# Date: 2025-03-23
# Purpose: Create an analog clock with real-time weather integration and date display.
# Features: 
# - Smooth second hand movement
# - Date and weather display
# - Automatic theme switching (light/dark mode)
# ===========================================================

import pygame
import pygame.gfxdraw
from datetime import datetime
import math
import requests

# Define the light and dark themes for the clock
THEMES = {
    "light": {  # Light theme colors
        "background": (225, 239, 240),
        "face_outer": (45, 45, 45),
        "face_middle": (229, 229, 229),
        "face_inner": (255, 255, 255),
        "hand_hour": (45, 45, 45),
        "hand_minute": (45, 45, 45),
        "hand_second": (255, 0, 0),
        "mark_color": (45, 45, 45),
        "shadow": (0, 0, 0, 50),
        "text_color": (0, 0, 0)
    },
    "dark": {  # Dark theme colors
        "background": (30, 30, 30),
        "face_outer": (100, 100, 100),
        "face_middle": (70, 70, 70),
        "face_inner": (50, 50, 50),
        "hand_hour": (255, 255, 255),
        "hand_minute": (200, 200, 200),
        "hand_second": (255, 69, 0),
        "mark_color": (255, 255, 255),
        "shadow": (0, 0, 0, 80),
        "text_color": (255, 255, 255)
    }
}

# Class representing the Analog Clock
class AnalogClock:
    def __init__(self, size, position):
        """
        Initialize the AnalogClock with the specified size and position.
        """
        self.size = size  # Clock size
        self.position = position  # Position of the clock center
        self.hour = 0  # Hour hand angle
        self.minute = 0  # Minute hand angle
        self.second = 0  # Second hand angle
        self.milliseconds = 0  # Milliseconds for smooth second hand movement
        self.font = pygame.font.Font(None, 36)  # Font for displaying date and weather
        self.weather = "Fetching..."  # Initial weather message
        self.update_weather()  # Update the weather info immediately
    
    def update(self):
        """
        Update the time, second, and date to show the current time.
        """
        now = datetime.now()  # Get current date and time
        self.hour = now.hour % 12  # 12-hour format
        self.minute = now.minute  # Get current minute
        self.second = now.second + now.microsecond / 1_000_000  # Smooth second hand movement with microseconds
        self.current_date = now.strftime("%A, %B %d, %Y")  # Format the current date as 'Day, Month Date, Year'
    
    def update_weather(self):
        """
        Fetch the current weather from an online API.
        """
        try:
            # Request the weather data from a weather service
            response = requests.get("https://wttr.in/?format=%t+%C")
            if response.status_code == 200:
                self.weather = response.text.strip()  # If successful, get the weather status
        except:
            self.weather = "Weather unavailable"  # If there is an error, display "Weather unavailable"
    
    def get_theme(self):
        """
        Get the appropriate theme based on the current time of day.
        """
        current_hour = datetime.now().hour
        return THEMES["dark"] if 18 <= current_hour or current_hour < 6 else THEMES["light"]  # Dark theme at night (6 PM - 6 AM), light theme during the day
    
    def draw(self, window):
        """
        Draw the analog clock on the window with the current time, date, and weather.
        """
        theme = self.get_theme()  # Get the appropriate theme based on the time of day
        window.fill(theme["background"])  # Set the background color
        self.__draw_info_panel(window, theme)  # Draw the information panel (date and weather)
        self.__draw_face(window, theme)  # Draw the clock face
        self.__draw_hour_marks(window, theme)  # Draw the hour marks
        self.__draw_hand(window, self.hour * 30 + self.minute * 0.5, self.size * 0.5, 8, theme["hand_hour"], True, theme)  # Draw the hour hand
        self.__draw_hand(window, self.minute * 6, self.size * 0.7, 6, theme["hand_minute"], True, theme)  # Draw the minute hand
        self.__draw_hand(window, self.second * 6, self.size * 0.9, 3, theme["hand_second"], True, theme)  # Draw the second hand
        self.__draw_circle(window, self.position, 10, theme["face_outer"])  # Draw the center circle

    def __draw_circle(self, window, position, size, color):
        """
        Draw a filled circle with anti-aliasing for smooth edges.
        """
        pygame.gfxdraw.aacircle(window, position[0], position[1], size, color)  # Draw anti-aliased circle
        pygame.gfxdraw.filled_circle(window, position[0], position[1], size, color)  # Fill the circle

    def __draw_face(self, window, theme):
        """
        Draw the clock's outer, middle, and inner faces.
        """
        self.__draw_circle(window, self.position, self.size, theme["face_outer"])  # Draw the outer face
        self.__draw_circle(window, self.position, self.size - 30, theme["face_middle"])  # Draw the middle face
        self.__draw_circle(window, self.position, self.size - 40, theme["face_inner"])  # Draw the inner face

    def __draw_hour_marks(self, window, theme):
        """
        Draw the hour marks (12 hour positions) around the clock.
        """
        for i in range(12):  # Draw 12 hour marks
            angle = math.radians(i * 30)  # 30 degree angle per hour
            x1 = self.position[0] + (self.size - 20) * math.cos(angle)  # X coordinate of the start point
            y1 = self.position[1] - (self.size - 20) * math.sin(angle)  # Y coordinate of the start point
            x2 = self.position[0] + (self.size - 40) * math.cos(angle)  # X coordinate of the end point
            y2 = self.position[1] - (self.size - 40) * math.sin(angle)  # Y coordinate of the end point
            pygame.draw.line(window, theme["mark_color"], (x1, y1), (x2, y2), 5)  # Draw the mark lines

    def __draw_hand(self, window, angle, length, width, color, shadow, theme):
        """
        Draw the clock hands (hour, minute, second) with optional shadow.
        """
        angle = math.radians(angle - 90)  # Convert the angle to radians and adjust for rotation
        x = self.position[0] + length * math.cos(angle)  # X coordinate of the hand end
        y = self.position[1] + length * math.sin(angle)  # Y coordinate of the hand end
        
        if shadow:  # If shadow is enabled
            shadow_offset = 5  # Offset for shadow positioning
            shadow_x = self.position[0] + length * math.cos(angle) + shadow_offset  # Shadow X position
            shadow_y = self.position[1] + length * math.sin(angle) + shadow_offset  # Shadow Y position
            pygame.draw.line(window, theme["shadow"], (self.position[0] + shadow_offset, self.position[1] + shadow_offset), (shadow_x, shadow_y), width)  # Draw the shadow
        
        pygame.draw.line(window, color, self.position, (x, y), width)  # Draw the hand itself

    def __draw_info_panel(self, window, theme):
        """
        Draw the date and weather information panel at the top of the window.
        """
        info_surface = self.font.render(f"{self.current_date} | {self.weather}", True, theme["text_color"])  # Render the date and weather text
        info_rect = info_surface.get_rect(center=(self.position[0], 50))  # Position the info panel at the top of the window
        window.blit(info_surface, info_rect)  # Draw the info panel on the window

# Initialize Pygame
pygame.init()
WINDOW_WIDTH = 600  # Set the width of the window
WINDOW_HEIGHT = 600  # Set the height of the window

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Create the game window
pygame.display.set_caption("Analog Clock")  # Set the window title

clock = pygame.time.Clock()  # Create the clock object to control FPS
analog_clock = AnalogClock(250, (300, 300))  # Create the analog clock with a size of 250px and center at (300, 300)

# Main Loop
while True:
    for event in pygame.event.get():  # Handle events like closing the window
        if event.type == pygame.QUIT:
            pygame.quit()  # Quit Pygame if the window is closed
            exit()  # Exit the program
    
    analog_clock.update()  # Update the clock time and weather
    analog_clock.draw(window)  # Draw the clock on the window
    pygame.display.update()  # Update the window display
    clock.tick(60)  # Limit the FPS to 60 for smooth animation