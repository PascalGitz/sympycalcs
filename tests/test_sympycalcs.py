import sys
import os

current_path = os.getcwd()
package_path = os.path.join(current_path, 'sympycalcs')  # Passe den Pfad entsprechend an

print(package_path)
if package_path not in sys.path:
    sys.path.append(package_path)



from sympy import Symbol, Eq, symbols
from helpers import *



def test_eq_subs():
    # Test case for eq_subs function
    a, b, c, q, v, t, k = symbols('a b c q v t k')

    eq_1 = Eq(a, b + c)
    eq_2 = Eq(b, q * v)
    eq_3 = Eq(c, t * k)

    # Perform substitutions
    result_eq = eq_subs(eq_1, eq_1, eq_2, eq_3)

    # Check if substitutions are applied correctly
    expected_eq = Eq(a, q * v + t * k)
    assert result_eq == expected_eq

    # Additional test case
    eq_4 = Eq(q, 5)
    result_eq = eq_subs(eq_1, eq_1, eq_2, eq_3, eq_4)

    # Check if substitutions are applied correctly
    expected_eq = Eq(a, 5 * v + t * k)
    assert result_eq == expected_eq

    # Test with a self-referencing equation
    eq_5 = Eq(b, a)
    result_eq = eq_subs(eq_5, eq_5)

    # Check if the function handles self-referencing equations correctly
    assert result_eq == eq_5

test_eq_subs()