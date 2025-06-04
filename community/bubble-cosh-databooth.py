import math
from typing import Tuple


class Catenary:
    """
    Represents a catenary curve defined by its endpoints and diameter.

    A catenary is the curve formed by a perfectly flexible, uniform chain or cable
    suspended by its ends and acted on only by gravity. Mathematically, it is described
    by the equation y = a * cosh((x - b) / a), where 'a' determines the curve's steepness
    and 'b' its horizontal offset.

    The catenary is also known as the "chainette" or "alysoid." It is distinct from a
    parabola, though the two are sometimes confused in architecture and engineering.

    References:
        - Wikipedia: "Catenary" (https://en.wikipedia.org/wiki/Catenary)
        - MathWorld: "Catenary" (https://mathworld.wolfram.com/Catenary.html)
        - Weisstein, Eric W. "Catenary." MathWorld--A Wolfram Web Resource.

    This class provides methods to fit a catenary to specified endpoints and diameter,
    and to compute geometric properties such as area under the curve and midpoint sag.
    """

    # Constants
    INF: float = 1e12  # Large constant for error fallback
    DEFAULT_A: float = 1.0  # Default initial guess for catenary parameter 'a'
    DEFAULT_B: float = 1.0  # Default initial guess for catenary parameter 'b'
    DEFAULT_STEP: float = 0.1  # Initial step size for parameter search
    STEP_REDUCTION_FACTOR: float = 10.0  # Factor by which step size is reduced
    DEFAULT_PRECISION: float = 1e-7  # Default target precision for fitting

    def __init__(self, diameter: float, span: float) -> None:
        """
        Initialize the Catenary with the specified diameter and span.

        Args:
            diameter: The vertical distance (diameter) at endpoints.
            span: The horizontal distance between endpoints.
        """
        self.diameter = float(diameter)
        self.span = float(span)
        self.a: float = self.DEFAULT_A  # Catenary parameter a
        self.b: float = self.DEFAULT_B  # Catenary parameter b

    def _boundary_error(self, a: float, b: float) -> float:
        """
        Compute the sum of absolute errors at the endpoints for given a and b.

        Args:
            a: Catenary parameter a.
            b: Catenary parameter b.

        Returns:
            Sum of absolute errors at both endpoints.
        """
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
            Tuple of optimized (a, b).
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
        """
        Calculate the area under the catenary curve between endpoints.

        Returns:
            Area under the curve.
        """
        a = self.a
        return math.pi * (a**2) * (math.sinh(self.span / a) + (self.span / a))

    def midpoint_radius(self) -> float:
        """
        Compute the vertical position (radius) of the catenary at the midpoint.

        Returns:
            Midpoint vertical position.
        """
        a, b = self.a, self.b
        midpoint_x = self.span / 2
        return a * math.cosh((midpoint_x - b) / a)

    def midpoint_dip(self) -> float:
        """
        Calculate the sag (dip) at the midpoint compared to endpoints.

        Returns:
            The vertical dip at the midpoint.
        """
        return (self.diameter / 2) - self.midpoint_radius()

    def midpoint_gap(self) -> float:
        """
        Compute twice the midpoint radius (vertical gap at center).

        Returns:
            The vertical gap at the midpoint.
        """
        return 2 * self.midpoint_radius()

    def summary(self) -> None:
        """
        Print a summary of the catenary's geometric properties.
        """
        print(f"Catenary for diameter {self.diameter} and span {self.span}:")
        print(f"  Parameters (a, b): ({self.a:.7f}, {self.b:.7f})")
        print(f"  Area under curve: {self.area_under_curve():.7f}")
        print(f"  Midpoint dip: {self.midpoint_dip():.7f}")
        print(f"  Midpoint gap: {self.midpoint_gap():.7f}")


# Example usage:
if __name__ == "__main__":
    DIAMETER = 1.068  # Example diameter
    SPAN = 0.6  # Example span
    catenary = Catenary(DIAMETER, SPAN)
    catenary.fit_parameters()
    catenary.summary()
