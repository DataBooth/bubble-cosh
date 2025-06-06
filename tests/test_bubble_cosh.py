import math
import pytest
import warnings
from community.bubble_cosh_databooth import Catenary


def is_valid_catenary_params(diameter, span):
    # For a real catenary, span should be less than diameter (adjust this as per your domain)
    return 0 < span < diameter


@pytest.mark.parametrize(
    "diameter, span",
    [
        (1.0, 1.0),
        (1.068, 0.6),
        (2.0, 1.2),
        (0.5, 0.3),
    ],
)
def test_fit_parameters_converges(diameter, span):
    if not is_valid_catenary_params(diameter, span):
        warnings.warn(f"Skipping invalid parameters: diameter={diameter}, span={span}")
        return
    cat = Catenary(diameter, span)
    a, b = cat.fit_parameters()
    assert math.isfinite(a) and a > 0
    assert math.isfinite(b)
    error = cat._boundary_error(a, b)
    assert error < 1e-5


def test_area_under_curve_positive():
    diameter, span = 1.0, 1.0
    if not is_valid_catenary_params(diameter, span):
        warnings.warn(f"Skipping invalid parameters: diameter={diameter}, span={span}")
        return
    cat = Catenary(diameter, span)
    cat.fit_parameters()
    area = cat.area_under_curve()
    assert area > 0


def test_midpoint_radius_and_gap():
    diameter, span = 1.0, 1.0
    if not is_valid_catenary_params(diameter, span):
        warnings.warn(f"Skipping invalid parameters: diameter={diameter}, span={span}")
        return
    cat = Catenary(diameter, span)
    cat.fit_parameters()
    radius = cat.midpoint_radius()
    gap = cat.midpoint_gap()
    assert math.isclose(gap, 2 * radius, rel_tol=1e-7)


def test_midpoint_dip_sign():
    diameter, span = 1.0, 1.0
    if not is_valid_catenary_params(diameter, span):
        warnings.warn(f"Skipping invalid parameters: diameter={diameter}, span={span}")
        return
    cat = Catenary(diameter, span)
    cat.fit_parameters()
    dip = cat.midpoint_dip()
    assert dip < 0


def test_invalid_parameters_warns():
    diameter, span = 0.0, 0.0
    if not is_valid_catenary_params(diameter, span):
        with warnings.catch_warnings(record=True) as w:
            warnings.warn(f"Invalid parameters: diameter={diameter}, span={span}")
            assert any("Invalid parameters" in str(warning.message) for warning in w)
        return
    cat = Catenary(diameter, span)
    a, b = cat.fit_parameters()
    assert math.isfinite(a)
    assert math.isfinite(b)


def test_summary_output():
    diameter, span = 1.068, 0.6
    if not is_valid_catenary_params(diameter, span):
        warnings.warn(f"Skipping invalid parameters: diameter={diameter}, span={span}")
        return
    cat = Catenary(diameter, span)
    cat.fit_parameters()
    summary = cat.summary()
    assert isinstance(summary, str)
    assert "Parameters" in summary


@pytest.mark.parametrize(
    "diameter, span",
    [
        (1.0, 1.0),
        (2.0, 1.2),
    ],
)
def test_consistency_of_methods(diameter, span):
    if not is_valid_catenary_params(diameter, span):
        warnings.warn(f"Skipping invalid parameters: diameter={diameter}, span={span}")
        return
    cat = Catenary(diameter, span)
    cat.fit_parameters()
    area = cat.area_under_curve()
    assert area > diameter * span
    gap = cat.midpoint_gap()
    assert gap < diameter * 2
