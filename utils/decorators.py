from time import time
"""
import into other python files like

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT)
from utils.decorators import timeit
"""

def timeit(func):
    """
    Decorator to measure the execution time of a function
    @timeit to use
    """
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        delta = time() - start_time
        print(f"Function {func.__name__} took {delta:.2f} seconds to execute.")
        return result
    return wrapper