# Quadcopter Drone for Agricultural Field Inspection

Custom-built quadcopter for aerial inspection of crop fields: frame build, flight
controller setup, ESC calibration, and survey-mission planning.

> **Note:** Part numbers, parameter values, and specs in this repository are
> *templates / typical starting points*. Replace them with the actual components and
> measurements from your build before relying on them.

## Contents
| Path | Description |
|------|-------------|
| `docs/01_bill_of_materials.md` | Components list |
| `docs/02_frame_build.md` | Frame assembly and layout notes |
| `docs/03_flight_controller_setup.md` | Firmware, sensors, radio, modes, failsafes |
| `docs/04_esc_calibration.md` | ESC calibration procedure and motor test |
| `docs/05_preflight_checklist.md` | Pre-flight and post-flight checklists |
| `docs/06_field_inspection_workflow.md` | Planning and flying a crop inspection survey |
| `config/arducopter_params_example.param` | Example ArduCopter parameters (starting point) |
| `tools/mission_planner.py` | Generates a lawnmower survey `.waypoints` file |
| `tools/flight_calculator.py` | Thrust-to-weight and flight-time estimates |
| `tests/test_tools.py` | Unit tests for the tools |

## Quick start
```bash
# Generate a survey mission for a 200 m x 120 m field at 40 m altitude
python tools/mission_planner.py --lat 19.0760 --lon 72.8777 \
    --width 200 --height 120 --alt 40 --out missions/field_survey.waypoints

# Estimate flight time and thrust-to-weight
python tools/flight_calculator.py --mass 1500 --capacity 5000 --cells 4 \
    --max-thrust 4000 --efficiency 7

python tests/test_tools.py
```
Load the `.waypoints` file in Mission Planner or QGroundControl. Python 3.8+, no
external dependencies.

## Safety
Always remove propellers during ESC calibration and bench tests. Follow local drone
regulations (registration, altitude limits, visual line of sight, no-fly zones).
