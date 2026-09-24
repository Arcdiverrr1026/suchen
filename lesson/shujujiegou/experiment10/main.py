"""Polynomial derivative using linked list.

Each node has (coef, expn, next).
Input polynomial terms interactively, compute and output the derivative.
"""

from __future__ import annotations


class _TermNode:
    __slots__ = ("coef", "expn", "next")

    def __init__(self, coef: float = 0.0, expn: int = 0, next_node: _TermNode | None = None) -> None:
        self.coef = coef
        self.expn = expn
        self.next = next_node


class Polynomial:
    """Univariate polynomial stored as a sorted linked list of terms."""

    def __init__(self) -> None:
        self._head = _TermNode()  # sentinel node

    def add_term(self, coef: float, expn: int) -> None:
        """Add a term. Maintains ascending order by exponent."""
        if coef == 0:
            return
        prev = self._head
        curr = prev.next
        while curr is not None and curr.expn < expn:
            prev = curr
            curr = curr.next
        if curr is not None and curr.expn == expn:
            curr.coef += coef
            if curr.coef == 0:
                prev.next = curr.next
        else:
            new_node = _TermNode(coef, expn, curr)
            prev.next = new_node

    def derivative(self) -> Polynomial:
        """Return the derivative polynomial."""
        result = Polynomial()
        node = self._head.next
        while node is not None:
            if node.expn > 0:
                result.add_term(node.coef * node.expn, node.expn - 1)
            node = node.next
        return result

    def display(self) -> str:
        """Return a human-readable string of the polynomial."""
        terms: list[str] = []
        node = self._head.next
        if node is None:
            return "0"

        while node is not None:
            coef = node.coef
            expn = node.expn

            # Format coefficient
            if expn == 0:
                terms.append(f"{coef:g}")
            elif coef == 1:
                if expn == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{expn}")
            elif coef == -1:
                if expn == 1:
                    terms.append("-x")
                else:
                    terms.append(f"-x^{expn}")
            else:
                if expn == 1:
                    terms.append(f"{coef:g}x")
                else:
                    terms.append(f"{coef:g}x^{expn}")

            node = node.next

        result = " + ".join(terms)
        result = result.replace(" + -", " - ")
        return result if result else "0"


def main() -> None:
    poly = Polynomial()

    n = int(input("请输入多项式项数："))
    for i in range(n):
        parts = input(f"请输入第{i+1}项的系数和指数（空格分隔）：").split()
        coef, expn = float(parts[0]), int(parts[1])
        poly.add_term(coef, expn)

    print(f"多项式: P(x) = {poly.display()}")

    deriv = poly.derivative()
    print(f"导数: P'(x) = {deriv.display()}")


if __name__ == "__main__":
    main()
