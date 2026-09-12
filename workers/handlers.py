# Fibonacci function to calculate the nth fibonacci number
def fibonacci(payload):
    if "n" not in payload:
            raise ValueError("Missing 'n' in payload.")
    n = payload["n"]

    if n < 0:
        raise ValueError("Input should be a non-negative integer.")
    

    a, b = 0, 1
    for _ in range(n):
        c = a + b
        a = b
        b = c
        return {"result": a}

# Prime check function to determine whether a number is prime or not
def prime_check(payload):
    if "n" not in payload:
        raise ValueError("Missing 'n' in payload.")
    n = payload["n"]

    if n < 2:
        return {"result": False}

    for i in range(2, int (n**0.5) + 1):
        if n % i == 0:
            return {"result": False}
    return {"result": True}

def compute_reactions(P, L, a):
    # R1 = Reaction at support 1
    # R2 = Reaction at support 2
    # P = Point load
    # L = Length of the beam
    # a = Length of point load P from R1
    R1 = P * (L - a) / L
    R2 = P * a / L
    return R1, R2

# Internal Shear Force at the cut left from point load P
def V(x, P, R1, a):
    # x = distance of the cut from R1
    if x < a:
         return R1
    else:
        return R1 - P

# Bending moment at the cut
def M(x, P, R1, a):
    if x < a:
        return R1 * x
    else:
        return R1 * x - P * (x - a)

def compute_bending_stress(M_max, c, I):
    # c = extreme fiber distance
    # M_max = Maximum bending moment
    return abs(M_max) * float(c) / float(I)

# Beam calculation function to compute reactions, shear force, bending moment and bending stress
def beam_calculation(payload):
    required = {"length", "load", "load_position", "second_moment_of_area", "extreme_fiber_distance"}
    provided = payload.keys()
    missing = required - provided

    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    L = payload["length"]
    P = payload["load"]
    a = payload["load_position"]
    I = payload["second_moment_of_area"]
    c = payload["extreme_fiber_distance"]

    R1, R2 = compute_reactions(P, L, a)
    M_max = M(a, P, R1, a)
    actual_bending_stress = compute_bending_stress(M_max, c, I)

    return {"result": actual_bending_stress}

JOB_HANDLERS ={
    "fibonacci": fibonacci,
    "prime_check": prime_check,
    "beam_calculation": beam_calculation
}