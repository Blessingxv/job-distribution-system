from workers.handlers import fibonacci

def test_fibonacci_zero():
    # Test case 1: n = 0
    payload = {"n": 0}
    result = fibonacci(payload)
    assert( result["result"] == 0)

def test_fibonacci_ten():
    # Test case 2: n = 10
    payload = {"n": 10}
    result = fibonacci(payload)
    assert(result["result"] == 55)

