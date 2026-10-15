# Field Inspection Workflow

1. **Define the area:** note field corners/centre, dimensions, nearby obstacles (trees, poles, power lines).
2. **Choose altitude and overlap:** lower altitude = more detail but longer flight. Typical:
   30-60 m AGL, 70-80% front overlap, 60-70% side overlap.
3. **Generate the mission:**
   `python tools/mission_planner.py --lat <lat> --lon <lon> --width <m> --height <m> --alt <m> --out missions/<name>.waypoints`
4. **Check endurance:** run `tools/flight_calculator.py`; keep >= 25-30% battery reserve. Split large
   fields into several missions.
5. **Fly the mission** (see the checklist), monitoring battery and wind.
6. **Process imagery:** stitch with photogrammetry software for an orthomosaic; compute vegetation
   indices if a suitable (multispectral/NIR) camera is used.
7. **Interpret:** look for stressed patches, irrigation problems, pest or weed pressure; ground-truth suspicious areas.
8. **Log:** record date, field, conditions, battery usage, and findings.
