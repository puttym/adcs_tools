import numpy as np
import yaml
from tabulate import tabulate

MU_EARTH = 398600.4418  # km^3/s^2

def safe_arccos(x):
    """Numerically safe arccos with clamping to [-1, 1]."""
    return np.arccos(np.clip(x, -1.0, 1.0))

class ClassicalOrbitalElements:
    """
    Computes the Classical Orbital Elements (COEs) from a position
    and velocity state vector.
    """

    def __init__(self, position, velocity, mu=MU_EARTH):
        self.r = np.array(position, dtype=float)
        self.v = np.array(velocity, dtype=float)
        self.mu = mu
        self.coe = None

        self._validate_input()

    def _validate_input(self):
        if np.allclose(self.r, 0):
            raise ValueError("Position vector cannot be zero.")
        if np.allclose(self.v, 0):
            raise ValueError("Velocity vector cannot be zero.")
        if not np.isfinite(self.r).all() or not np.isfinite(self.v).all():
            raise ValueError("Position and velocity must contain finite numbers.")

    def calculate(self):
        r = self.r
        v = self.v
        mu = self.mu

        r_norm = np.linalg.norm(r)
        v_norm = np.linalg.norm(v)

        # Specific angular momentum
        h_vec = np.cross(r, v)
        h = np.linalg.norm(h_vec)

        # Inclination
        i = np.degrees(safe_arccos(h_vec[2] / h))

        # Node vector
        k_hat = np.array([0, 0, 1])
        n_vec = np.cross(k_hat, h_vec)
        n = np.linalg.norm(n_vec)

        # RAAN
        if n != 0:
            RAAN = np.degrees(safe_arccos(n_vec[0] / n))
            if n_vec[1] < 0:
                RAAN = 360 - RAAN
        else:
            RAAN = np.nan  # undefined for equatorial orbits

        # Eccentricity vector
        e_vec = (1/mu) * ((v_norm**2 - mu/r_norm)*r - np.dot(r, v)*v)
        e = np.linalg.norm(e_vec)

        # Argument of perigee
        if n != 0 and e > 1e-8:
            omega = np.degrees(np.arccos(np.dot(n_vec, e_vec) / (n * e)))
            if e_vec[2] < 0:
                omega = 360 - omega
        else:
            omega = np.nan

        # True anomaly
        if e > 1e-8:
            nu = np.degrees(safe_arccos(np.dot(e_vec, r) / (e * r_norm)))
            if np.dot(r, v) < 0:
                nu = 360 - nu
        else:  # Circular orbit
            if n != 0:
                nu = np.degrees(safe_arccos(np.dot(n_vec, r) / (n * r_norm)))
                if r[2] < 0:
                    nu = 360 - nu
            else:
                nu = np.nan  # circular equatorial case: undefined

       # Semi-major axis
        energy = v_norm**2 / 2 - mu / r_norm
        if abs(energy) > 1e-12:
            a = -mu / (2 * energy)
        else:
            a = np.inf  # parabolic case 

        # Full precision dict (for YAML or further computation)
        self.coe = {
            "h (km^2/s)": float(h),
            "a (km)": float(a),
            "i (deg)": float(i),
            "RAAN (deg)": float(RAAN),
            "e": float(e),
            "omega (deg)": float(omega),
            "nu (deg)": float(nu),
        }

        # Rounded copy (for human-friendly printing)
        self.coe_display = {k: round(v, 2) for k, v in self.coe.items()}

        return self.coe

    def summary(self):
        if self.coe is None:
            raise RuntimeError("COEs not yet calculated. Call calculate() first.")
        table = tabulate(
            self.coe_display.items(),  # use rounded copy
            headers=["Element", "Value"],
            floatfmt=".2f",
            tablefmt="fancy_grid"
        )
        print(table)

    def save_to_yaml(self, filename="coe_output.yaml"):
        if self.coe is None:
            raise RuntimeError("COEs not yet calculated. Call calculate() first.")

        with open(filename, "w") as f:
            yaml.dump(self.coe, f, default_flow_style=False)

        print(f"COEs saved to {filename}")