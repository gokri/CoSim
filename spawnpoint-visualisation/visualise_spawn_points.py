"""
Spawn Point Visualiser for CARLA 0.10.0 (UE5)
----------------------------------------------
Connects to a running CARLA server, fetches all spawn points for the
currently loaded map, and plots them on a 2D scatter map.

Usage:
    python visualise_spawn_points.py
    python visualise_spawn_points.py --host localhost --port 2000

Hover over a point to see its index, X, Y coordinates and yaw.
Click a point to print its carla.Transform to the terminal.

Requirements: pip install matplotlib (already in carla_ue5_env likely)
"""

import argparse
import carla
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
import numpy as np


def main():
    parser = argparse.ArgumentParser(description="Visualise CARLA spawn points on a 2D map")
    parser.add_argument("--host", default="localhost", help="CARLA server host (default: localhost)")
    parser.add_argument("--port", type=int, default=2000, help="CARLA server port (default: 2000)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Client timeout seconds (default: 10)")
    args = parser.parse_args()

    # --- Connect to CARLA ---
    print(f"Connecting to CARLA at {args.host}:{args.port} ...")
    client = carla.Client(args.host, args.port)
    client.set_timeout(args.timeout)
    world = client.get_world()
    map_name = world.get_map().name
    spawn_points = world.get_map().get_spawn_points()
    print(f"Map: {map_name}")
    print(f"Total spawn points: {len(spawn_points)}")

    if not spawn_points:
        print("No spawn points found. Make sure a map is loaded.")
        return

    # --- Extract coordinates ---
    xs = [sp.location.x for sp in spawn_points]
    ys = [-sp.location.y for sp in spawn_points]   # flip Y so map looks natural (CARLA Y is left-handed)
    yaws = [sp.rotation.yaw for sp in spawn_points]
    indices = list(range(len(spawn_points)))

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.canvas.manager.set_window_title(f"Spawn Points — {map_name}")
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#16213e")

    sc = ax.scatter(xs, ys, c=range(len(xs)), cmap="plasma", s=60, zorder=3, picker=True, pickradius=8)

    # Draw yaw arrows
    arrow_len = 4.0
    for x, y, yaw in zip(xs, ys, yaws):
        import math
        rad = math.radians(-yaw)   # flip to match Y flip
        ax.annotate("", xy=(x + arrow_len * math.cos(rad), y + arrow_len * math.sin(rad)),
                    xytext=(x, y),
                    arrowprops=dict(arrowstyle="->", color="white", lw=0.6),
                    zorder=4)

    # Index labels
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.text(x + 1.5, y + 1.5, str(i), fontsize=6, color="white", zorder=5)

    plt.colorbar(sc, ax=ax, label="Spawn point index")
    ax.set_title(f"{map_name}  —  {len(spawn_points)} spawn points", color="white", fontsize=13)
    ax.set_xlabel("X (CARLA)", color="white")
    ax.set_ylabel("Y (CARLA, flipped for display)", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")
    ax.grid(True, color="#333", linewidth=0.5)
    ax.set_aspect("equal")

    # --- Hover tooltip ---
    annot = ax.annotate("", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.4", fc="#0f3460", ec="white", lw=1),
                        arrowprops=dict(arrowstyle="->", color="white"),
                        color="white", fontsize=9, zorder=10)
    annot.set_visible(False)

    def update_annot(ind):
        i = ind["ind"][0]
        sp = spawn_points[i]
        annot.xy = (xs[i], ys[i])
        annot.set_text(
            f"Index: {i}\n"
            f"X: {sp.location.x:.2f}\n"
            f"Y: {sp.location.y:.2f}\n"
            f"Z: {sp.location.z:.2f}\n"
            f"Yaw: {sp.rotation.yaw:.1f}°"
        )

    def on_hover(event):
        if event.inaxes != ax:
            return
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
        else:
            annot.set_visible(False)
        fig.canvas.draw_idle()

    def on_pick(event):
        if event.artist != sc:
            return
        i = event.ind[0]
        sp = spawn_points[i]
        print(f"\n--- Spawn Point [{i}] ---")
        print(f"carla.Transform(")
        print(f"    carla.Location(x={sp.location.x:.3f}, y={sp.location.y:.3f}, z={sp.location.z:.3f}),")
        print(f"    carla.Rotation(pitch={sp.rotation.pitch:.3f}, yaw={sp.rotation.yaw:.3f}, roll={sp.rotation.roll:.3f})")
        print(f")")
        print(f"  → use in scenarioManager.py: spawn_points[{i}]")

    fig.canvas.mpl_connect("motion_notify_event", on_hover)
    fig.canvas.mpl_connect("pick_event", on_pick)

    print("\nPlot ready. Hover over dots to see coordinates. Click a dot to print its Transform.")
    print("Close the window when done.\n")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
