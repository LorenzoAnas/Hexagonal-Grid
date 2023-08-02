import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import matplotlib.lines as mlines

# Define a Hexagon class for convenience
class Hexagon:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def to_pixel(self):
        x = np.sqrt(3) * (self.q + self.r/2)
        y = 3./2. * self.r
        return x, y

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __hash__(self):
        return hash((self.q, self.r))

# Create a function to draw the hexagon grid and return the hexagons as a set
def draw_hex_grid(size):
    hexagons = set()
    for q in range(-size, size+1):
        for r in range(-size, size+1):
            hex = Hexagon(q, r)
            hex_center = hex.to_pixel()
            hex_color = 'skyblue'
            hexagons.add(hex)

            hex_patch = RegularPolygon(hex_center, numVertices=6, radius=0.95, 
                                       edgecolor='k', facecolor=hex_color, alpha=0.2)
            plt.gca().add_patch(hex_patch)

    return hexagons

# Create a function to find and draw a line between two hexagons
def draw_line(hexA, hexB, hexagons):
    # Draw a line between the two hexagons
    line = mlines.Line2D(*zip(hexA.to_pixel(), hexB.to_pixel()), color='red')
    plt.gca().add_line(line)

    # Use a simple DDA algorithm to sample the line and find crossed hexagons
    crossed_hexagons = set([hexA, hexB])
    N = 1000  # Number of samples (increase for higher accuracy)
    for t in np.linspace(0, 1, N):
        # Compute a point along the line
        x = (1-t)*hexA.to_pixel()[0] + t*hexB.to_pixel()[0]
        y = (1-t)*hexA.to_pixel()[1] + t*hexB.to_pixel()[1]

        # Convert the point back to hexagon coordinates
        q = (np.sqrt(3)/3 * x - 1./3 * y) / (0.95 * 3./2.)
        r = (2./3 * y) / (0.95 * 3./2.)

        # Round to nearest hexagon coordinates
        q, r = round(q), round(r)
        hex = Hexagon(q, r)

        if hex in hexagons:
            crossed_hexagons.add(hex)

    # Draw the crossed hexagons in a different color
    for hex in crossed_hexagons:
        hex_center = hex.to_pixel()
        hex_patch = RegularPolygon(hex_center, numVertices=6, radius=0.95, 
                                   edgecolor='k', facecolor='green', alpha=0.5)
        plt.gca().add_patch(hex_patch)

    return crossed_hexagons

# Set up the drawing
plt.figure(figsize=(8,8))
plt.gca().set_aspect('equal')

# Draw a hex grid of size 10 and get the hexagons
hexagons = draw_hex_grid(10)

# Draw a line between two hexagons and get the crossed hexagons
hexA = Hexagon(0, 0)
hexB = Hexagon(5, -7)
crossed_hexagons = draw_line(hexA, hexB, hexagons)

# Print the crossed hexagons
for hex in crossed_hexagons:
    print(f"Crossed hexagon at coordinates (q={hex.q}, r={hex.r})")

# Adjust the plot limits
plt.xlim(-20, 20)
plt.ylim(-20, 20)

# Display the plot
plt.show()
