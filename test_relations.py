"""
test_relations.py

Unit tests for relations.py module using Python's built-in unittest framework.
Tests all six binary relation property checking functions (reflexive, irreflexive,
symmetric, antisymmetric, asymmetric, transitive) and input parsing error handling.
"""

import unittest
from relations import (
    parse_set,
    parse_relation,
    reflexive,
    irreflexive,
    symmetric,
    antisymmetric,
    asymmetric,
    transitive,
)


class TestRelationProperties(unittest.TestCase):

    def setUp(self):
        """Standard set A = {1, 2, 3} for testing."""
        self.A = {'1', '2', '3'}

    # -------------------------------------------------------------------------
    # Case A: Equality Relation R = {(1,1), (2,2), (3,3)} on A = {1, 2, 3}
    # -------------------------------------------------------------------------
    def test_case_a_equality_relation(self):
        R = {('1', '1'), ('2', '2'), ('3', '3')}
        
        # Reflexive: True
        is_refl, ce = reflexive(self.A, R)
        self.assertTrue(is_refl, "Equality relation should be reflexive")
        self.assertIsNone(ce)
        
        # Irreflexive: False
        is_irrefl, ce = irreflexive(self.A, R)
        self.assertFalse(is_irrefl, "Equality relation should NOT be irreflexive")
        self.assertIsNotNone(ce)
        self.assertEqual(ce[0], ce[1])
        self.assertIn(ce[0], self.A)
        self.assertIn((ce[0], ce[0]), R)
        
        # Symmetric: True
        is_sym, ce = symmetric(self.A, R)
        self.assertTrue(is_sym, "Equality relation should be symmetric")
        self.assertIsNone(ce)
        
        # Antisymmetric: True
        is_antisym, ce = antisymmetric(self.A, R)
        self.assertTrue(is_antisym, "Equality relation should be antisymmetric")
        self.assertIsNone(ce)
        
        # Asymmetric: False (due to self-loops)
        is_asym, ce = asymmetric(self.A, R)
        self.assertFalse(is_asym, "Equality relation should NOT be asymmetric")
        self.assertIsNotNone(ce)
        self.assertIn((ce[0], ce[1]), R)
        self.assertIn((ce[1], ce[0]), R)
        
        # Transitive: True
        is_trans, ce = transitive(self.A, R)
        self.assertTrue(is_trans, "Equality relation should be transitive")
        self.assertIsNone(ce)

    # -------------------------------------------------------------------------
    # Case B: Strict Order R = {(1,2), (1,3), (2,3)} on A = {1, 2, 3}
    # -------------------------------------------------------------------------
    def test_case_b_strict_order(self):
        R = {('1', '2'), ('1', '3'), ('2', '3')}
        
        # Reflexive: False (no self-loops)
        is_refl, ce = reflexive(self.A, R)
        self.assertFalse(is_refl, "Strict order should NOT be reflexive")
        self.assertIsNotNone(ce)
        self.assertEqual(ce[0], ce[1])
        self.assertIn(ce[0], self.A)
        self.assertNotIn((ce[0], ce[0]), R)
        
        # Irreflexive: True
        is_irrefl, ce = irreflexive(self.A, R)
        self.assertTrue(is_irrefl, "Strict order should be irreflexive")
        self.assertIsNone(ce)
        
        # Symmetric: False
        is_sym, ce = symmetric(self.A, R)
        self.assertFalse(is_sym, "Strict order should NOT be symmetric")
        self.assertIsNotNone(ce)
        self.assertIn((ce[0], ce[1]), R)
        self.assertNotIn((ce[1], ce[0]), R)
        
        # Antisymmetric: True
        is_antisym, ce = antisymmetric(self.A, R)
        self.assertTrue(is_antisym, "Strict order should be antisymmetric")
        self.assertIsNone(ce)
        
        # Asymmetric: True
        is_asym, ce = asymmetric(self.A, R)
        self.assertTrue(is_asym, "Strict order should be asymmetric")
        self.assertIsNone(ce)
        
        # Transitive: True
        is_trans, ce = transitive(self.A, R)
        self.assertTrue(is_trans, "Strict order should be transitive")
        self.assertIsNone(ce)

    # -------------------------------------------------------------------------
    # Case C: Symmetric Non-Transitive R = {(1,2), (2,1)} on A = {1, 2, 3}
    # -------------------------------------------------------------------------
    def test_case_c_symmetric_non_transitive(self):
        R = {('1', '2'), ('2', '1')}
        
        # Reflexive: False
        is_refl, ce = reflexive(self.A, R)
        self.assertFalse(is_refl, "R = {(1,2),(2,1)} should NOT be reflexive")
        self.assertIsNotNone(ce)
        self.assertEqual(ce[0], ce[1])
        self.assertIn(ce[0], self.A)
        self.assertNotIn((ce[0], ce[0]), R)
        
        # Irreflexive: True
        is_irrefl, ce = irreflexive(self.A, R)
        self.assertTrue(is_irrefl, "R = {(1,2),(2,1)} should be irreflexive")
        self.assertIsNone(ce)
        
        # Symmetric: True
        is_sym, ce = symmetric(self.A, R)
        self.assertTrue(is_sym, "R = {(1,2),(2,1)} should be symmetric")
        self.assertIsNone(ce)
        
        # Antisymmetric: False
        is_antisym, ce = antisymmetric(self.A, R)
        self.assertFalse(is_antisym, "R = {(1,2),(2,1)} should NOT be antisymmetric")
        self.assertIsNotNone(ce)
        self.assertNotEqual(ce[0], ce[1])
        self.assertIn((ce[0], ce[1]), R)
        self.assertIn((ce[1], ce[0]), R)
        
        # Asymmetric: False
        is_asym, ce = asymmetric(self.A, R)
        self.assertFalse(is_asym, "R = {(1,2),(2,1)} should NOT be asymmetric")
        self.assertIsNotNone(ce)
        self.assertIn((ce[0], ce[1]), R)
        self.assertIn((ce[1], ce[0]), R)
        
        # Transitive: False
        is_trans, ce = transitive(self.A, R)
        self.assertFalse(is_trans, "R = {(1,2),(2,1)} should NOT be transitive")
        self.assertIsNotNone(ce)
        p1, p2, missing = ce
        self.assertIn(p1, R)
        self.assertIn(p2, R)
        self.assertEqual(p1[1], p2[0])
        self.assertEqual(missing, (p1[0], p2[1]))
        self.assertNotIn(missing, R)

    # -------------------------------------------------------------------------
    # Case D: Divides Relation R = {(1,1),(1,2),(1,3),(2,2),(3,3)} on A = {1,2,3}
    # -------------------------------------------------------------------------
    def test_case_d_divides_relation(self):
        R = {('1', '1'), ('1', '2'), ('1', '3'), ('2', '2'), ('3', '3')}
        
        # Reflexive: True
        is_refl, ce = reflexive(self.A, R)
        self.assertTrue(is_refl, "Divides relation should be reflexive")
        self.assertIsNone(ce)
        
        # Irreflexive: False
        is_irrefl, ce = irreflexive(self.A, R)
        self.assertFalse(is_irrefl, "Divides relation should NOT be irreflexive")
        self.assertIsNotNone(ce)
        
        # Symmetric: False
        is_sym, ce = symmetric(self.A, R)
        self.assertFalse(is_sym, "Divides relation should NOT be symmetric")
        self.assertIsNotNone(ce)
        self.assertIn((ce[0], ce[1]), R)
        self.assertNotIn((ce[1], ce[0]), R)
        
        # Antisymmetric: True
        is_antisym, ce = antisymmetric(self.A, R)
        self.assertTrue(is_antisym, "Divides relation should be antisymmetric")
        self.assertIsNone(ce)
        
        # Asymmetric: False
        is_asym, ce = asymmetric(self.A, R)
        self.assertFalse(is_asym, "Divides relation should NOT be asymmetric")
        self.assertIsNotNone(ce)
        
        # Transitive: True
        is_trans, ce = transitive(self.A, R)
        self.assertTrue(is_trans, "Divides relation should be transitive")
        self.assertIsNone(ce)

    # -------------------------------------------------------------------------
    # Case E: Empty Relation R = {} on Non-Empty Set A = {1, 2, 3}
    # -------------------------------------------------------------------------
    def test_case_e_empty_relation_on_nonempty_set(self):
        R = set()
        
        # Reflexive: False
        is_refl, ce = reflexive(self.A, R)
        self.assertFalse(is_refl, "Empty relation on non-empty A should NOT be reflexive")
        self.assertIsNotNone(ce)
        self.assertEqual(ce[0], ce[1])
        self.assertIn(ce[0], self.A)
        self.assertNotIn((ce[0], ce[0]), R)
        
        # Irreflexive: True
        is_irrefl, ce = irreflexive(self.A, R)
        self.assertTrue(is_irrefl, "Empty relation should be irreflexive")
        self.assertIsNone(ce)
        
        # Symmetric: True (vacuously)
        is_sym, ce = symmetric(self.A, R)
        self.assertTrue(is_sym, "Empty relation should be symmetric")
        self.assertIsNone(ce)
        
        # Antisymmetric: True (vacuously)
        is_antisym, ce = antisymmetric(self.A, R)
        self.assertTrue(is_antisym, "Empty relation should be antisymmetric")
        self.assertIsNone(ce)
        
        # Asymmetric: True (vacuously)
        is_asym, ce = asymmetric(self.A, R)
        self.assertTrue(is_asym, "Empty relation should be asymmetric")
        self.assertIsNone(ce)
        
        # Transitive: True (vacuously)
        is_trans, ce = transitive(self.A, R)
        self.assertTrue(is_trans, "Empty relation should be transitive")
        self.assertIsNone(ce)

    # -------------------------------------------------------------------------
    # Case F: Empty Set A = {} and R = {}
    # -------------------------------------------------------------------------
    def test_case_f_empty_set(self):
        empty_A = set()
        R = set()
        
        self.assertTrue(reflexive(empty_A, R)[0], "Empty set A should be reflexive")
        self.assertTrue(irreflexive(empty_A, R)[0], "Empty set A should be irreflexive")
        self.assertTrue(symmetric(empty_A, R)[0], "Empty set A should be symmetric")
        self.assertTrue(antisymmetric(empty_A, R)[0], "Empty set A should be antisymmetric")
        self.assertTrue(asymmetric(empty_A, R)[0], "Empty set A should be asymmetric")
        self.assertTrue(transitive(empty_A, R)[0], "Empty set A should be transitive")


