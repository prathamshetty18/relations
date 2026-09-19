"""
relations.py

Functions to parse sets and binary relations from string inputs,
and to test mathematical properties of relations on a given set A:
- Reflexive
- Irreflexive
- Symmetric
- Antisymmetric
- Asymmetric
- Transitive

Each property checking function returns a tuple: (is_property: bool, counterexample).
"""

import re


def parse_set(input_str: str) -> set[str]:
    """
    Parses a user input string into a set of elements (strings).

    Supports input formats like:
    - Comma-separated: "1, 2, 3"
    - Space-separated: "1 2 3"
    - Set notation: "{1, 2, 3}"
    """
    # Remove leading/trailing curly braces and whitespace
    cleaned = input_str.strip().strip("{}")
    if not cleaned:
        return set()

    # Split by comma if present, otherwise split by whitespace
    if "," in cleaned:
        elements = [item.strip() for item in cleaned.split(",") if item.strip()]
    else:
        elements = [item.strip() for item in cleaned.split() if item.strip()]

    return set(elements)


def parse_relation(input_str: str, A: set[str] = None) -> set[tuple[str, str]]:
    """
    Parses a user input string of space-separated elements into a set of ordered pairs.

    Example input: "1 2 3 1 3 1" -> {('1', '2'), ('3', '1')}

    Args:
        input_str: Space-separated elements representing relation pairs.
        A: Optional set of allowed elements. If provided, validates that all
           relation elements belong to set A.

    Returns:
        set of (x, y) tuples representing the relation R.

    Raises:
        ValueError: If the number of elements is odd, or if an element is not in set A.
    """
    # Split input string into a list of space-separated elements
    elements = input_str.strip().split()

    if not elements:
        print("R = {}")
        return set()

    # Show an error if the number of elements is odd
    if len(elements) % 2 != 0:
        error_msg = f"Error: The number of elements is odd ({len(elements)}). Relation pairs must consist of 2 elements each."
        print(error_msg)
        raise ValueError(error_msg)

    # Show an error if any element is not in set A
    if A is not None:
        for elem in elements:
            if elem not in A:
                error_msg = f"Error: Element '{elem}' is not in set A."
                print(error_msg)
                raise ValueError(error_msg)

    # Group every 2 consecutive elements into a tuple and store in a set (removes duplicates)
    relation = set()
    for i in range(0, len(elements), 2):
        relation.add((elements[i], elements[i + 1]))

    # Print relation in the form R = {(1,2), (3,1)} for user confirmation
    sorted_pairs = sorted(list(relation))
    pairs_str = ", ".join(f"({x},{y})" for x, y in sorted_pairs)
    print(f"R = {{{pairs_str}}}")

    return relation


def reflexive(A: set[str], R: set[tuple[str, str]]) -> tuple[bool, tuple[str, str] | None]:
    """
    Checks if relation R is reflexive on set A.
    Definition: For every element x in A, the pair (x, x) must be in R.

    Returns:
        (True, None) if reflexive.
        (False, (x, x)) as counterexample if (x, x) is missing from R.
    """
    for x in A:
        if (x, x) not in R:
            return False, (x, x)
    return True, None


def irreflexive(A: set[str], R: set[tuple[str, str]]) -> tuple[bool, tuple[str, str] | None]:
    """
    Checks if relation R is irreflexive on set A.
    Definition: For every element x in A, the pair (x, x) must NOT be in R.

    Returns:
        (True, None) if irreflexive.
        (False, (x, x)) as counterexample if (x, x) is present in R.
    """
    for x in A:
        if (x, x) in R:
            return False, (x, x)
    return True, None


def symmetric(A: set[str], R: set[tuple[str, str]]) -> tuple[bool, tuple[str, str] | None]:
    """
    Checks if relation R is symmetric.
    Definition: For every (x, y) in R, the pair (y, x) must also be in R.

    Returns:
        (True, None) if symmetric.
        (False, (x, y)) as counterexample if (y, x) is missing from R.
    """
    for x, y in R:
        if (y, x) not in R:
            return False, (x, y)
    return True, None


def antisymmetric(A: set[str], R: set[tuple[str, str]]) -> tuple[bool, tuple[str, str] | None]:
    """
    Checks if relation R is antisymmetric.
    Definition: For every (x, y) in R with x != y, (y, x) must NOT be in R.

    Returns:
        (True, None) if antisymmetric.
        (False, (x, y)) as counterexample if both (x, y) and (y, x) exist for x != y.
    """
    for x, y in R:
        if x != y and (y, x) in R:
            return False, (x, y)
    return True, None


def asymmetric(A: set[str], R: set[tuple[str, str]]) -> tuple[bool, tuple[str, str] | None]:
    """
    Checks if relation R is asymmetric.
    Definition: For every (x, y) in R, (y, x) must NOT be in R.
    (Note: Asymmetry excludes both symmetric reverse pairs and self-loops (x, x)).

    Returns:
        (True, None) if asymmetric.
        (False, (x, y)) as counterexample if (y, x) is also in R.
    """
    for x, y in R:
        if (y, x) in R:
            return False, (x, y)
    return True, None


def transitive(A: set[str], R: set[tuple[str, str]]) -> tuple[bool, tuple[tuple[str, str], tuple[str, str], tuple[str, str]] | None]:
    """
    Checks if relation R is transitive.
    Definition: For every (x, y) in R and (y, z) in R, (x, z) must also be in R.

    Returns:
        (True, None) if transitive.
        (False, ((x, y), (y, z), (x, z))) as counterexample if (x, z) is missing from R.
    """
    for x, y in R:
        for y2, z in R:
            if y == y2:
                if (x, z) not in R:
                    return False, ((x, y), (y, z), (x, z))
    return True, None
