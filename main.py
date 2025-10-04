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
