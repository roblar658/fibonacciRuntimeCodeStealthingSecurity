import math
from typing import Callable, Tuple

# --- Implementation 1: Iterative Two-Variable ---
def fib_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# --- Implementation 2: Dynamic Programming Table ---
def fib_dp(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]

# --- Implementation 3: 2x2 Matrix Exponentiation (O(log n)) ---
def fib_matrix(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    def multiply(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        # [[a0, a1], [a2, a3]] * [[b0, b1], [b2, b3]]
        return (
            a[0] * b[0] + a[1] * b[2],
            a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2],
            a[2] * b[1] + a[3] * b[3],
        )

    def power(mat: Tuple[int, int, int, int], p: int) -> Tuple[int, int, int, int]:
        res = (1, 0, 0, 1)  # Identity matrix
        base = mat
        while p > 0:
            if p & 1:
                res = multiply(res, base)
            base = multiply(base, base)
            p >>= 1
        return res

    t = power((1, 1, 1, 0), n - 1)
    return t[0]

# --- Implementation 4: Binet's Analytical Formula ---
def fib_binet(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    sqrt_5 = math.sqrt(5)
    phi = (1 + sqrt_5) / 2
    psi = (1 - sqrt_5) / 2
    return round((phi**n - psi**n) / sqrt_5)


# --- Replacement Candidates ---
# Fast doubling algorithm (pure integer arithmetic, O(log n))
def fib_fast_doubling(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")

    def _fib(k: int) -> Tuple[int, int]:
        if k == 0:
            return (0, 1)
        a, b = _fib(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)

    return _fib(n)[0]

# Memoized recursive approach
def fib_memoized(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {0: 0, 1: 1}
    if n not in memo:
        memo[n] = fib_memoized(n - 1, memo) + fib_memoized(n - 2, memo)
    return memo[n]


# --- Runner with Dynamic List Swapping ---
def run_dynamic_pipeline():
    # Active pool of 4 functions
    active_solvers = [fib_iterative, fib_dp, fib_matrix, fib_binet]
    
    # Pool of alternatives to swap in
    standby_solvers = [fib_fast_doubling, fib_memoized]

    queries = [0, 1, 5, 8, 10, 12]

    for step, n in enumerate(queries):
        # 1. Pop the solver from the front of the active list
        current_func: Callable[[int], int] = active_solvers.pop(0)

        # 2. Compute Fibonacci value
        result = current_func(n)
        print(f"Step {step + 1} | Executed: {current_func.__name__:<15} | fib({n}) = {result}")

        # 3. Swap in a new solver or rotate
        if standby_solvers:
            new_func = standby_solvers.pop(0)
            active_solvers.append(new_func)
            print(f"  -> Replaced with: {new_func.__name__}")
        else:
            # Recycle the evaluated function to the back of the queue
            active_solvers.append(current_func)
            print(f"  -> Recycled to tail: {current_func.__name__}")

        print(f"  Active list: {[f.__name__ for f in active_solvers]}\n")


if __name__ == "__main__":
    run_dynamic_pipeline()
