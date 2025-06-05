import math
import argparse
from typing import Tuple


class Catenary:
    """
    Represents a catenary curve defined by its endpoints and diameter.

    Methods allow fitting parameters and computing geometric properties.
    """

    INF: float = 1e12
    DEFAULT_A: float = 1.0
    DEFAULT_B: float = 1.0
    DEFAULT_STEP: float = 0.1
    STEP_REDUCTION_FACTOR: float = 10.0
    DEFAULT_PRECISION: float = 1e-7

    def __init__(self, diameter: float, span: float) -> None:
        """
        Initialise the Catenary with the specified diameter and span.

        Args:
            diameter: The vertical distance (diameter) at endpoints.
            span: The horizontal distance between endpoints.
        """
        self.diameter = float(diameter)
        self.span = float(span)
        self.a: float = self.DEFAULT_A
        self.b: float = self.DEFAULT_B

    def _boundary_error(self, a: float, b: float) -> float:
        """Compute the sum of absolute errors at the endpoints for given a and b."""
        try:
            y1 = self.diameter / 2
            y2 = self.diameter / 2
            e1 = a * math.cosh((0 - b) / a) - y1
            e2 = a * math.cosh((self.span - b) / a) - y2
            return abs(e1) + abs(e2)
        except Exception:
            return self.INF

    def fit_parameters(
        self, precision: float = DEFAULT_PRECISION
    ) -> Tuple[float, float]:
        """
        Find the optimal catenary parameters a and b to fit the endpoints.

        Args:
            precision: Desired precision for parameter fitting.

        Returns:
            Tuple of optimised (a, b).
        """
        step = self.DEFAULT_STEP
        error = self.INF
        a, b = self.DEFAULT_A, self.DEFAULT_B

        while error > precision:
            improved = False
            best_error = error
            best_a, best_b = a, b

            for candidate_a in [a - step, a, a + step]:
                for candidate_b in [b - step, b, b + step]:
                    candidate_error = self._boundary_error(candidate_a, candidate_b)
                    if candidate_error < best_error:
                        best_error = candidate_error
                        best_a, best_b = candidate_a, candidate_b
                        improved = True

            if not improved:
                step /= self.STEP_REDUCTION_FACTOR
                if step < precision:
                    break
            else:
                a, b = best_a, best_b
                error = best_error

        self.a, self.b = a, b
        return a, b

    def area_under_curve(self) -> float:
        """Calculate the area under the catenary curve between endpoints."""
        a = self.a
        return math.pi * (a**2) * (math.sinh(self.span / a) + (self.span / a))

    def midpoint_radius(self) -> float:
        """Compute the vertical position (radius) of the catenary at the midpoint."""
        a, b = self.a, self.b
        midpoint_x = self.span / 2
        return a * math.cosh((midpoint_x - b) / a)

    def midpoint_dip(self) -> float:
        """Calculate the sag (dip) at the midpoint compared to endpoints."""
        return (self.diameter / 2) - self.midpoint_radius()

    def midpoint_gap(self) -> float:
        """Compute twice the midpoint radius (vertical gap at centre)."""
        return 2 * self.midpoint_radius()

    def summary(self) -> str:
        """Return a summary of the catenary's geometric properties as a string."""
        return (
            f"Catenary for diameter {self.diameter} and span {self.span}:\n"
            f"  Parameters (a, b): ({self.a:.7f}, {self.b:.7f})\n"
            f"  Area under curve: {self.area_under_curve():.7f}\n"
            f"  Midpoint dip: {self.midpoint_dip():.7f}\n"
            f"  Midpoint gap: {self.midpoint_gap():.7f}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Calculate catenary parameters and properties for given diameter and span."
    )
    parser.add_argument(
        "diameter",
        type=float,
        help="Vertical distance (diameter) at endpoints (metres)",
    )
    parser.add_argument(
        "span", type=float, help="Horizontal distance between endpoints (metres)"
    )
    parser.add_argument(
        "--precision",
        type=float,
        default=Catenary.DEFAULT_PRECISION,
        help=f"Desired precision for parameter fitting (default: {Catenary.DEFAULT_PRECISION})",
    )

    args = parser.parse_args()

    catenary = Catenary(args.diameter, args.span)
    catenary.fit_parameters(precision=args.precision)
    print(catenary.summary())


if __name__ == "__main__":
    main()
