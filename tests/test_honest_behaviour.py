from kilimo_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_an_unknown_crop_has_no_cost_total_rather_than_a_total_of_zero():
    """A cost of 0 for 'quinoa' looks like an answer; it was only the absence of data."""
    r = _fn("input_cost_calculator")("quinoa", 2)
    assert r["estimated_total_kes"] is None and "note" in r["input_costs_per_acre_kes"]


def test_a_known_crop_is_still_costed_and_scales_with_acreage():
    one, two = _fn("input_cost_calculator")("maize", 1), _fn("input_cost_calculator")("maize", 2)
    assert one["estimated_total_kes"] > 0 and two["estimated_total_kes"] == 2 * one["estimated_total_kes"]
