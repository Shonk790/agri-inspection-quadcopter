#!/usr/bin/env python3
"""Rough thrust-to-weight and flight-time estimates for a multirotor.

Estimates only: real hover power depends on props, motors, and conditions.
Replace --efficiency with a value measured from your own bench/flight data.
"""
import argparse


def thrust_to_weight(max_thrust_g, mass_g):
    return max_thrust_g / mass_g


def hover_power_w(mass_g, efficiency_g_per_w):
    return mass_g / efficiency_g_per_w


def battery_energy_wh(capacity_mah, cells, nominal_cell_v=3.7):
    return capacity_mah / 1000.0 * cells * nominal_cell_v


def flight_time_min(energy_wh, power_w, usable=0.8):
    return energy_wh * usable / power_w * 60.0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mass", type=float, required=True, help="all-up weight (g)")
    p.add_argument("--capacity", type=float, required=True, help="battery capacity (mAh)")
    p.add_argument("--cells", type=int, required=True, help="LiPo cell count (S)")
    p.add_argument("--max-thrust", type=float, required=True, help="total max thrust, all motors (g)")
    p.add_argument("--efficiency", type=float, default=7.0, help="hover efficiency (g/W), typical 5-9")
    p.add_argument("--usable", type=float, default=0.8, help="usable battery fraction")
    a = p.parse_args()

    twr = thrust_to_weight(a.max_thrust, a.mass)
    power = hover_power_w(a.mass, a.efficiency)
    energy = battery_energy_wh(a.capacity, a.cells)
    t = flight_time_min(energy, power, a.usable)
    print("Thrust-to-weight : %.2f : 1 %s" % (twr, "(OK)" if twr >= 2 else "(low, aim for >= 2)"))
    print("Hover power      : %.0f W" % power)
    print("Battery energy   : %.1f Wh" % energy)
    print("Est. hover time  : %.1f min (%.0f%% usable)" % (t, a.usable * 100))
    print("Survey budget    : ~%.1f min (keeping 25%% reserve)" % (t * 0.75))


if __name__ == "__main__":
    main()
