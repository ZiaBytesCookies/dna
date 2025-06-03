import pygame
import math
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
PURPLE = (150, 0, 150)
CYAN = (0, 150, 150)

# DNA Parameters
HELIX_RADIUS = 100  # Radius of the helix
NUM_PAIRS = 20      # Number of base pairs visible
PAIR_SPACING = 25   # Vertical spacing between base pairs
ROTATION_SPEED = 0.01 # Radians per frame
DOT_RADIUS_BASE = 8 # Base radius for backbone dots
DOT_RADIUS_DEPTH_FACTOR = 4 # How much size changes with depth

# Base pair colors (simplified)
# Adenine-Thymine (A-T)
# Guanine-Cytosine (G-C)
BASE_PAIR_COLORS = [
    (RED, YELLOW),   # A-T like
    (BLUE, GREEN),   # G-C like
    (PURPLE, CYAN),
    (YELLOW, RED)
]
BACKBONE_COLOR_1 = WHITE
BACKBONE_COLOR_2 = (200, 200, 200) # Slightly different for distinction

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DNA Animation")
clock = pygame.time.Clock()

# --- Main Loop ---
running = True
angle_offset = 0  # Initial rotation angle

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    angle_offset += ROTATION_SPEED
    if angle_offset > 2 * math.pi:
        angle_offset -= 2 * math.pi

    # --- Drawing ---
    screen.fill(BLACK)

    # Store all elements to draw with their z-depth for sorting
    # (z, type, color1, color2/pos1, pos2/radius)
    # z > 0 is "closer"
    draw_elements = []

    center_x = SCREEN_WIDTH // 2
    start_y = SCREEN_HEIGHT // 2 - (NUM_PAIRS * PAIR_SPACING) // 2

    for i in range(NUM_PAIRS):
        y_pos = start_y + i * PAIR_SPACING

        # Calculate angle for this segment of the helix
        # The 'i * 0.3' creates the twist. Adjust 0.3 for more/less twist.
        current_angle1 = angle_offset + i * 0.3
        current_angle2 = angle_offset + i * 0.3 + math.pi # 180 degrees offset for the other strand

        # Calculate positions for the two backbone strands
        # Strand 1
        x1 = center_x + HELIX_RADIUS * math.cos(current_angle1)
        z1 = math.sin(current_angle1) # Depth (-1 to 1)

        # Strand 2
        x2 = center_x + HELIX_RADIUS * math.cos(current_angle2)
        z2 = math.sin(current_angle2) # Depth (-1 to 1)

        # Base pair color
        pair_color_idx = i % len(BASE_PAIR_COLORS)
        color_bp1, color_bp2 = BASE_PAIR_COLORS[pair_color_idx]

        # Add rung (line between backbone points)
        # Average Z for the rung for sorting
        avg_z_rung = (z1 + z2) / 2.0
        # For rungs, we use two colors to represent the two bases
        # We'll draw two short lines from center to each backbone point
        mid_x_rung = (x1 + x2) / 2
        mid_y_rung = y_pos
        draw_elements.append((avg_z_rung, "rung_segment", color_bp1, (mid_x_rung, mid_y_rung), (x1, y_pos)))
        draw_elements.append((avg_z_rung, "rung_segment", color_bp2, (mid_x_rung, mid_y_rung), (x2, y_pos)))


        # Add backbone dots
        # Radius scaled by depth (z)
        radius1 = int(DOT_RADIUS_BASE + z1 * DOT_RADIUS_DEPTH_FACTOR)
        radius2 = int(DOT_RADIUS_BASE + z2 * DOT_RADIUS_DEPTH_FACTOR)

        if radius1 < 1: radius1 = 1 # ensure visible
        if radius2 < 1: radius2 = 1

        draw_elements.append((z1, "dot", BACKBONE_COLOR_1, (int(x1), y_pos), radius1))
        draw_elements.append((z2, "dot", BACKBONE_COLOR_2, (int(x2), y_pos), radius2))

    # Sort elements by Z-depth (draw elements further away first)
    draw_elements.sort(key=lambda item: item[0])

    # Draw sorted elements
    for z, type, color1, data1, data2 in draw_elements:
        if type == "dot":
            pos = data1
            radius = data2
            pygame.draw.circle(screen, color1, pos, radius)
        elif type == "rung_segment":
            pos1 = data1
            pos2 = data2
            # Scale line thickness slightly by depth (optional, can be subtle)
            thickness = max(1, int(2 + z * 1.5)) # z is -1 to 1
            pygame.draw.line(screen, color1, pos1, pos2, thickness)


    # --- Display ---
    pygame.display.flip()
    clock.tick(FPS)

# --- Quit ---
pygame.quit()