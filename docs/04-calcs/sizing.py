"""DockHub sizing calculations, DKH-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
Geometry comes from cad/src/model.py (parameters only; build123d is not imported) and costs
from bom/bom.csv. First-principles paper estimates; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, canopy_heights, key_heights, pack_z0  # noqa: E402

rows = []


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


def h(title):
    print(f"\n== {title}")


print("DKH-CAL-001 DockHub sizing (SwapCell interface v0.3)")

# ---------------------------------------------------------------- 1. Assumptions
# SwapCell interface v0.3 reference pack (SWC-PRC-001 v0.3, SWC-CAL-001 v0.1)
V_NOM, V_MAX = 46.8, 54.6
AH = 10.0
E_NAME = V_NOM * AH              # 468 Wh nameplate
R_PACK = 0.110                   # ohm, cells plus links, FETs, shunt, fuse, connector
UA_PACK = 1.17                   # W/K, pack to surrounding air (SWC-CAL-001, open air)
TAU_PACK = 32.0                  # min, pack thermal time constant (SWC-CAL-001)
T_CHG_MAX, T_CHG_MIN = 45.0, 0.0  # degC, pack refuses charge outside this window (v0.3 behaviour rules)
PACK_MASS = 2.85                 # kg
PACK_COST = 414.0                # USD, priced once in the SwapCell BOM
I_CHG = 5.0                      # A, charger CC current and pack charge limit
CC_END = 0.85                    # state of charge at the end of CC (SWC-CAL-001)
I_TERM = 1.0                     # A, CV termination; linear taper gives the 0.6 h CV of SWC-CAL-001
ETA_CHG = 0.90                   # certified charger efficiency
ETA_CELL = 0.95                  # cell charge efficiency (SWC-CAL-001); used for energy accounting
P_CHG_IN_PEAK = V_MAX * I_CHG / ETA_CHG   # 303 W at the end of CC

# Duty case (DKH-REQ-001)
SWAPS = 20
SOC_RETURN = 0.15
SOC_RELEASE = 0.80               # minimum state of charge (decided, DKH-DDR-002) for releasing a pack
# Demand profile: 20 arrival times (h) with a lunch and a dinner peak (assumption to test with riders)
ARRIVALS = [7.5, 8.5, 9.5, 11.0, 11.75, 12.25, 12.75, 13.25, 14.0, 15.5,
            16.5, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.25, 22.5]
assert len(ARRIVALS) == SWAPS
PATIENCE = 15.0                  # min a rider waits for a charged pack before leaving (assumption)

# Cabinet loads
P_AUX_AVG = 30.0                 # W average: controller, modem, display, lights, fans on duty cycle
P_AUX_PEAK = 40.0                # W: two locks during a swap, fans, display, modem transmitting
PF_GOOD, PF_POOR = 0.95, 0.60    # charger power factor with and without power factor correction
V_120, V_230 = 120.0, 230.0
BREAKER_120, BREAKER_230 = 15.0, 10.0
CONTINUOUS = 0.80                # continuous load limit as a fraction of the breaker rating

# Solar
P_PANEL, PSH, DERATE, ETA_MPPT = 400.0, 4.5, 0.80, 0.96
DAY0, DAYLEN = 6.0, 12.0         # sine irradiance profile from 06:00 to 18:00
V_CHG_MEAN = 50.0                # V, mean pack voltage while charging
P_SOLAR_MIN = 50.0               # W, below this bay 1 uses its AC charger instead of the MPPT

# Thermal
RHO_AIR, CP_AIR = 1.2, 1005.0
FAN_FREE = 90.0                  # m3/h free air per 120 mm fan; half is lost to filter and louver
N_FANS = 2
H_OUT, H_IN = 17.0, 8.0          # W/(m2 K), outside (light wind) and inside film coefficients
ALPHA = 0.35                     # solar absorptance, light powder coat
G_WALL = 500.0                   # W/m2 on sunlit walls, canopy shades the roof
PACK_LOSS_HI = 1 - ETA_CELL      # upper bound: all cell charge loss appears as heat

# Wind (R15)
V_GUST, RHO_WIND = 30.0, 1.225
CF_PANEL = 1.5                   # force coefficient normal to the tilted panel (TRL 2 assumption)
CF_BODY = 1.3                    # drag coefficient of the cabinet body
CF_POST = 2.0                    # square posts
ECC = 0.25                       # centre of pressure offset as a fraction of panel depth
LOAD_FACTOR = 1.5                # partial factor on wind for anchor design
MU = 0.4                         # steel plinth on concrete, friction

# Steel
RHO_STEEL = 7850.0
HEM = 1.15                       # allowance for hems, flanges and folds

W, D, t = P["W"] / 1000, P["D"] / 1000, P["sheet_t"] / 1000
BODY_H = (P["roof_z"] - P["plinth_h"]) / 1000
N_BAYS, N_FIT = P["n_bays"], P["bays_fitted"]

# ---------------------------------------------------------------- 2. Charging (R3)
h("2. Charging (R3)")


def i_limit(soc):
    """Charge current in A for the CC-CV profile of a 5 A charger."""
    if soc < CC_END:
        return I_CHG
    k = (I_CHG - I_TERM) / (1 - CC_END)
    return max(I_TERM, I_CHG - k * (soc - CC_END))


def t_charge(s0, s1):
    """Hours to charge from s0 to s1 on the AC charger (analytic CC plus linear-taper CV)."""
    tt = 0.0
    if s0 < CC_END:
        tt += (min(s1, CC_END) - s0) * AH / I_CHG
    if s1 > CC_END:
        k = (I_CHG - I_TERM) / (1 - CC_END)
        a = max(s0, CC_END)
        tt += AH / k * math.log((I_CHG - k * (a - CC_END)) / (I_CHG - k * (s1 - CC_END)))
    return tt


t_20_80, t_full, t_swap_full, t_swap_rel = t_charge(0.2, 0.8), t_charge(0.0, 1.0), t_charge(SOC_RETURN, 1.0), t_charge(SOC_RETURN, SOC_RELEASE)
print(f"20 to 80 %: {t_20_80:.2f} h; 0 to 100 %: {t_full:.2f} h (CV {t_charge(CC_END, 1.0):.2f} h); "
      f"15 to 100 %: {t_swap_full:.2f} h; 15 to 80 %: {t_swap_rel:.2f} h")
e_stored = (1 - SOC_RETURN) * E_NAME
e_out = e_stored / ETA_CELL
e_grid = e_out / ETA_CHG
print(f"Per swap (15 to 100 %): {e_stored:.1f} Wh stored, {e_out:.1f} Wh from the charger, {e_grid:.1f} Wh from the grid")
print(f"Charger input at the end of CC: {P_CHG_IN_PEAK:.0f} W; loss {P_CHG_IN_PEAK * (1 - ETA_CHG):.0f} W")
res("R3", f"20 to 80 % in {t_20_80:.1f} h; full in {t_full:.1f} h", "1.5 h; 2.5 h", "Met")

# ---------------------------------------------------------------- 3. Swap time (R1)
h("3. Swap time (R1)")
steps = [("Tap card or phone, token checked offline", 3), ("Empty bay door unlocks", 1),
         ("Open door, place flat pack connector down", 8), ("Close door", 2),
         ("Controller confirms return (door switch, INTERLOCK, pack identity on CAN)", 2),
         ("Second door unlocks; open and lift out charged pack", 10), ("Close door, step away", 5)]
t_swap = sum(s for _, s in steps)
for n, s in steps:
    print(f"  {s:3d} s  {n}")
print(f"Swap time {t_swap} s")
res("R1", f"{t_swap} s task analysis", "60 s or less", "Met")

# ---------------------------------------------------------------- 4. Throughput and solar, day simulation (R4, R6)
h("4. Throughput and solar share (R4, R6)")


def solar_out(hr):
    """MPPT output in W at clock hour hr on the design day (sine profile, 4.5 peak sun hours)."""
    x = (hr % 24 - DAY0) / DAYLEN
    if not 0 < x < 1:
        return 0.0
    g_pk = PSH * math.pi / (2 * DAYLEN)                     # kW/m2 at noon
    return P_PANEL * g_pk * math.sin(math.pi * x) * DERATE * ETA_MPPT


def simulate(n_bays, steer=True, days=3, dt_min=1.0):
    """Minute-step model of one station. n_bays fitted; n_bays - 1 packs resident, one bay empty.
    Returns statistics for the last day."""
    dt = dt_min / 60.0
    packs = {b: 1.0 for b in range(1, n_bays)}               # bay -> state of charge; bay n_bays empty
    empty = n_bays
    queue, waits, served, turned = [], [], 0, 0
    e = dict(ac_out=0.0, solar_out=0.0, grid=0.0, stored=0.0, solar_avail=0.0)
    peak_chargers = 0
    arrivals = sorted(d * 24 + a for d in range(days) for a in ARRIVALS)
    ai = 0
    steps_n = int(days * 24 / dt)
    for k in range(steps_n):
        now = k * dt
        last_day = now >= (days - 1) * 24
        while ai < len(arrivals) and arrivals[ai] <= now + 1e-9:
            queue.append(arrivals[ai]); ai += 1
        # riders who have waited longer than their patience leave without a swap
        for q_t in [q_t for q_t in queue if (now - q_t) * 60 > PATIENCE]:
            queue.remove(q_t)
            if q_t >= (days - 1) * 24:
                turned += 1
        # serve riders in arrival order
        while queue:
            ready = {b: s for b, s in packs.items() if s >= SOC_RELEASE - 1e-9}
            if not ready:
                break
            sun = solar_out(now) >= P_SOLAR_MIN
            if steer and sun and 1 in ready and len(ready) >= 2:
                take = 1                                        # empty bay 1 so a flat pack lands under the sun
            else:
                take = max(ready, key=lambda b: ready[b])
            t_arr = queue.pop(0)
            packs[empty] = SOC_RETURN                          # returned pack goes into the empty bay
            del packs[take]
            empty = take
            if t_arr >= (days - 1) * 24:
                waits.append((now - t_arr) * 60); served += 1
        # charge
        active = 0
        ps = solar_out(now)
        if last_day:
            e["solar_avail"] += ps * dt
        for b, s in list(packs.items()):
            if s >= 0.999:
                continue
            lim = i_limit(s)
            if b == 1 and ps >= P_SOLAR_MIN:
                i = min(lim, ps / V_CHG_MEAN)
                src = "solar"
            else:
                i = lim
                src = "ac"; active += 1
            ds = min(i * dt / AH, 1.0 - s)
            packs[b] = s + ds
            if last_day:
                wh = ds * E_NAME
                e["stored"] += wh
                if src == "solar":
                    e["solar_out"] += wh / ETA_CELL
                else:
                    e["ac_out"] += wh / ETA_CELL
                    e["grid"] += wh / ETA_CELL / ETA_CHG
        peak_chargers = max(peak_chargers, active)
    return dict(waits=waits, served=served, unserved=turned, peak_chargers=peak_chargers, **e)


sims = {}
for nb in (N_BAYS, N_FIT):
    for steer in (True, False):
        sims[(nb, steer)] = simulate(nb, steer)
for (nb, steer), s in sims.items():
    wt = [w for w in s["waits"] if w > 0.5]
    share = s["solar_out"] / (s["solar_out"] + s["ac_out"]) if s["solar_out"] + s["ac_out"] else 0
    s["share"] = share
    s["n_wait"] = len(wt)
    s["max_wait"] = max(s["waits"]) if s["waits"] else 0
    print(f"{nb} bays ({nb - 1} packs), steering {'on ' if steer else 'off'}: served {s['served']} of {SWAPS}, "
          f"{len(wt)} riders wait, longest wait {s['max_wait']:.0f} min, turned away after {PATIENCE:.0f} min {s['unserved']}; "
          f"solar to packs {s['solar_out']:.0f} Wh of {s['solar_avail']:.0f} Wh available; "
          f"AC charger output {s['ac_out']:.0f} Wh; grid to chargers {s['grid']:.0f} Wh; "
          f"stored {s['stored']:.0f} Wh; solar share {share * 100:.1f} %; peak chargers on {s['peak_chargers']}")

cap_full = (N_BAYS - 1) * 24 / t_swap_full
cap_rel = (N_BAYS - 1) * 24 / t_swap_rel
cap2_full = (N_FIT - 1) * 24 / t_swap_full
cap2_rel = (N_FIT - 1) * 24 / t_swap_rel
print(f"Ceiling with packs released full: {cap_full:.0f} swaps a day (4 bays), {cap2_full:.0f} (2 bays); "
      f"released at 80 %: {cap_rel:.0f} (4 bays), {cap2_rel:.0f} (2 bays)")
print(f"Peak-hour capacity at 80 % release: {(N_BAYS - 1) / t_swap_rel:.2f} swaps/h (4 bays), "
      f"{(N_FIT - 1) / t_swap_rel:.2f} swaps/h (2 bays)")
s4, s2 = sims[(N_BAYS, False)], sims[(N_FIT, False)]      # baseline: release the fullest pack (service first)
s4s = sims[(N_BAYS, True)]
res("R4", f"4 bays: {s4['served']} of {SWAPS} served, longest wait {s4['max_wait']:.0f} min; ceiling {cap_full:.0f} a day "
          f"({cap_rel:.0f} at 80 % release). 2-bay prototype: {s2['served']} of {SWAPS} served",
    "20 a day from 4 bays", "Met (4 bays)")
print(f"Solar steering (release bay 1 first in sun): share {s4s['share'] * 100:.1f} %, served {s4s['served']} of {SWAPS}")

daily_solar_dc = P_PANEL * PSH * DERATE
print(f"Panel DC energy on the design day {daily_solar_dc:.0f} Wh; MPPT output {daily_solar_dc * ETA_MPPT:.0f} Wh; "
      f"peak MPPT output {solar_out(12):.0f} W against the 5 A bay limit of about {I_CHG * V_CHG_MEAN:.0f} W")
res("R6", f"{s4['share'] * 100:.1f} % of charging energy ({s4['solar_out'] / 1000:.2f} of {daily_solar_dc * ETA_MPPT / 1000:.2f} kWh used); "
          f"{s4s['share'] * 100:.1f} % with solar steering, which turns {SWAPS - s4s['served']} rider away",
    "10 % or more (relaxed from 20 %, DKH-DDR-001)",
    ("Met (thin margin)" if s4["share"] < 0.12 else "Met") if s4["share"] >= 0.10 else "Not met")

# ---------------------------------------------------------------- 5. Daily energy
h("5. Daily energy at the duty case (4 bays)")
aux_day = P_AUX_AVG * 24
grid_day = s4["grid"] + aux_day
print(f"Grid to chargers {s4['grid'] / 1000:.2f} kWh + cabinet loads {aux_day / 1000:.2f} kWh = {grid_day / 1000:.2f} kWh from the grid; "
      f"solar {s4['solar_out'] / ETA_MPPT / 1000:.2f} kWh from the panel; stored in packs {s4['stored'] / 1000:.2f} kWh")
charger_loss = s4["grid"] - s4["ac_out"]
mppt_loss = s4["solar_out"] / ETA_MPPT - s4["solar_out"]
cell_loss = s4["ac_out"] + s4["solar_out"] - s4["stored"]
print(f"Losses: chargers {charger_loss / 1000:.2f} kWh, MPPT {mppt_loss / 1000:.2f} kWh, cells {cell_loss / 1000:.2f} kWh")
sol_dc = s4["solar_out"] / ETA_MPPT
to_conv = s4["grid"] + sol_dc
to_packs = s4["ac_out"] + s4["solar_out"]
print(f"Flow diagram (kWh): in {(grid_day + sol_dc) / 1000:.2f} -> chargers and MPPT {to_conv / 1000:.2f} -> pack terminals "
      f"{to_packs / 1000:.2f} -> stored {s4['stored'] / 1000:.2f}; losses: loads {aux_day / 1000:.2f}, conversion "
      f"{(to_conv - to_packs) / 1000:.2f}, cells {cell_loss / 1000:.2f}")
PRICE = 0.20
print(f"Energy cost per swap at ${PRICE:.2f}/kWh: ${grid_day / 1000 / SWAPS * PRICE:.3f} (grid energy incl. cabinet loads), "
      f"${e_grid / 1000 * PRICE:.3f} (charging only)")

# ---------------------------------------------------------------- 6. Grid supply (R5)
h("6. Grid supply (R5)")
p_peak = N_BAYS * P_CHG_IN_PEAK + P_AUX_PEAK
for pf, lab in ((PF_GOOD, "with PFC"), (PF_POOR, "without PFC")):
    s_va = N_BAYS * P_CHG_IN_PEAK / pf + P_AUX_PEAK
    i120, i230 = s_va / V_120, s_va / V_230
    print(f"4 chargers {lab} (PF {pf}): {s_va:.0f} VA, {i120:.1f} A at 120 V (limit {BREAKER_120 * CONTINUOUS:.0f} A continuous), "
          f"{i230:.1f} A at 230 V (limit {BREAKER_230 * CONTINUOUS:.0f} A continuous)")
    if pf == PF_GOOD:
        i120_good, i230_good = i120, i230
    else:
        i120_poor, i230_poor = i120, i230
print(f"Peak real power {p_peak:.0f} W with 4 bays; {N_FIT * P_CHG_IN_PEAK + P_AUX_PEAK:.0f} W with 2 bays fitted; "
      f"simulated day: at most {s4['peak_chargers']} chargers on at once")
res("R5", f"{p_peak / 1000:.2f} kW; {i120_good:.1f} A at 120 V with PF 0.95 ({i120_poor:.1f} A at PF 0.6)",
    "1.5 kW; one 120 V 15 A or 230 V 10 A circuit", "Met (PF 0.9 or better chargers)")

# ---------------------------------------------------------------- 7. Thermal (R9)
h("7. Thermal (R9)")
area_cab = 2 * (W * D) + 2 * (W * BODY_H) + 2 * (D * BODY_H)
u_wall = 1 / (1 / H_OUT + 1 / H_IN)
ua_cab = u_wall * area_cab
sunlit = W * BODY_H + D * BODY_H
q_sol_in = ALPHA * G_WALL * sunlit * (u_wall / H_OUT)
flow = N_FANS * FAN_FREE * 0.5
mc = RHO_AIR * CP_AIR * flow / 3600
n_on = N_BAYS - 1
q_chg = n_on * P_CHG_IN_PEAK * (1 - ETA_CHG)
q_pack_lo = I_CHG ** 2 * R_PACK
q_pack_hi = V_MAX * I_CHG * PACK_LOSS_HI
q_int = q_chg + n_on * q_pack_lo + P_AUX_AVG
dT_air = (q_int + q_sol_in) / (mc + ua_cab)
dT_air_lo_q = (q_chg + n_on * q_pack_hi + P_AUX_AVG + q_sol_in) / (mc + ua_cab)
t_cc = t_charge(SOC_RETURN, CC_END) * 60
dT_pack_lo = q_pack_lo / UA_PACK * (1 - math.exp(-t_cc / TAU_PACK))
dT_pack_hi = q_pack_hi / UA_PACK * (1 - math.exp(-t_cc / TAU_PACK))
t_amb_max_lo = T_CHG_MAX - dT_air - dT_pack_lo
t_amb_max_hi = T_CHG_MAX - dT_air_lo_q - dT_pack_hi
print(f"Cabinet area {area_cab:.2f} m2, U {u_wall:.2f} W/(m2 K), UA {ua_cab:.1f} W/K; fan flow {flow:.0f} m3/h ({flow / 1.699:.0f} cfm), "
      f"{mc:.1f} W/K")
print(f"Heat with {n_on} packs charging: chargers {q_chg:.0f} W, packs {n_on * q_pack_lo:.1f} W (I2R) to {n_on * q_pack_hi:.0f} W (5 % loss bound), "
      f"loads {P_AUX_AVG:.0f} W, sun through the walls {q_sol_in:.0f} W")
print(f"Cabinet air rise {dT_air:.1f} K ({dT_air_lo_q:.1f} K with the loss bound); pack rise at the end of CC "
      f"{dT_pack_lo:.1f} K to {dT_pack_hi:.1f} K")
print(f"At 45 degC ambient: cabinet air {45 + dT_air:.0f} degC, packs {45 + dT_air + dT_pack_lo:.0f} to {45 + dT_air_lo_q + dT_pack_hi:.0f} degC; "
      f"pack refuses charge above {T_CHG_MAX:.0f} degC")
print(f"Highest ambient for uninterrupted 5 A charging: {t_amb_max_hi:.0f} to {t_amb_max_lo:.0f} degC")
dT_idle = P_AUX_AVG / ua_cab
print(f"Cold: idle cabinet with fans off {dT_idle:.1f} K above ambient; a cold-soaked pack reaches 0 degC only above "
      f"about {T_CHG_MIN - dT_idle:.0f} degC ambient")
res("R9", f"Charging pauses above about {t_amb_max_hi:.0f} to {t_amb_max_lo:.0f} degC ambient and for cold-soaked packs below about "
          f"{T_CHG_MIN - dT_idle:.0f} degC; charge window enforced by pack and controller",
    "-10 to 45 degC ambient; never charge outside the pack window", "Not met")

# ---------------------------------------------------------------- 8. Fire detection and venting (R7, R8)
h("8. Fire detection and venting (R7, R8)")
lat = {"NTC sample period": 1.0, "Confirmation (2 further samples)": 2.0, "Controller loop": 0.1}
t_detect = sum(lat.values())
t_open = 0.1 + 0.05
for k, v in lat.items():
    print(f"  {v:4.1f} s  {k}")
print(f"Electronic detection latency {t_detect:.1f} s, leaving {10 - t_detect:.1f} s for sensor response; pack over-temperature "
      f"fault arrives on change over CAN. Contactor: decision 0.10 s + drop-out 0.05 s = {t_open:.2f} s")
port = 60 * 60 / 1e6
plenum = (P["W"] - 2 * P["sheet_t"]) * (P["D"] / 2 - P["sheet_t"] - P["liner_y1"] - P["plenum_t"]) / 1e6
louver = 9 * 50 * 35 / 1e6
print(f"Vent path: bay port {port * 1e4:.0f} cm2, plenum section {plenum * 1e4:.0f} cm2, louver free area {louver * 1e4:.0f} cm2; "
      f"fan air speed through the louver {flow / 3600 / louver:.1f} m/s")
res("R7", f"Electronic latency {t_detect:.1f} s; contactor {t_open:.2f} s; vent path to the roof louver by design",
    "Detect in 10 s; contactor in 1 s", "Not verifiable at TRL 3")
res("R8", "Two 1.5 mm steel walls and a gap between packs; propagation needs a test", "No spread for 30 min",
    "At risk (not verifiable at TRL 3)")

# ---------------------------------------------------------------- 9. Geometry (R2, R11, R13)
h("9. Geometry (R2, R11, R13)")
kh = key_heights()
pz = pack_z0()
overall = P["pack_l"] + P["handle_h"] + P["plug_h"]
clear_top = P["bay_z1"] - (pz + P["pack_l"] + P["handle_h"])
print(f"Pack {P['pack_l']:.0f} x {P['pack_w']:.0f} x {P['pack_d']:.0f} mm, {overall:.0f} mm overall; "
      f"door opening {P['bay_z1'] - P['bay_z0'] - 10:.0f} mm tall, {P['bay_open_w']:.0f} mm wide; clearance above the handle {clear_top:.0f} mm; "
      f"lift to clear the receptacle {P['plug_h'] + 1:.0f} mm")
ops = [kh["door handle"][0], kh["door handle"][1], kh["reader"][0], kh["reader"][1], pz, kh["pack handle top"]]
lo, hi = min(ops), max(ops)
print(f"Operable range {lo:.0f} to {hi:.0f} mm (door handles {kh['door handle']}, reader {kh['reader']}, "
      f"pack from {pz:.0f} to {kh['pack handle top']:.0f} mm)")
res("R11", f"Operable parts {lo / 1000:.2f} to {hi / 1000:.2f} m", "0.38 to 1.22 m", "Met" if lo >= 380 and hi <= 1220 else "Not met")
zr, zf, yf, yr = canopy_heights()
Z_RAIL_OUT = 2179.0              # lowest canopy point outside the footprint, printed by cad/src/model.py
print(f"Footprint {P['W']:.0f} x {P['D']:.0f} mm (plinth flush; handles add 22 mm at the front); panel rear edge underside {zr:.0f} mm, "
      f"front edge top {zf:.0f} mm; lowest rail point over the sidewalk {Z_RAIL_OUT:.0f} mm (model.py)")
res("R13", f"{P['W'] / 1000:.1f} x {P['D'] / 1000:.1f} m; canopy lowest point over the sidewalk {Z_RAIL_OUT / 1000:.2f} m",
    "1.0 x 0.6 m; 2.1 m", "Met")
frames = 34.1                    # frames/s per pack, SwapCell v0.3 message set (SWC-CAL-001)
print(f"CAN: one channel per bay at 250 kbit/s, {frames} frames/s, bus load {frames * 135 / 250e3 * 100:.1f} % per channel; "
      f"SPI traffic for 4 channels about {4 * frames * 16 * 8 / 1e3:.1f} kbit/s")
res("R2", "Interface v0.3: coded INTERLOCK receptacle, dock host type 1, class D catch, one CAN channel per bay",
    "Build to the SwapCell interface, no change", "Met (design review)")
rec_b, tok_b = 64, 16
print(f"Log: {rec_b} B per swap, {SWAPS * rec_b} B a day; 10,000 tokens x {tok_b} B = {10000 * tok_b / 1000:.0f} kB")
res("R12", f"{SWAPS * rec_b / 1000:.2f} kB of log a day; offline token list {10000 * tok_b / 1000:.0f} kB", "No cameras; 24 h offline",
    "Met (design review)")

# ---------------------------------------------------------------- 10. Mass
h("10. Mass")


def cabinet_mass(n_fit, n_packs):
    sheet = {
        "Body shell": area_cab,
        "Bay deck": W * (P["liner_y1"] + P["D"] / 2) / 1000,
        "Bay liners": n_fit * (2 * 0.3585 * 0.53 + 2 * 0.18 * 0.3585 + 0.18 * 0.53),
        "Plenum wall": W * (P["roof_z"] - P["bay_z0"]) / 1000,
        "Doors and blank plates": N_BAYS * 0.18 * 0.52 + 0.96 * 0.52,
        "Charger rack": 0.94 * 0.29,
    }
    a = sum(sheet.values())
    m_sheet = a * t * RHO_STEEL * HEM
    post_l = (canopy_heights()[0] - P["roof_z"]) / 1000
    m = {
        f"Sheet steel ({a:.2f} m2, 1.5 mm, +15 % hems)": m_sheet,
        "Plinth, 4.0 m of 100 x 50 x 5 channel": 4.0 * (100 + 2 * 45) * 5e-6 * RHO_STEEL,
        "Canopy posts and rails": 4 * post_l * 564e-6 * RHO_STEEL + 2 * 1.054 * 504e-6 * RHO_STEEL,
        "Solar panel": 21.0,
        "Chargers": 1.2 * n_fit,
        "Cradles and receptacles": 0.5 * n_fit,
        "Controller, MPPT, grid unit, access panel, fire unit, fans, wiring": 1.0 + 1.0 + 2.0 + 1.5 + 1.5 + 2.0 + 3.0,
        "Packs": PACK_MASS * n_packs,
    }
    return m, sum(m.values())


m4, M4 = cabinet_mass(N_BAYS, N_BAYS - 1)
m2, M2 = cabinet_mass(N_FIT, 0)
for k, v in m4.items():
    print(f"  {v:6.1f} kg  {k}")
print(f"Four bays with 3 packs: {M4:.0f} kg; two-bay prototype without packs (wind case): {M2:.0f} kg")

# ---------------------------------------------------------------- 11. Wind and anchoring (R15)
h("11. Wind and anchoring (R15)")
q = 0.5 * RHO_WIND * V_GUST ** 2
pw, pd, pt = P["panel"]
a_panel = pw * pd / 1e6
a_rad = math.radians(P["tilt_deg"])
N = CF_PANEL * q * a_panel
Nh, Nv = N * math.sin(a_rad), N * math.cos(a_rad)
post_l = (zr - P["roof_z"]) / 1000
F_post = CF_POST * q * 4 * 0.05 * post_l
F_body = CF_BODY * q * W * (P["roof_z"] / 1000)
z_panel = P["panel_z"] / 1000
y_cp = (P["panel_y"] - ECC * pd * math.cos(a_rad)) / 1000       # toward the street edge
pivot = D / 2
M_ot = F_body * P["roof_z"] / 2000 + (Nh + F_post) * z_panel + Nv * (pivot - y_cp)
Wt = M2 * 9.81
M_res = Wt * D / 2
print(f"q = {q:.0f} Pa; panel {a_panel:.2f} m2, normal force {N:.0f} N ({Nh:.0f} N horizontal, {Nv:.0f} N uplift) at y = {y_cp * 1000:.0f} mm; "
      f"posts {F_post:.0f} N; body drag {F_body:.0f} N")
print(f"Overturning about the rear edge {M_ot / 1000:.2f} kN m; self-weight of the {M2:.0f} kg prototype resists {M_res / 1000:.2f} kN m; "
      f"factor {M_res / M_ot:.2f} unanchored")
arm = D - P["anchor_inset"] / 2000
T_anchor = max(0.0, M_ot - M_res) / arm / 2
Td = LOAD_FACTOR * T_anchor
F_h = F_body + Nh + F_post
slide = MU * max(0.0, Wt - Nv)
print(f"Front anchors: {T_anchor / 1000:.2f} kN each characteristic, {Td / 1000:.2f} kN design (x {LOAD_FACTOR}); "
      f"shear {F_h:.0f} N total, {LOAD_FACTOR * F_h / 4:.0f} N per anchor design; friction alone resists {slide:.0f} N")
R_front = Nv * (P["post_y"] / 1000 - y_cp) / (2 * P["post_y"] / 1000) / 2
Wsec = (50 ** 4 - 44 ** 4) / 12 / 25
M_post = (Nh + F_post) / 4 * post_l
print(f"Canopy: front post tension {R_front:.0f} N each into the roof frame; post bending {M_post:.0f} N m, "
      f"{M_post * 1000 / Wsec:.1f} MPa in 50 x 50 x 3 SHS (W = {Wsec / 1000:.2f} cm3), post length {post_l * 1000:.0f} mm")
res("R15", f"Overturning {M_ot / 1000:.1f} kN m against {M_res / 1000:.2f} kN m self-weight; anchors {Td / 1000:.1f} kN design tension each",
    "Upright at a 30 m/s gust", "At risk (anchors and pad not yet chosen)")

# ---------------------------------------------------------------- 12. Cost (R16)
h("12. Cost (R16)")
budget = 1200.0
with open(ROOT / "bom/bom.csv") as f:
    bom = list(csv.DictReader(f))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
per_bay = sum(float(r["unit_cost_usd"]) for r in bom if r["item"].split()[0] in ("2", "3", "5"))
full = total + per_bay * (N_BAYS - N_FIT)
for r in bom:
    print(f"  {r['item']:45s} {float(r['qty']):3.0f} x {float(r['unit_cost_usd']):7.2f} = {float(r['qty']) * float(r['unit_cost_usd']):8.2f}")
print(f"Total with {N_FIT} bays fitted ${total:,.0f} against ${budget:,.0f} (margin ${budget - total:,.0f}); "
      f"each further bay ${per_bay:.0f}; all four fitted ${full:,.0f}. Resident packs (not in cost): "
      f"{N_FIT - 1} x ${PACK_COST:.0f} for the prototype, {N_BAYS - 1} x ${PACK_COST:.0f} for four bays")
res("R16", f"${total:,.0f} with 2 of 4 bays fitted (${full:,.0f} with 4)", "$1,200, packs excluded (two bays fitted, DKH-DDR-001)",
    "At risk" if budget - total < 0.05 * budget and total <= budget else ("Met" if total <= budget else "Not met"))

# ---------------------------------------------------------------- Design review items
res("R10", "1.5 mm steel, fail-secure locks, anchored plinth, token plus returned pack", "Security features", "Met (design review)")
res("R14", "All parts through the service door or bay door with hand tools", "15 min per part", "Not verifiable at TRL 3")

# ---------------------------------------------------------------- Results
h("Results")
order = {"Not met": 0, "At risk": 1, "At risk (anchors and pad not yet chosen)": 1, "At risk (not verifiable at TRL 3)": 1,
         "Not verifiable at TRL 3": 2}
rows.sort(key=lambda r: (order.get(r[3], 3), int(r[0][1:])))
with open(ROOT / "docs/04-calcs/results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    for r in rows:
        w.writerow(r)
        print(f"{r[0]:4s} {r[3]:42s} {r[1]}")
counts = {}
for r in rows:
    key = "Met" if r[3].startswith("Met") else ("At risk" if r[3].startswith("At risk") else r[3])
    counts[key] = counts.get(key, 0) + 1
print("Counts:", counts)
