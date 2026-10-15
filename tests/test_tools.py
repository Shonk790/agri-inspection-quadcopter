import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import mission_planner as mp
import flight_calculator as fc


class TestMission(unittest.TestCase):
    def test_footprint(self):
        w, h = mp.footprint(40, 62, 49)
        self.assertAlmostEqual(w, 2 * 40 * 0.6009, places=1)
        self.assertGreater(w, h)

    def test_spacing_shrinks_with_overlap(self):
        a, _ = mp.survey_spacing(40, 62, 49, 0.7, 0.5)
        b, _ = mp.survey_spacing(40, 62, 49, 0.7, 0.8)
        self.assertGreater(a, b)

    def test_mission_format(self):
        text, _, _, n = mp.build_mission(19.07, 72.87, 200, 120, 40, 62, 49, 0.75, 0.65)
        lines = text.strip().split("\n")
        self.assertEqual(lines[0], "QGC WPL 110")
        self.assertTrue(all(len(l.split("\t")) == 12 for l in lines[1:]))
        self.assertEqual(n % 2, 0)
        self.assertEqual(lines[-1].split("\t")[3], "20")  # ends with RTL

    def test_waypoints_within_field(self):
        pts = mp.survey_path(19.0, 72.0, 200, 120, 20)
        lats = [p[0] for p in pts]
        span_m = (max(lats) - min(lats)) * mp.M_PER_DEG_LAT
        self.assertAlmostEqual(span_m, 120, delta=0.5)


class TestCalc(unittest.TestCase):
    def test_twr(self):
        self.assertAlmostEqual(fc.thrust_to_weight(3000, 1500), 2.0)

    def test_flight_time(self):
        e = fc.battery_energy_wh(5000, 4)
        self.assertAlmostEqual(e, 74.0)
        self.assertGreater(fc.flight_time_min(e, fc.hover_power_w(1500, 7)), 0)


if __name__ == "__main__":
    unittest.main()
