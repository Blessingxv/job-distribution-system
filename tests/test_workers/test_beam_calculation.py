from workers.handlers import beam_calculation

# Simply supported beam, point load at midspan
def test_beam_calculation_midspan_load():
    # L = 1000mm, P = 1000N, a = 500mm, I = 8333333.33 mm**4, c = 50mm
    # Expected: R1 = R2= 500N, M_max = 250000 N*mm, bending_stress = 1.5 MPa
    payload = {
        "length": 1000,
        "load": 1000,
        "load_position": 500,
        "second_moment_of_area": 8333333.33,
        "extreme_fiber_distance": 50
    }
    result = beam_calculation(payload)
    assert round(result["result"], 2) == 1.5