class TestInputParsingAndErrors(unittest.TestCase):

    def setUp(self):
        self.A = {'1', '2', '3'}

    def test_error_odd_number_of_elements(self):
        """Test error raised when relation input contains an odd number of elements."""
        with self.assertRaises(ValueError) as cm:
            parse_relation("1 2 3", self.A)
        self.assertIn("odd", str(cm.exception).lower())

    def test_error_element_not_in_set_a(self):
        """Test error raised when an element in relation is not present in set A."""
        with self.assertRaises(ValueError) as cm:
            parse_relation("1 2 4 1", self.A)
        self.assertIn("not in set a", str(cm.exception).lower())

    def test_duplicate_pairs_collapsing(self):
        """Test that duplicate pairs collapse into a single set entry."""
        R = parse_relation("1 2 1 2 1 2", self.A)
        self.assertEqual(R, {('1', '2')})
        self.assertEqual(len(R), 1)

    def test_empty_set_parsing(self):
        """Test parsing empty strings for set A and relation R."""
        parsed_empty_a = parse_set("")
        self.assertEqual(parsed_empty_a, set())

        parsed_empty_r = parse_relation("", self.A)
        self.assertEqual(parsed_empty_r, set())

    def test_bracketed_inputs(self):
        """Test parsing inputs containing delimiters like { }, ( ), [ ], < >, commas, and semicolons."""
        # Test set parsing with various brackets and delimiters
        self.assertEqual(parse_set("{1,2,3}"), {'1', '2', '3'})
        self.assertEqual(parse_set("[a, b, c]"), {'a', 'b', 'c'})
        self.assertEqual(parse_set("<1 2 3>"), {'1', '2', '3'})
        self.assertEqual(parse_set("1; 2; 3"), {'1', '2', '3'})

        # Test relation parsing with bracketed tuples and sets
        r1 = parse_relation("{(1,1),(2,2),(3,3)}", self.A)
        self.assertEqual(r1, {('1', '1'), ('2', '2'), ('3', '3')})

        r2 = parse_relation("[(1, 2), (2, 3)]", self.A)
        self.assertEqual(r2, {('1', '2'), ('2', '3')})

        r3 = parse_relation("<1, 2> <3, 1>", self.A)
        self.assertEqual(r3, {('1', '2'), ('3', '1')})

        r4 = parse_relation("1,2; 2,3", self.A)
        self.assertEqual(r4, {('1', '2'), ('2', '3')})


def run_custom_test_runner():
    """Custom test runner that outputs clear PASS/FAIL results for each test."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestRelationProperties))
    suite.addTests(loader.loadTestsFromTestCase(TestInputParsingAndErrors))

    print("=" * 70)
    print("                 RUNNING RELATIONS MODULE UNIT TESTS")
    print("=" * 70)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print(f"ALL TESTS PASSED ({result.testsRun} tests executed successfully).")
    else:
        print(f"TEST FAILURES DETECTED ({len(result.failures)} failures, {len(result.errors)} errors).")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_custom_test_runner()
    if not success:
        sys.exit(1)
