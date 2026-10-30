"""Generate a conic gradient ring icon for Circuit High Contrast theme."""

from PIL import Image
import math

SIZE = 512
CENTER = SIZE // 2
PADDING = 40
RADIUS = SIZE // 2 - PADDING
RING_THICKNESS = 50  # width of the ring
INNER_RADIUS = RADIUS - RING_THICKNESS

# Circuit greens evenly spaced around the circle.
# Last stop wraps back to the first color for a seamless loop.
COLORS = [
    (0 / 4, (24, 193, 95)),    # green-8          #18c15f
    (1 / 4, (28, 227, 112)),   # green-9 (dark)   #1ce370
    (2 / 4, (29, 216, 160)),   # logo-turquoise   #1dd8a0
    (3 / 4, (15, 118, 58)),    # green-10 (light) #0f763a
    (4 / 4, (24, 193, 95)),    # green-8  (wrap)
]


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB tuples."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def get_gradient_color(t):
    """Get color at position t (0.0 to 1.0) along the gradient."""
    t = max(0.0, min(1.0, t))
    for i in range(len(COLORS) - 1):
        t0, c0 = COLORS[i]
        t1, c1 = COLORS[i + 1]
        if t <= t1:
            local_t = (t - t0) / (t1 - t0) if t1 != t0 else 0
            return lerp_color(c0, c1, local_t)
    return COLORS[-1][1]


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    pixels = img.load()

    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CENTER
            dy = y - CENTER
            dist = math.sqrt(dx * dx + dy * dy)

            # Only draw in the ring area
            if INNER_RADIUS - 2 < dist <= RADIUS + 2:
                # Angle from center, normalized to 0.0-1.0
                angle = math.atan2(dy, dx)  # -pi to pi
                t = (angle + math.pi) / (2 * math.pi)  # 0.0 to 1.0

                r, g, b = get_gradient_color(t)
                alpha = 255

                # Anti-alias outer edge
                if dist > RADIUS:
                    alpha = max(0, int(255 * (RADIUS + 2 - dist) / 2))
                # Anti-alias inner edge
                elif dist < INNER_RADIUS:
                    alpha = max(0, int(255 * (dist - (INNER_RADIUS - 2)) / 2))

                pixels[x, y] = (r, g, b, alpha)

    # Save full size and the 256x256 VS Code icon (recommended for Retina)
    img.save("icon_large.png")
    icon = img.resize((256, 256), Image.LANCZOS)
    icon.save("icon.png")
    print("Generated icon.png (256x256) and icon_large.png (512x512)")


if __name__ == "__main__":
    main()
