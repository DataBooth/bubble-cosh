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
    return go, math


@app.cell
def _():
    # --- CONSTANTS ---
    INF = 1e12
    DEFAULT_A = 1.0
    DEFAULT_B = 1.0
    DEFAULT_STEP = 0.1
    STEP_REDUCTION_FACTOR = 10.0
    DEFAULT_PRECISION = 1e-7
    return (
        DEFAULT_A,
        DEFAULT_B,
        DEFAULT_PRECISION,
        DEFAULT_STEP,
        INF,
        STEP_REDUCTION_FACTOR,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    # Interactive Catenary Curve Explorer

    This notebook demonstrates the properties of a catenary curve, also known as a "chainette" or "alysoid."
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
    math,
):
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
        """

        def __init__(self, diameter: float, span: float) -> None:
            self.diameter = float(diameter)
            self.span = float(span)
            self.a: float = DEFAULT_A
            self.b: float = DEFAULT_B

        def _boundary_error(self, a: float, b: float) -> float:
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
            return self.a * math.cosh((x - self.b) / self.a)

        def area_under_curve(self) -> float:
            a = self.a
            return math.pi * (a**2) * (math.sinh(self.span / a) + (self.span / a))

        def midpoint_radius(self) -> float:
            a, b = self.a, self.b
            midpoint_x = self.span / 2
            return a * math.cosh((midpoint_x - b) / a)

        def midpoint_dip(self) -> float:
            return (self.diameter / 2) - self.midpoint_radius()

        def midpoint_gap(self) -> float:
            return 2 * self.midpoint_radius()


    return (Catenary,)


@app.cell
def _(mo):
    # --- Interactive controls using marimo UI elements ---
    diameter = mo.ui.slider(start=0.5, stop=2.0, value=1.0, step=0.01, label="Diameter (m)")
    span = mo.ui.slider(start=0.1, stop=2.0, value=0.6, step=0.01, label="Span (m)")
    return diameter, span


@app.cell
def _(mo):
    # --- Display controls, plot, and properties ---
    mo.md(f"""
    ## Interactive Catenary Visualization

    Adjust the sliders for **Diameter** and **Span** to see how the catenary curve changes.

    """)
    return


@app.cell
def _(diameter):
    diameter
    return


@app.cell
def _(span):
    span
    return


@app.cell
def _(Catenary, diameter, span):
    # --- Compute catenary parameters and properties ---
    catenary = Catenary(diameter.value, span.value)
    a, b = catenary.fit_parameters()
    return a, b, catenary


@app.cell
def _(catenary, span):
    # --- Prepare data for plotting ---
    num_points = 200
    x_vals = [i * span.value / (num_points - 1) for i in range(num_points)]
    y_vals = [catenary.y(x) for x in x_vals]
    return x_vals, y_vals


@app.cell
def _(diameter, go, span, x_vals, y_vals):
    # --- Plotly plot ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Catenary Curve"))
    fig.update_layout(
        title="Catenary Curve",
        xaxis_title="Horizontal Distance (m)",
        yaxis_title="Vertical Position (m)",
        height=400,
    )
    fig.add_trace(
        go.Scatter(
            x=[0, span.value],
            y=[diameter.value / 2, diameter.value / 2],
            mode="markers",
            marker=dict(size=10, color="red"),
            name="Endpoints",
        )
    )
    return


@app.cell
def _(a, b, catenary, mo):
    # Markdown and computed properties
    mo.md(f"""
    **Catenary parameters:**

    - a = `{a:.6f}`
    - b = `{b:.6f}`

    **Geometric properties:**

    - Area under curve: `{catenary.area_under_curve():.6f} m²`
    - Midpoint dip: `{catenary.midpoint_dip():.6f} m`
    - Midpoint gap: `{catenary.midpoint_gap():.6f} m`
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
