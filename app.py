"""
app.py

Flask Web Application for analyzing binary relation properties.
Imports and reuses functions directly from relations.py without modifying its logic.

Features:
- GET & POST route for relation property checking.
- Computes relation matrix, SVG directed graph.
- Evaluates Equivalence Relation and Partial Order (Poset) separately.
- Formats reasons, counterexamples, and properties grid data.
- Supports light and dark theme adaptations.
"""

import math
from flask import Flask, render_template, request
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

app = Flask(__name__)


def format_set(s: set) -> str:
    """Formats a set of elements into mathematical notation, e.g. {1, 2, 3}."""
    sorted_elements = sorted(list(s))
    return "{" + ", ".join(sorted_elements) + "}"


def format_relation(R: set[tuple[str, str]]) -> str:
    """Formats a set of relation pairs into mathematical notation, e.g. {(1,2), (3,1)}."""
    sorted_pairs = sorted(list(R))
    pairs_str = ", ".join(f"({x},{y})" for x, y in sorted_pairs)
    return "{" + pairs_str + "}"


def generate_svg_graph(A: set[str], R: set[tuple[str, str]]) -> str:
    """
    Generates a clean SVG directed graph representing set A and relation R.
    Nodes are arranged in a circle with directed arrows and curved self-loops.
    Uses CSS classes for theme adaptability (Dark/Light mode).
    """
    sorted_A = sorted(list(A))
    n = len(sorted_A)
    if n == 0:
        return "<p class='empty-graph'>Set A is empty. No graph to display.</p>"

    width, height = 380, 380
    cx, cy = width / 2, height / 2
    r_circle = 125 if n > 1 else 0
    node_r = 20

    # Calculate (x, y) coordinates for each node on a circle
    coords = {}
    for idx, elem in enumerate(sorted_A):
        if n == 1:
            coords[elem] = (cx, cy)
        else:
            angle = (2 * math.pi * idx / n) - (math.pi / 2)
            x = cx + r_circle * math.cos(angle)
            y = cy + r_circle * math.sin(angle)
            coords[elem] = (x, y)

    svg_lines = [
        f'<svg viewBox="0 0 {width} {height}" class="graph-svg" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#6366f1" />',
        '    </marker>',
        '    <marker id="arrow-loop" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#8b5cf6" />',
        '    </marker>',
        '  </defs>'
    ]

    # Draw Edges first
    for u, v in R:
        if u not in coords or v not in coords:
            continue
        x1, y1 = coords[u]
        x2, y2 = coords[v]

        if u == v:
            # Self-loop arc
            dx, dy = x1 - cx, y1 - cy
            dist = math.hypot(dx, dy)
            if dist == 0:
                ux, uy = 0, -1
            else:
                ux, uy = dx / dist, dy / dist

            perp_x, perp_y = -uy, ux
            sx = x1 + ux * node_r + perp_x * 6
            sy = y1 + uy * node_r + perp_y * 6
            ex = x1 + ux * node_r - perp_x * 6
            ey = y1 + uy * node_r - perp_x * 6
            cp_x = x1 + ux * (node_r + 42)
            cp_y = y1 + uy * (node_r + 42)

            svg_lines.append(
                f'  <path d="M {sx:.1f} {sy:.1f} Q {cp_x:.1f} {cp_y:.1f} {ex:.1f} {ey:.1f}" '
                f'fill="none" stroke="#8b5cf6" stroke-width="2" marker-end="url(#arrow-loop)"/>'
            )
        else:
            # Directed edge between distinct nodes u -> v
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            ux, uy = dx / dist, dy / dist

            sx = x1 + ux * node_r
            sy = y1 + uy * node_r
            ex = x2 - ux * node_r
            ey = y2 - uy * node_r

            # If reverse edge (v, u) also exists, curve the line so both are visible
            if (v, u) in R:
                perp_x, perp_y = -uy, ux
                mx = (sx + ex) / 2 + perp_x * 18
                my = (sy + ey) / 2 + perp_y * 18
                svg_lines.append(
                    f'  <path d="M {sx:.1f} {sy:.1f} Q {mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}" '
                    f'fill="none" stroke="#6366f1" stroke-width="2" marker-end="url(#arrow)"/>'
                )
            else:
                svg_lines.append(
                    f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                    f'stroke="#6366f1" stroke-width="2" marker-end="url(#arrow)"/>'
                )

    # Draw Nodes on top
    for elem in sorted_A:
        nx, ny = coords[elem]
        svg_lines.append('  <g class="graph-node">')
        svg_lines.append(
            f'    <circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r}" class="node-circle" stroke="#6366f1" stroke-width="2.5"/>'
        )
        svg_lines.append(
            f'    <text x="{nx:.1f}" y="{ny + 5:.1f}" text-anchor="middle" class="node-text" font-size="13" font-weight="bold">{elem}</text>'
        )
        svg_lines.append('  </g>')

    svg_lines.append('</svg>')
    return "\n".join(svg_lines)


