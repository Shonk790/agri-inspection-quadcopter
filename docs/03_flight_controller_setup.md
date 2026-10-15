# Flight Controller Setup (ArduPilot / Mission Planner flow)

1. **Firmware:** flash the latest stable ArduCopter for your board.
2. **Frame type:** set `FRAME_CLASS = 1` (Quad), `FRAME_TYPE = 1` (X).
3. **Accelerometer calibration:** 6-position calibration on a level surface.
4. **Compass calibration:** outdoors, away from metal; confirm no large offsets.
5. **Radio calibration:** calibrate RC channels; verify min/max/trim.
6. **Flight modes:** typical set - Stabilize, AltHold, Loiter, Auto, RTL, Land.
7. **Power module:** set `BATT_MONITOR`, voltage/current multipliers matching measured values.
8. **Failsafes:** configure radio, battery, and GCS failsafe actions (RTL/Land).
9. **Geofence (optional):** set max altitude and radius.
10. **Tuning:** after first hover, review logs for vibration and tune PIDs / use autotune.

See `config/arducopter_params_example.param` for a starting-point parameter set.
Always verify parameter names and units against the ArduPilot documentation for your firmware version.
