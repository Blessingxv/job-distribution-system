from workers.handlers import prime_check

# Testing whether 7 is a prime number or not
def test_prime_check_seven():
    # Test case 1: n = 7
    payload = {"n": 7}
    result = prime_check(payload)
    assert(result["result"] == True)

# Testing whether 8 is a prime number or not
def test_prime_check_eight():
    # Test case 2: n = 8
    payload = {"n": 8}
    result = prime_check(payload)
    assert(result["result"] == False)

# Testing whether 0 is a prime number or not
def test_prime_check_zero():
    # Test case 3: n = 0
    payload = {"n": 0}
    result = prime_check(payload)
    assert(result["result"] == False)

# Testing whether 2 is a prime number or not (the boundary/edge case)
def test_prime_check_two():
    # Test case 4: n = 2
    payload = {"n": 2}
    result = prime_check(payload)
    assert(result["result"] == True)

# Testing whether -1 is a prime number or not
def test_prime_check_negative():
    # Test case 5: n = -1
    payload = {"n": -1}
    result = prime_check(payload)
    assert(result["result"] == False)

