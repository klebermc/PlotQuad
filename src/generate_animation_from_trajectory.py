from pathlib import Path

import matplotlib
from matplotlib.animation import PillowWriter
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUT_DIR = PROJECT_ROOT / "output"

def animate_trajectory(horizontal, vertical, path_robot_icon, robot_zoom=0.5,  fig_size=5, save_path='quadElevation.gif', fps=30, draw_traj=True):
    """"
    Animate the trajectory of a robot given its horizontal and vertical positions.
    Parameters:
    - horizontal: list or array of horizontal positions (x-coordinates)
    - vertical: list or array of vertical positions (y-coordinates)
    - path_robot_icon: file path to the robot icon image (e.g., 'robot.png')
    - robot_zoom: zoom factor for the robot icon (default: 0.5)
    - fig_size: tuple specifying the horizontal size of the figure in inches (default: 5)
    - save_path: file path where the animation will be saved (default: 'quadElevation.gif')
    - fps: frames per second for the animation (default: 30)
    - draw_traj: boolean indicating whether to draw the trajectory (default: True)
    """
    
    vertical_traj = list(vertical)
    horizontal_traj = list(horizontal)
    
    linestyle = 'k-' if draw_traj else 'None'

    # Pad each bound ~15% further from zero (or ~15% closer to zero if it's
    # already on the "wrong" side of the origin), so the trajectory doesn't
    # touch the plot edges regardless of whether it sits in positive or
    # negative territory.
    minx, maxx = min(horizontal_traj), max(horizontal_traj)
    miny, maxy = min(vertical_traj), max(vertical_traj)
    if minx < 0:        minx *= 1.15
    else:               minx *= 0.85
    if maxx > 0:        maxx *= 1.15
    else:               maxx *= 0.85
    if miny < 0:        miny *= 1.15
    else:               miny *= 0.85
    if maxy > 0:        maxy *= 1.15
    else:               maxy *= 0.85

    # Force square plotting limits so x/y share the same span.
    xrange = maxx - minx
    yrange = maxy - miny
    maxrange = max(xrange, yrange)
    xcenter = 0.5 * (minx + maxx)
    ycenter = 0.5 * (miny + maxy)
    minx = xcenter - 0.5 * maxrange
    maxx = xcenter + 0.5 * maxrange
    miny = ycenter - 0.5 * maxrange
    maxy = ycenter + 0.5 * maxrange

    # Keep the figure itself square.
    fig_size = (float(fig_size), float(fig_size))

    fig = plt.figure(figsize=fig_size)
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_xlim(minx, maxx), ax.set_xticks([])
    ax.set_ylim(miny, maxy), ax.set_yticks([])
    ax.set_aspect('equal', adjustable='box')

    # Fixed demo obstacle markers (center, radius) — not derived from the
    # trajectory input, just decorative/illustrative for the animation.
    obstacles = [
        ((np.pi / 2.0, -1.0), 0.5),
        ((3.0 * np.pi / 2.0, 1.0), 0.5),
    ]

    img = OffsetImage(plt.imread(path_robot_icon), zoom=robot_zoom)

    def animate(i):
        ax.cla()
        ax.set_xlim(minx, maxx), ax.set_xticks([])
        ax.set_ylim(miny, maxy), ax.set_yticks([])
        ax.set_aspect('equal', adjustable='box')

        for center, radius in obstacles:
            ax.add_patch(Circle(center, radius, facecolor='gray', edgecolor='black', alpha=0.5, lw=1.5))

        ab = AnnotationBbox(img, (horizontal_traj[i], vertical_traj[i]), frameon=False)
        ax.add_artist(ab)
        if draw_traj:
            ax.plot(horizontal_traj[:i+1], vertical_traj[:i+1], linestyle, lw=2)
    # min() on two same-length lists just picks one lexicographically; this
    # relies on horizontal_traj and vertical_traj being the same length, so
    # it's really just `len(horizontal_traj)`.
    ani = matplotlib.animation.FuncAnimation(fig, animate, interval=1000/fps, frames=len(min(horizontal_traj, vertical_traj)))

    ani.save(save_path, writer=PillowWriter(fps=fps))

# Example usage:

t = np.linspace(0, 10, 20)

x = t #np.exp(-0.1 * t) * np.cos(2 * np.pi * t/10)
y = np.sin(2 * np.pi * t/10)
#np.exp(-0.1 * t) * 

plt.plot(x, y)

# FPS is frames per second. 
# For a realistic animation (real-time), fps = 1 / simulation step (seconds) 
# shorter gifs / faster animations = higher fps
# longer gifs / slower animations = lower fps
animate_trajectory(horizontal=x, vertical=y, path_robot_icon=str(ASSETS_DIR / 'quadIcon.png'), robot_zoom=0.5, fig_size=5, save_path=str(OUTPUT_DIR / 'quadTrajectory.gif'), fps=10)