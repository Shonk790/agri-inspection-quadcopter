#!/usr/bin/env python3
"""Generate a lawnmower (boustrophedon) survey mission for a rectangular field.

Output is a QGC WPL 110 .waypoints file usable in Mission Planner / QGroundControl.
Survey lines run east-west and step northward. The rectangle is centred on --lat/--lon.
"""
import argparse
import math

M_PER_DEG_LAT = 111320.0


def footprint(alt, hfov_deg, vfov_deg):
    """Ground footprint (width, height) in metres for a nadir camera at `alt`."""
    w = 2 * alt * math.tan(math.radians(hfov_deg) / 2)
    h = 2 * alt * math.tan(math.radians(vfov_deg) / 2)
    return w, h


def survey_spacing(alt, hfov, vfov, front_overlap, side_overlap):
    """Return (line_spacing_m, photo_spacing_m). Camera width is across-track."""
    w, h = footprint(alt, hfov, vfov)
    return w * (1 - side_overlap), h * (1 - front_overlap)


def offset(lat, lon, north_m, east_m):
    dlat = north_m / M_PER_DEG_LAT
    dlon = east_m / (M_PER_DEG_LAT * math.cos(math.radians(lat)))
    return lat + dlat, lon + dlon


def survey_path(lat, lon, width, height, line_spacing):
    """Local (north, east) corner points of the lawnmower pattern, then to lat/lon."""
    n_lines = max(2, int(math.ceil(height / line_spacing)) + 1)
    step = height / (n_lines - 1)
    pts = []
    for i in range(n_lines):
        north = -height / 2 + i * step
        east_a, east_b = (-width / 2, width / 2) if i % 2 == 0 else (width / 2, -width / 2)
        pts.append(offset(lat, lon, north, east_a))
        pts.append(offset(lat, lon, north, east_b))
    return pts


def build_mission(lat, lon, width, height, alt, hfov, vfov, front, side, speed=None):
    line_sp, photo_sp = survey_spacing(alt, hfov, vfov, front, side)
    pts = survey_path(lat, lon, width, height, line_sp)
    rows = []
    seq = 0

    def add(cur, frame, cmd, p1, p2, p3, p4, la, lo, al):
        nonlocal seq
        rows.append("\t".join(str(x) for x in (
            seq, cur, frame, cmd, p1, p2, p3, p4,
            "%.8f" % la, "%.8f" % lo, "%.2f" % al, 1)))
        seq += 1

    add(1, 0, 16, 0, 0, 0, 0, lat, lon, 0)                    # home
    add(0, 3, 22, 0, 0, 0, 0, 0, 0, alt)                       # takeoff
    if speed:
        add(0, 3, 178, 1, speed, -1, 0, 0, 0, 0)               # DO_CHANGE_SPEED
    add(0, 3, 206, round(photo_sp, 1), 0, 1, 0, 0, 0, 0)       # camera trigger by distance
    for la, lo in pts:
        add(0, 3, 16, 0, 0, 0, 0, la, lo, alt)                 # waypoint
    add(0, 3, 206, 0, 0, 1, 0, 0, 0, 0)                        # stop camera trigger
    add(0, 3, 20, 0, 0, 0, 0, 0, 0, 0)                         # RTL
    return "QGC WPL 110\n" + "\n".join(rows) + "\n", line_sp, photo_sp, len(pts)


def path_length_m(width, height, line_spacing):
    n_lines = max(2, int(math.ceil(height / line_spacing)) + 1)
    return n_lines * width + (n_lines - 1) * (height / (n_lines - 1))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lat", type=float, required=True, help="field centre latitude")
    p.add_argument("--lon", type=float, required=True, help="field centre longitude")
    p.add_argument("--width", type=float, required=True, help="east-west size (m)")
    p.add_argument("--height", type=float, required=True, help="north-south size (m)")
    p.add_argument("--alt", type=float, default=40, help="altitude AGL (m)")
    p.add_argument("--hfov", type=float, default=62, help="camera horizontal FOV (deg)")
    p.add_argument("--vfov", type=float, default=49, help="camera vertical FOV (deg)")
    p.add_argument("--front-overlap", type=float, default=0.75)
    p.add_argument("--side-overlap", type=float, default=0.65)
    p.add_argument("--speed", type=float, default=None, help="ground speed (m/s)")
    p.add_argument("--out", default="missions/field_survey.waypoints")
    a = p.parse_args()

    text, line_sp, photo_sp, n = build_mission(
        a.lat, a.lon, a.width, a.height, a.alt, a.hfov, a.vfov,
        a.front_overlap, a.side_overlap, a.speed)
    with open(a.out, "w") as f:
        f.write(text)
    dist = path_length_m(a.width, a.height, line_sp)
    print("Wrote %s" % a.out)
    print("Waypoints: %d | line spacing: %.1f m | photo spacing: %.1f m" % (n, line_sp, photo_sp))
    print("Approx. survey path length: %.0f m" % dist)
    if a.speed:
        print("Approx. survey time: %.1f min" % (dist / a.speed / 60))


if __name__ == "__main__":
    main()
