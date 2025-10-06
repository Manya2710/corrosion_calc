from dataclasses import dataclass
from typing import Optional, Dict

def mm_per_y_to_mpy(mm_per_y: float) -> float:
    """Convert mmpy to mpy. 1 mm = 39.3701 mils."""
    return mm_per_y * 39.3701

def mpy_to_mm_per_y(mpy: float) -> float:
    """Convert mpy to mmpy."""
    return mpy / 39.3701

def corrosion_rate_weight_loss_m_per_y(W_mg: float, density_g_cm3: float, A_cm2: float, t_h: float) -> float:
    """
        CR_mm_per_y = (534 * W) / (D * A * t)
        W in mg, density in g/cm^3, area A in in^2, time t in hours.
    """
    if density_g_cm3 <= 0 or A_cm2 <= 0 or t_h <= 0:
        raise ValueError("density_g_cm3, A_cm2, and t_h must be positive.")
    return (543 * W_mg) / (density_g_cm3 * A_cm2 * t_h)

def corrosion_rate_weight_loss_mm_per_y(W_mg: float, density_g_cm3: float, A_cm2: float, t_h: float) -> float:
    """Convenience wrapper to return mmpy."""
    if density_g_cm3 <= 0 or A_cm2 <= 0 or t_h <= 0:
        raise ValueError("density_g_cm3, A_cm2, and t_h must be positive.")
    return mpy_to_mm_per_y(corrosion_rate_weight_loss_m_per_y(W_mg, density_g_cm3, A_cm2, t_h))

# ---------- LPR method ----------
def icorr_uA_cm2_from_LPR(B_mV: float, Rp_ohm_cm2: float) -> float:
    """
    Linear Polarization Resistance:
        i_corr (µA/cm^2) = B (mV) / Rp (Ω·cm^2)
    """
    if Rp_ohm_cm2 <= 0:
        raise ValueError("Rp must be positive.")
    return B_mV / Rp_ohm_cm2

def corrosion_rate_LPR_mm_per_y(B_mV: float, Rp_ohm_cm2: float, EW_g_per_equiv: float, density_g_cm3: float) -> float:
    """
    CR (mm/y) = 0.00327 * (i_corr * EW) / density
    where i_corr in µA/cm^2, EW in g/equiv, density in g/cm^3.
    """
    if density_g_cm3 <= 0 or EW_g_per_equiv <= 0:
        raise ValueError("density and EW must be positive.")
    icorr = icorr_uA_cm2_from_LPR(B_mV, Rp_ohm_cm2)
    return 0.00327 * (icorr * EW_g_per_equiv) / density_g_cm3

# ---------- Pitting rate ----------
def pitting_rate_mm_per_y(depth_mm: float, t_h: float) -> float:
    """
    Pitting corrosion rate defined as deepest pit depth per year equivalent:
        PR_mm_per_y = depth_mm * (8760 / t_h)
        1yr=8760hrours
    """
    if t_h <= 0:
        raise ValueError("t_h must be positive.")
    return depth_mm * (8760.0 / t_h)

# ---------- Material suggestion (rule-based) ----------
def suggest_material(chloride_ppm: float, pH: float, temp_C: float) -> Dict[str, str]:
    """
    Very simplified rules to illustrate decision logic.
    Returns dict with 'suggestion' and 'notes'.
    """
    suggestion = "Carbon steel with coating"
    notes = []

    if chloride_ppm >= 20000 and temp_C >= 60:
        suggestion = "Super duplex stainless steel (e.g., UNS S32750)"
        notes.append("High chlorides & elevated temperature → duplex class for pitting resistance.")
    elif chloride_ppm >= 1000 and pH <= 6.0:
        suggestion = "316L stainless or 2205 duplex; consider corrosion inhibitor"
        notes.append("Moderate chlorides and acidic conditions increase pitting/SCC risk.")
    elif pH <= 4.5:
        suggestion = "Alloy 625 / 825 or lined carbon steel; inhibitor required"
        notes.append("Acidic conditions aggressive to CS and 300-series SS.")

    if temp_C >= 80:
        notes.append("High temperature accelerates corrosion; verify chloride SCC risk.")

    return {
        "suggestion": suggestion,
        "notes": " ".join(notes) if notes else "Baseline service; verify with detailed materials selection."
    }
