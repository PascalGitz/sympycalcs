import sys
import os

current_path = os.getcwd()
package_path = os.path.join(current_path, 'sympycalcs')  # Passe den Pfad entsprechend an

print(package_path)
if package_path not in sys.path:
    sys.path.append(package_path)



from sympy import Symbol, Eq, symbols
from sympycalcs import *



def test_eq_subs():
    # Test case for eq_subs function
    a, b, c, q, v, t, k = symbols('a b c q v t k')

    eq_1 = Eq(a, b + c)
    eq_2 = Eq(b, q * v)
    eq_3 = Eq(c, t * k)

    # Perform substitutions
    result_eq = to_subs(eq_1, eq_1, eq_2, eq_3)

    # Check if substitutions are applied correctly
    expected_eq = Eq(a, q * v + t * k)
    assert result_eq == expected_eq

    # Additional test case
    eq_4 = Eq(q, 5)
    result_eq = to_subs(eq_1, eq_1, eq_2, eq_3, eq_4)

    # Check if substitutions are applied correctly
    expected_eq = Eq(a, 5 * v + t * k)
    assert result_eq == expected_eq

    # Test with a self-referencing equation
    eq_5 = Eq(b, a)
    result_eq = to_subs(eq_5, eq_5)

    # Check if the function handles self-referencing equations correctly
    assert result_eq == eq_5



from sympy import Symbol, Eq
from sympy.printing import latex
from sympy.calculus.util import function_range
import pytest

@pytest.fixture
def sample_dict():
    # Create a sample dictionary for testing
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    w = Symbol('w')
    a_eq = Eq(x,y)
    b_val = 42
    c_eq = 4
    
    return {'a': a_eq, 'b': b_val, 'c': c_eq}

def test_dict_to_table(sample_dict):
    # Test case for dict_to_table function
    
    # Capture the printed output
    import io
    from contextlib import redirect_stdout
    
    with io.StringIO() as buf, redirect_stdout(buf):
        dict_to_table(sample_dict)
        output = buf.getvalue()
    
if __name__ == '__main__':
    pytest.main()




