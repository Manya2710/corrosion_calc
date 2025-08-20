# Corrosion Rate Calculator (Metallurgy Project)

A compact, production-ready Python project to compute corrosion rates using common industry methods:

1. **Weight-loss method (ASTM G31 style units)**
   - `CR_mm_per_y = (87.6 * W) / (ρ * A * t)`
     - W in **mg**, ρ in **g/cm³**, A in **cm²**, t in **hours**.
   - Also returns **mpy** (mils per year).

2. **Linear Polarization Resistance (LPR)**
   - `i_corr = B / R_p`
     - B in **mV**, R_p in **Ω·cm²**
   - `CR_mm_per_y = 0.00327 * (i_corr * EW) / ρ`
     - i_corr in **µA/cm²**, EW (equivalent weight) in **g/equiv**, ρ in **g/cm³**

3. **Pitting rate**
   - `PR_mm_per_y = depth_mm * (8760 / t_hours)`

It also includes a tiny **rule-based material suggestion** to illustrate engineering judgement (for resume demos).

## Quick Start

```bash
# 1) Run the CLI
python main.py --method weight-loss --W_mg 25.4 --rho_g_cm3 7.85 --A_cm2 12.5 --t_h 168

# 2) LPR method
python main.py --method lpr --B_mV 26 --Rp_ohm_cm2 1200 --EW_g_per_equiv 27.92 --rho_g_cm3 7.85

# 3) Pitting rate
python main.py --method pitting --depth_mm 0.35 --t_h 720

# 4) Material suggestion (toy rules)
python main.py --method suggest --chloride_ppm 5000 --pH 5.5 --temp_C 60
```

## Files
- `corrosion.py` — Core formulas and utilities.
- `main.py` — CLI for quick use.
- `sample_inputs.csv` — Example input rows for batch calculations.
- `tests.py` — Minimal sanity tests.
- `README.md` — This file.

> **Disclaimer:** Simplified equations for educational use. For critical engineering, consult relevant standards (e.g., ASTM G31, API 571/580/579, NACE/AMPP), validated plant data, and domain experts.
