import pygame
import numpy as np

class Hexagon:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def to_pixel(self, size):
        x = size * 3/2 * self.q
        y = size * np.sqrt(3) * (self.r + self.q/2)
        return (x, y)

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __hash__(self):
        return hash((self.q, self.r))

# Create the hexagonal grid and store it as a list of pygame.Polygon objects
def create_hex_grid(size, grid_range):
    hexagons = []
    for q in range(-grid_range, grid_range+1):
        r1 = max(-grid_range, -q - grid_range)
        r2 = min(grid_range, -q + grid_range)
        for r in range(r1, r2+1):
            hex = Hexagon(q, r)
            center_x, center_y = hex.to_pixel(size)
            hex_points = [(center_x + size * np.cos(theta), center_y + size * np.sin(theta)) for theta in np.linspace(0, 2*np.pi, 6, endpoint=False)]
            hexagons.append((hex, hex_points))
    return hexagons

# Bresenham's line algorithm adapted for hexagonal grid
def get_line_high_precision(start, end, num_points=100):
    # Calculate the points along the line
    x_values = np.linspace(start.q, end.q, num_points)
    y_values = np.linspace(start.r, end.r, num_points)
    # Identify the hexagon each point falls into
    hexes = set()
    for x, y in zip(x_values, y_values):
        hex = Hexagon(round(x), round(y))
        hexes.add(hex)
    return hexes


# Pygame setup
pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

size = 30  # Size of each hexagon
grid_range = 5
hexagons = create_hex_grid(size=size, grid_range=grid_range)  # Reduced grid_range for better fit in the screen

# Calculate the center of the hexagonal grid
max_x = max(hex_points[0][0] for hex, hex_points in hexagons)
min_x = min(hex_points[0][0] for hex, hex_points in hexagons)
max_y = max(hex_points[0][1] for hex, hex_points in hexagons)
min_y = min(hex_points[0][1] for hex, hex_points in hexagons)
grid_center_x = (max_x + min_x) / 2
grid_center_y = (max_y + min_y) / 2
# Calculate the adjustment values for centering the grid
adjust_x = screen_width / 2 - grid_center_x
adjust_y = screen_height / 2 - grid_center_y

# Adjust the pixel coordinates of the hexagons to center the grid
for hex, hex_points in hexagons:
    for i in range(len(hex_points)):
        hex_points[i] = (hex_points[i][0] + adjust_x, hex_points[i][1] + adjust_y)

# Main loop
running = True
hexA = hexB = None
while running:
    screen.fill(pygame.Color('white'))  # Fill the background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for hex, hex_points in hexagons:
                if pygame.draw.polygon(screen, pygame.Color('white'), hex_points).collidepoint(x, y):
                    print(f"Clicked hexagon at coordinates (q={hex.q}, r={hex.r})")
                    pygame.draw.polygon(screen, pygame.Color('green'), hex_points)  # Highlight the clicked hexagon
                    if hexA is None:
                        hexA = hex
                    elif hexB is None:
                        hexB = hex
                    else:
                        hexA = hex
                        hexB = None

    # Draw all the hexagons
    for hex, hex_points in hexagons:
        pygame.draw.polygon(screen, pygame.Color('skyblue'), hex_points, 3)  # Line width parameter added for borders

    # Highlight hexagons crossed by the line
    if hexA is not None and hexB is not None:
        crossed_hexes = get_line_high_precision(hexA, hexB)
        for crossed_hex in crossed_hexes:
            for hex, hex_points in hexagons:
                if hex == crossed_hex:
                    pygame.draw.polygon(screen, pygame.Color('yellow'), hex_points)  # Highlight with yellow color
                    pygame.draw.polygon(screen, pygame.Color('black'), hex_points, 3)  # Add border with black color

        # Draw the line between selected hexagons
        pygame.draw.line(screen, pygame.Color('red'), (hexA.to_pixel(size)[0] + adjust_x, hexA.to_pixel(size)[1] + adjust_y), (hexB.to_pixel(size)[0] + adjust_x, hexB.to_pixel(size)[1] + adjust_y), 3)

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Cap at 60 FPS

pygame.quit()
