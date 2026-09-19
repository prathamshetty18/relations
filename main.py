"""
main.py

Main entry point for the Relation Property Checker application.
Prompts the user to input a set A and relation R, parses them into Python set objects,
and prints whether R is reflexive, irreflexive, symmetric, antisymmetric, asymmetric,
or transitive, along with detailed explanations and counterexamples when applicable.
"""

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


def format_set(s: set) -> str:
    """Formats a set into standard string notation, e.g., {1, 2, 3}."""
    sorted_elements = sorted(list(s))
    return "{" + ", ".join(sorted_elements) + "}"


def format_relation(R: set[tuple[str, str]]) -> str:
    """Formats a relation (set of tuples) into standard string notation, e.g., {(1, 2), (2, 3)}."""
    sorted_pairs = sorted(list(R))
    pairs_str = ", ".join(f"({x}, {y})" for x, y in sorted_pairs)
    return "{" + pairs_str + "}"


def main():
    print("=" * 65)
    print("                 RELATION PROPERTY CHECKER")
    print("=" * 65)
    print("Input formats accepted:")
    print("  Set A:      1, 2, 3        or   {a, b, c}")
    print("  Relation R: 1 2 3 1 3 1    (space-separated pairs)")
    print("-" * 65)

    # Prompt user for inputs
    raw_a = input("\nEnter set A: ")
    A = parse_set(raw_a)

    raw_r = input("Enter relation R: ")

    # Parse relation R and check for errors
    print()
    try:
        R = parse_relation(raw_r, A)
    except ValueError:
        return

    print("-" * 65)
    print(f"Set A      = {format_set(A)}")
    print(f"Relation R = {format_relation(R)}")

    print("-" * 65)
    print("ANALYSIS RESULTS:")
    print("-" * 65)

    # 1. Reflexive Check
    is_refl, ce_refl = reflexive(A, R)
    if is_refl:
        print("- Reflexive:     YES")
        print("  Reason: For every element x in A, (x, x) is in R.")
    else:
        x, _ = ce_refl
        print("- Reflexive:     NO")
        print(f"  Reason: Element '{x}' is in A, but ({x}, {x}) is NOT in R.")

    # 2. Irreflexive Check
    is_irrefl, ce_irrefl = irreflexive(A, R)
    if is_irrefl:
        print("\n- Irreflexive:   YES")
        print("  Reason: For every element x in A, (x, x) is NOT in R.")
    else:
        x, _ = ce_irrefl
        print("\n- Irreflexive:   NO")
        print(f"  Reason: Element '{x}' is in A, and ({x}, {x}) is present in R.")

    # 3. Symmetric Check
    is_sym, ce_sym = symmetric(A, R)
    if is_sym:
        print("\n- Symmetric:     YES")
        print("  Reason: For every (x, y) in R, (y, x) is also in R.")
    else:
        x, y = ce_sym
        print("\n- Symmetric:     NO")
        print(f"  Reason: Pair ({x}, {y}) is in R, but reverse pair ({y}, {x}) is NOT in R.")

    # 4. Antisymmetric Check
    is_antisym, ce_antisym = antisymmetric(A, R)
    if is_antisym:
        print("\n- Antisymmetric: YES")
        print("  Reason: No distinct elements x != y exist where both (x, y) and (y, x) are in R.")
    else:
        x, y = ce_antisym
        print("\n- Antisymmetric: NO")
        print(f"  Reason: Distinct elements '{x}' and '{y}' have both ({x}, {y}) and ({y}, {x}) in R.")

    # 5. Asymmetric Check
    is_asym, ce_asym = asymmetric(A, R)
    if is_asym:
        print("\n- Asymmetric:    YES")
        print("  Reason: For every pair (x, y) in R, reverse pair (y, x) is NOT in R.")
    else:
        x, y = ce_asym
        if x == y:
            print("\n- Asymmetric:    NO")
            print(f"  Reason: Self-loop pair ({x}, {x}) is present in R.")
        else:
            print("\n- Asymmetric:    NO")
            print(f"  Reason: Pair ({x}, {y}) and reverse pair ({y}, {x}) are both in R.")

    # 6. Transitive Check
    is_trans, ce_trans = transitive(A, R)
    if is_trans:
        print("\n- Transitive:    YES")
        print("  Reason: For every (x, y) in R and (y, z) in R, (x, z) is also in R.")
    else:
        (x, y), (y2, z), (missing_x, missing_z) = ce_trans
        print("\n- Transitive:    NO")
        print(f"  Reason: ({x}, {y}) and ({y2}, {z}) are in R, but required pair ({missing_x}, {missing_z}) is NOT in R.")

    print("=" * 65)


if __name__ == "__main__":
    main()