@app.route("/", methods=["GET", "POST"])
def index():
    raw_a = ""
    raw_r = ""
    error = None
    results = None
    set_a_str = ""
    relation_r_str = ""

    if request.method == "POST":
        raw_a = request.form.get("set_a", "").strip()
        raw_r = request.form.get("relation_r", "").strip()

        if not raw_a:
            error = "Error: Set A cannot be empty. Please enter space or comma separated elements."
        else:
            try:
                # 1. Parse Set A using relations.py parse_set
                A = parse_set(raw_a)
                if not A:
                    raise ValueError("Error: Set A contains no valid elements.")

                # 2. Parse Relation R using relations.py parse_relation
                R = parse_relation(raw_r, A)

                # Format set and relation text
                set_a_str = f"A = {format_set(A)}"
                relation_r_str = f"R = {format_relation(R)}"

                # 3. Evaluate Relation Properties via relations.py functions
                is_refl, ce_refl = reflexive(A, R)
                is_irrefl, ce_irrefl = irreflexive(A, R)
                is_sym, ce_sym = symmetric(A, R)
                is_antisym, ce_antisym = antisymmetric(A, R)
                is_asym, ce_asym = asymmetric(A, R)
                is_trans, ce_trans = transitive(A, R)

                # Reasons & Counterexamples
                reason_refl = (
                    "For every x ∈ A, (x, x) ∈ R."
                    if is_refl
                    else f"Element '{ce_refl[0]}' ∈ A, but ({ce_refl[0]}, {ce_refl[0]}) ∉ R."
                )

                reason_irrefl = (
                    "For every x ∈ A, (x, x) ∉ R."
                    if is_irrefl
                    else f"Element '{ce_irrefl[0]}' ∈ A, and ({ce_irrefl[0]}, {ce_irrefl[0]}) ∈ R."
                )

                reason_sym = (
                    "For every (x, y) ∈ R, reverse pair (y, x) ∈ R."
                    if is_sym
                    else f"Pair ({ce_sym[0]}, {ce_sym[1]}) ∈ R, but ({ce_sym[1]}, {ce_sym[0]}) ∉ R."
                )

                reason_antisym = (
                    "No distinct x ≠ y exist where both (x, y) ∈ R and (y, x) ∈ R."
                    if is_antisym
                    else f"Distinct '{ce_antisym[0]}' and '{ce_antisym[1]}' have both ({ce_antisym[0]}, {ce_antisym[1]}) ∈ R and ({ce_antisym[1]}, {ce_antisym[0]}) ∈ R."
                )

                if is_asym:
                    reason_asym = "For every (x, y) ∈ R, reverse pair (y, x) ∉ R."
                else:
                    if ce_asym[0] == ce_asym[1]:
                        reason_asym = f"Self-loop pair ({ce_asym[0]}, {ce_asym[0]}) is in R."
                    else:
                        reason_asym = f"Pair ({ce_asym[0]}, {ce_asym[1]}) and ({ce_asym[1]}, {ce_asym[0]}) are both in R."

                if is_trans:
                    reason_trans = "For every (x, y) ∈ R and (y, z) ∈ R, (x, z) ∈ R."
                else:
                    (x, y), (y2, z), (missing_x, missing_z) = ce_trans
                    reason_trans = f"({x}, {y}) ∈ R and ({y2}, {z}) ∈ R, but required ({missing_x}, {missing_z}) ∉ R."

                # Build 6-properties grid data
                properties_list = [
                    {
                        "name": "Reflexive",
                        "definition": "∀x ∈ A, (x, x) ∈ R",
                        "satisfied": is_refl,
                        "reason": reason_refl,
                    },
                    {
                        "name": "Irreflexive",
                        "definition": "∀x ∈ A, (x, x) ∉ R",
                        "satisfied": is_irrefl,
                        "reason": reason_irrefl,
                    },
                    {
                        "name": "Symmetric",
                        "definition": "∀x,y ∈ A, (x, y) ∈ R ⇒ (y, x) ∈ R",
                        "satisfied": is_sym,
                        "reason": reason_sym,
                    },
                    {
                        "name": "Antisymmetric",
                        "definition": "∀x,y ∈ A, (x,y) ∈ R ∧ (y,x) ∈ R ⇒ x = y",
                        "satisfied": is_antisym,
                        "reason": reason_antisym,
                    },
                    {
                        "name": "Asymmetric",
                        "definition": "∀x,y ∈ A, (x, y) ∈ R ⇒ (y, x) ∉ R",
                        "satisfied": is_asym,
                        "reason": reason_asym,
                    },
                    {
                        "name": "Transitive",
                        "definition": "∀x,y,z ∈ A, (x,y) ∈ R ∧ (y,z) ∈ R ⇒ (x,z) ∈ R",
                        "satisfied": is_trans,
                        "reason": reason_trans,
                    },
                ]

                # 4A. Evaluate Equivalence Relation (Reflexive + Symmetric + Transitive)
                is_equivalence = is_refl and is_sym and is_trans
                missing_eq = []
                if not is_refl:
                    missing_eq.append("Reflexivity")
                if not is_sym:
                    missing_eq.append("Symmetry")
                if not is_trans:
                    missing_eq.append("Transitivity")

                if is_equivalence:
                    eq_reason = "Relation R is an Equivalence Relation because it satisfies Reflexivity, Symmetry, and Transitivity."
                else:
                    eq_reason = f"Relation R is NOT an Equivalence Relation because it lacks: {', '.join(missing_eq)}."

                equivalence_data = {
                    "is_satisfied": is_equivalence,
                    "title": "Equivalence Relation",
                    "badge": "YES" if is_equivalence else "NO",
                    "reason": eq_reason,
                    "requirements": [
                        {"name": "Reflexive", "ok": is_refl},
                        {"name": "Symmetric", "ok": is_sym},
                        {"name": "Transitive", "ok": is_trans},
                    ],
                }

                # 4B. Evaluate Partial Order / Poset (Reflexive + Antisymmetric + Transitive)
                is_partial_order = is_refl and is_antisym and is_trans
                missing_po = []
                if not is_refl:
                    missing_po.append("Reflexivity")
                if not is_antisym:
                    missing_po.append("Antisymmetry")
                if not is_trans:
                    missing_po.append("Transitivity")

                if is_partial_order:
                    po_reason = "Relation R is a Partial Order (Poset) because it satisfies Reflexivity, Antisymmetry, and Transitivity."
                else:
                    po_reason = f"Relation R is NOT a Partial Order because it lacks: {', '.join(missing_po)}."

                poset_data = {
                    "is_satisfied": is_partial_order,
                    "title": "Partial Order (Poset)",
                    "badge": "YES" if is_partial_order else "NO",
                    "reason": po_reason,
                    "requirements": [
                        {"name": "Reflexive", "ok": is_refl},
                        {"name": "Antisymmetric", "ok": is_antisym},
                        {"name": "Transitive", "ok": is_trans},
                    ],
                }

                # 5. Build Relation Matrix
                sorted_A = sorted(list(A))
                matrix_data = {
                    "headers": sorted_A,
                    "rows": [
                        {
                            "element": x,
                            "cells": [
                                {
                                    "value": 1 if (x, y) in R else 0,
                                    "is_diagonal": (x == y)
                                }
                                for y in sorted_A
                            ]
                        }
                        for x in sorted_A
                    ]
                }

                # 6. Build SVG Graph
                svg_graph = generate_svg_graph(A, R)

                results = {
                    "properties": properties_list,
                    "equivalence": equivalence_data,
                    "poset": poset_data,
                    "matrix": matrix_data,
                    "svg_graph": svg_graph,
                }

            except ValueError as ve:
                error = str(ve)

    return render_template(
        "index.html",
        raw_a=raw_a,
        raw_r=raw_r,
        error=error,
        results=results,
        set_a_str=set_a_str,
        relation_r_str=relation_r_str,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
