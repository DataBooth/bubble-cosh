import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import math
    import plotly.graph_objs as go
    from scipy.optimize import minimize_scalar

    return go, math


@app.cell
def _():
    # --- CONSTANTS ---

    INF = 1e12  # A very large number used as a fallback for error cases or to represent 'infinite' error
    DEFAULT_A = (
        1.0  # Default initial guess for the catenary parameter 'a' (curve steepness)
    )
    DEFAULT_B = 1.0  # Default initial guess for the catenary parameter 'b' (curve horizontal offset)
    DEFAULT_STEP = (
        0.1  # Initial step size for the grid search when fitting catenary parameters
    )
    STEP_REDUCTION_FACTOR = (
        10.0  # Factor by which the step size is reduced during each refinement cycle
    )
    DEFAULT_PRECISION = 1e-7  # Target precision for parameter fitting (stopping criterion for optimization)

    # --- Constants for constraints ---

    MAX_SPAN_RATIO = 0.6627  # Maximum allowed span as a fraction of diameter for a valid catenary solution (approximate value)
    MIN_DIAMETER = 0.5  # Minimum allowed diameter value for the UI slider (meters)
    MAX_DIAMETER = 2.0  # Maximum allowed diameter value for the UI slider (meters)
    MIN_SPAN = 0.1  # Minimum allowed span value for the UI slider (meters)
    MAX_SPAN = MAX_SPAN_RATIO * MAX_DIAMETER
    return (
        DEFAULT_A,
        DEFAULT_B,
        DEFAULT_PRECISION,
        DEFAULT_STEP,
        INF,
        MAX_DIAMETER,
        MAX_SPAN_RATIO,
        MIN_DIAMETER,
        MIN_SPAN,
        STEP_REDUCTION_FACTOR,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    # Interactive Catenary Curve Explorer

    This notebook demonstrates the properties of a **catenary** curve, also known as a "chainette" or "alysoid."  
    A catenary is the shape assumed by a flexible, uniform chain or cable suspended by its ends and acted on only by gravity.

    **References:**

    - [Wikipedia: Catenary](https://en.wikipedia.org/wiki/Catenary)
    - [MathWorld: Catenary](https://mathworld.wolfram.com/Catenary.html)
    """
    )
    return


@app.cell
def _(
    DEFAULT_A,
    DEFAULT_B,
    DEFAULT_PRECISION,
    DEFAULT_STEP,
    INF,
    STEP_REDUCTION_FACTOR,
    go,
    math,
):
    class Catenary:
        """
        Represents a catenary curve defined by its endpoints and diameter.

        A catenary is the curve formed by a perfectly flexible, uniform chain or cable
        suspended by its ends and acted on only by gravity. Mathematically, it is described
        by the equation y = a * cosh((x - b) / a), where 'a' determines the curve's steepness
        and 'b' its horizontal offset.
        """

        def __init__(self, diameter: float, span: float) -> None:
            """
            Initialise a Catenary object.

            Args:
                diameter: Vertical distance between endpoints (metres).
                span: Horizontal distance between endpoints (metres).
            """
            self.diameter = float(diameter)
            self.span = float(span)
            self.a: float = DEFAULT_A
            self.b: float = DEFAULT_B

        def _boundary_error(self, a: float, b: float) -> float:
            """Return the error in the boundary condition for given a, b."""
            try:
                y1 = self.diameter / 2
                y2 = self.diameter / 2
                e1 = a * math.cosh((0 - b) / a) - y1
                e2 = a * math.cosh((self.span - b) / a) - y2
                return abs(e1) + abs(e2)
            except Exception:
                return INF

        def fit_parameters(
            self, precision: float = DEFAULT_PRECISION
        ) -> tuple[float, float]:
            """
            Fit the catenary parameters 'a' and 'b' to satisfy the boundary conditions.

            Args:
                precision: Target precision for parameter fitting.

            Returns:
                Tuple of (a, b).
            """
            step = DEFAULT_STEP
            error = INF
            a, b = DEFAULT_A, DEFAULT_B

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
                    step /= STEP_REDUCTION_FACTOR
                    if step < precision:
                        break
                else:
                    a, b = best_a, best_b
                    error = best_error

            self.a, self.b = a, b
            return a, b

        def y(self, x: float) -> float:
            """Return the y-coordinate of the catenary at position x."""
            return self.a * math.cosh((x - self.b) / self.a)

        def area_under_curve(self) -> float:
            """Return the area under the catenary curve (metres squared)."""
            a = self.a
            return math.pi * (a**2) * (math.sinh(self.span / a) + (self.span / a))

        def midpoint_radius(self) -> float:
            """Return the radius at the midpoint of the span."""
            a, b = self.a, self.b
            midpoint_x = self.span / 2
            return a * math.cosh((midpoint_x - b) / a)

        def midpoint_dip(self) -> float:
            """Return the dip at the midpoint relative to the endpoints."""
            return (self.diameter / 2) - self.midpoint_radius()

        def midpoint_gap(self) -> float:
            """Return the gap at the midpoint (twice the radius at midpoint)."""
            return 2 * self.midpoint_radius()

        def plot(
            self,
            num_points: int = 200,
            x_range: tuple[float, float] = None,
            y_range: tuple[float, float] = (0, 1.5),
            height: int = 700,
            show_endpoints: bool = True,
        ):
            """
            Plot the catenary curve using Plotly.

            Args:
                num_points: Number of points to plot along the curve.
                x_range: Tuple (min_x, max_x) for the x-axis. If None, uses sensible defaults.
                y_range: Tuple (min_y, max_y) for the y-axis.
                height: Height of the plot in pixels.
                show_endpoints: Whether to show the endpoints as red markers.

            Returns:
                Plotly Figure object.
            """
            # Default x_range: from -(span-1) to next 0.1 above span
            if x_range is None:
                import math

                x_max = math.ceil(self.span * 10) / 10
                x_min = -(self.span - 1)
                x_range = (x_min, x_max)

            x_vals = [i * self.span / (num_points - 1) for i in range(num_points)]
            y_vals = [self.y(x) for x in x_vals]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Catenary Curve")
            )
            fig.update_layout(
                title="Catenary Curve",
                xaxis_title="Horizontal Distance (m)",
                yaxis_title="Vertical Position (m)",
                height=height,
                xaxis=dict(range=list(x_range)),
                yaxis=dict(range=list(y_range)),
            )
            if show_endpoints:
                fig.add_trace(
                    go.Scatter(
                        x=[0, self.span],
                        y=[self.diameter / 2, self.diameter / 2],
                        mode="markers",
                        marker=dict(size=10, color="red"),
                        name="Endpoints",
                    )
                )
            return fig

        def describe(self) -> str:
            """
            Return a Markdown-formatted summary of the catenary's parameters and geometric properties.

            Returns:
                str: Markdown string for display in marimo or other Markdown renderers.
            """
            return (
                f"**Catenary parameters:**\n\n"
                f"- a = `{self.a:.6f}`\n"
                f"- b = `{self.b:.6f}`\n\n"
                f"**Geometric properties:**\n\n"
                f"- Area under curve: `{self.area_under_curve():.6f} m²`\n"
                f"- Midpoint dip: `{self.midpoint_dip():.6f} m`\n"
                f"- Midpoint gap: `{self.midpoint_gap():.6f} m`\n"
            )

    return (Catenary,)


@app.cell
def _(MAX_DIAMETER, MIN_DIAMETER, mo):
    # --- UI controls ---

    diameter = mo.ui.slider(
        start=MIN_DIAMETER,
        stop=MAX_DIAMETER,
        value=1.0,
        step=0.01,
        label="Diameter (m)",
    )
    return (diameter,)


@app.cell
def _(MAX_SPAN_RATIO, diameter):
    # Compute the maximum allowable span for the current diameter

    max_span = round(MAX_SPAN_RATIO * diameter.value, 4)

    return (max_span,)


@app.cell
def _(MIN_SPAN, max_span, mo):
    span = mo.ui.slider(
        start=MIN_SPAN,
        stop=max_span,
        value=min(0.6, max_span),
        step=0.01,
        label="Span (m)",
    )
    return (span,)


@app.cell
def _(MAX_SPAN_RATIO, diameter, max_span, mo):
    mo.md(
        f"""
    ### Catenary Parameter Constraints

    - The **span** (horizontal distance between endpoints) must not exceed **{MAX_SPAN_RATIO:.2f} × diameter** (vertical distance between endpoints).
    - For the current diameter (**{diameter.value:.2f} m**), the maximum allowed span is **{max_span:.4f} m**.
    - This limit is based on practical engineering guidelines for safe and realistic catenary curves, not a strict mathematical maximum.
    - Horizontal distance between endpoints. Must be less than {MAX_SPAN_RATIO:.2f} times the diameter.
    - Vertical distance between endpoints. Must be positive.

    **References:**  

    - [Wikipedia: Catenary](https://en.wikipedia.org/wiki/Catenary)  
    - [Engineering practice for catenary sag](https://jlengineering.net/blog/wp-content/uploads/2018/02/Aerial-Power-Cables.pdf)

    ## Interactive Catenary Visualisation

    Adjust the sliders for **Diameter** and **Span** to see how the catenary curve changes.
    """
    )
    return


@app.cell
def _(Catenary, diameter, mo, span):
    # --- Try to compute catenary ---

    try:
        catenary = Catenary(diameter.value, span.value)
        a, b = catenary.fit_parameters()

    except Exception as e:
        mo.md(f"**Error occurred:** {e}")
    return (catenary,)


@app.cell
def _(diameter, mo, span):
    # --- Show controls stacked ---

    mo.hstack([diameter, span])
    return


@app.cell
def _(catenary):
    catenary.plot(x_range=(-0.2, 1.4), y_range=(0.0, 1.2))
    return


@app.cell
def _(catenary, mo):
    mo.md(catenary.describe())
    return


if __name__ == "__main__":
    app.run()
