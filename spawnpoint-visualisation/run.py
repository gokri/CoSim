"""
Spawn Point Visualiser — Quick Launcher
========================================

This script launches the CARLA 2D map visualiser with spawn points visible.
The visualiser is the built-in no_rendering_mode.py, modified to show
red circles + index numbers at every spawn point.

REQUIREMENTS:
  - carla_ue5_env venv must be active  (run: carlaue5  in PowerShell)
  - CARLA server must be running        (StagedBuilds\Windows\CarlaUnreal.exe)

HOW TO USE:
  1. Run this script:  python run.py
  2. Press TAB        → switches to full Map Mode (shows entire Town10)
  3. Scroll           → zoom in/out
  4. Left-click a dot → prints index + coordinates to this terminal

OUTPUT EXAMPLE:
  === Spawn Point [85] ===
    X=-89.886, Y=27.934, Z=0.600
    Yaw=0.16
    scenarioManager.py: spawn_points[85]
    carla.Transform(carla.Location(x=-89.886, y=27.934, z=0.600), carla.Rotation(yaw=0.16))

AFTER PICKING POINTS:
  Edit CoSim/src/sim/config.py:
    useCustomNPCSpawnPoints = True
    npcSpawnIndices = [85, 90, 99, 103]   # <-- your chosen indices here

NOTES:
  - Modified file: PythonAPI/examples/no_rendering_mode.py
  - Cache deleted from:  CoSim/cache/no_rendering_mode/  (delete to force redraw)
  - Works for any CARLA map — just load the map first, then run this script
"""

import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(__file__), "spawn_point_viewer.py")

cmd = [sys.executable, SCRIPT, "--res", "1280x720", "--show-spawn-points"]

print("Launching CARLA Spawn Point Visualiser...")
print("  -> Press TAB to switch to full Map Mode")
print("  -> Left-click a red dot to print its coordinates\n")

subprocess.run(cmd)
