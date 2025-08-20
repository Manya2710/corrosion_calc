# """
# main.py
# Simple CLI for the Corrosion Rate Calculator.
# """
# import argparse, json, matplotlib.pyplot as plt
# from corrosion import (
#     corrosion_rate_weight_loss_mm_per_y,
#     corrosion_rate_weight_loss_m_per_y,
#     corrosion_rate_LPR_mm_per_y,
#     pitting_rate_mm_per_y,
#     suggest_material,
# )

# def main():
#     parser = argparse.ArgumentParser(description="Corrosion Rate Calculator (educational)")
#     parser.add_argument("--method", required=True, choices=["weight-loss", "lpr", "pitting", "suggest"],
#                         help="Choose calculation method.")
#     # Weight-loss inputs
#     parser.add_argument("--W_mg", type=float, help="Weight loss in mg")
#     parser.add_argument("--density_g_cm3", type=float, help="Density in g/cm^3")
#     parser.add_argument("--A_cm2", type=float, help="Exposed area in cm^2")
#     parser.add_argument("--t_h", type=float, help="Exposure time in hours")

#     # LPR inputs
#     parser.add_argument("--B_mV", type=float, help="Stern-Geary constant in mV (e.g., 26 active, 52 passive)")
#     parser.add_argument("--Rp_ohm_cm2", type=float, help="Polarization resistance in ohm*cm^2")
#     parser.add_argument("--EW_g_per_equiv", type=float, help="Equivalent weight in g/equiv")

#     # Pitting inputs
#     parser.add_argument("--depth_mm", type=float, help="Deepest pit depth in mm")

#     # Suggestion inputs
#     parser.add_argument("--chloride_ppm", type=float, help="Chloride concentration in ppm")
#     parser.add_argument("--pH", type=float, help="Solution pH")
#     parser.add_argument("--temp_C", type=float, help="Temperature in Celsius")

#     args = parser.parse_args()

#     if args.method == "weight-loss":
#         for name in ("W_mg","density_g_cm3","A_cm2","t_h"):
#             if getattr(args, name) is None:
#                 parser.error(f"--{name} is required for weight-loss method")
#         cr_mm_y = corrosion_rate_weight_loss_mm_per_y(args.W_mg, args.density_g_cm3, args.A_cm2, args.t_h)
#         cr_mpy = corrosion_rate_weight_loss_m_per_y(args.W_mg, args.density_g_cm3, args.A_cm2, args.t_h)
#         print(json.dumps({"CR_mm_per_y": round(cr_mm_y, 6), "CR_mpy": round(cr_mpy, 6)}, indent=2))

#     elif args.method == "lpr":
#         for name in ("B_mV","Rp_ohm_cm2","EW_g_per_equiv","density_g_cm3"):
#             if getattr(args, name) is None:
#                 parser.error(f"--{name} is required for LPR method")
#         cr_mm_y = corrosion_rate_LPR_mm_per_y(args.B_mV, args.Rp_ohm_cm2, args.EW_g_per_equiv, args.density_g_cm3)
#         print(json.dumps({"CR_mm_per_y": round(cr_mm_y, 6)}, indent=2))

#     elif args.method == "pitting":
#         for name in ("depth_mm","t_h"):
#             if getattr(args, name) is None:
#                 parser.error(f"--{name} is required for pitting method")
#         pr_mm_y = pitting_rate_mm_per_y(args.depth_mm, args.t_h)
#         print(json.dumps({"PR_mm_per_y": round(pr_mm_y, 6)}, indent=2))

#     elif args.method == "suggest":
#         for name in ("chloride_ppm","pH","temp_C"):
#             if getattr(args, name) is None:
#                 parser.error(f"--{name} is required for suggest method")
#         out = suggest_material(args.chloride_ppm, args.pH, args.temp_C)
#         print(json.dumps(out, indent=2))


# if __name__ == "_main_":
    
#     weight_loss = 0.5   # g
#     area = 10.0         # cm^2
#     time = 100.0        # hours
#     density = 7.85      # g/cm^3 (steel)

#     rate = corrosion_rate_weight_loss_mm_per_y(weight_loss * 1000, density, area, time)
#     print("Corrosion Rate:", round(rate, 6), "mm/year")

#     # ------------------------------
#     # Example graph plotting
#     # ------------------------------
#     areas = [5, 10, 20, 30]
#     rates = [corrosion_rate_weight_loss_mm_per_y(500, 7.85, a, 100) for a in areas]  # 500 mg as example

#     plt.plot(areas, rates, marker='o')
#     plt.xlabel("Surface Area (cm^2)")
#     plt.ylabel("Corrosion Rate (mm/year)")
#     plt.title("Corrosion Rate vs Area")
#     plt.grid(True)
#     plt.show()



import matplotlib.pyplot as plt
from corrosion import (
    corrosion_rate_weight_loss_mm_per_y,
    corrosion_rate_LPR_mm_per_y,
    pitting_rate_mm_per_y,
    suggest_material,
)

if __name__ == "__main__":
    # --- Weight-loss method example ---
    W = 500.0      # mg
    density = 7.85 # g/cm³ (steel)
    A = 10.0       # cm²
    t = 100.0      # hours

    cr_wl = corrosion_rate_weight_loss_mm_per_y(W, density, A, t)
    print(f"Weight Loss Corrosion Rate: {cr_wl:.4f} mm/year")

    # --- LPR method example ---
    B = 26.0       # mV (active steel)
    Rp = 100.0     # ohm·cm²
    EW = 27.92     # g/equiv for steel

    cr_lpr = corrosion_rate_LPR_mm_per_y(B, Rp, EW, density)
    print(f"LPR Corrosion Rate: {cr_lpr:.4f} mm/year")

    # --- Pitting corrosion example ---
    depth = 0.5    # mm
    t_pit = 500.0  # hours

    pr = pitting_rate_mm_per_y(depth, t_pit)
    print(f"Pitting Rate: {pr:.4f} mm/year")

    # --- Material suggestion example ---
    chloride = 5000  # ppm
    pH = 5.0
    temp = 70.0      # °C

    suggestion = suggest_material(chloride, pH, temp)
    print("Material Suggestion:", suggestion["suggestion"])
    print("Notes:", suggestion["notes"])

    # --- Plot corrosion rate vs area (Weight Loss Method) ---
    areas = [5, 10, 20, 30]
    rates = [corrosion_rate_weight_loss_mm_per_y(W, density, a, t) for a in areas]

    plt.plot(areas, rates, marker='o')
    plt.xlabel("Surface Area (cm²)")
    plt.ylabel("Corrosion Rate (mm/year)")
    plt.title("Corrosion Rate vs Area (Weight Loss Method)")
    plt.grid(True)
    plt.show()
