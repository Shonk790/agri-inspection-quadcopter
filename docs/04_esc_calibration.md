# ESC Calibration

**WARNING: REMOVE ALL PROPELLERS before doing any of this.**

## Why
ESCs must agree on the throttle endpoints (min/max PWM) so all four motors respond identically.

## All-at-once method (ArduPilot)
1. Remove propellers. Disconnect the battery and USB.
2. Connect via USB, set `ESC_CALIBRATION = 3` (calibrate on next power-up), write params.
3. Disconnect USB.
4. Connect the battery. ESCs enter calibration; the flight controller sends max, then min throttle.
5. Wait for the confirmation beeps; then power-cycle. The parameter resets to 0.

## Manual per-ESC method
1. Props off. Connect the ESC signal lead to the receiver throttle channel (or use the FC passthrough).
2. Throttle stick to maximum, then connect the battery.
3. After the tones, move the stick to minimum and wait for confirmation tones.

## Verify
- In Mission Planner's *Motor Test*, spin each motor at low throttle; confirm order and direction
  (swap any two motor wires to reverse direction).
- All motors should start at the same throttle point and run at similar RPM.
- Record `MOT_SPIN_ARM` / `MOT_SPIN_MIN` after testing.
