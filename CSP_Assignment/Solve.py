from collections import deque
from time import perf_counter
from typing import Dict, List, Optional, Set, Tuple

Cell = Tuple[int, int]
Domains = Dict[Cell, Set[int]]


class SudokuCSP:
    SIZE = 9
    DIGITS = set(range(1, 10))

    def __init__(self, puzzle: str) -> None:
        self.puzzle = puzzle.strip()
        self.variables: List[Cell] = [
            (row, col)
            for row in range(self.SIZE)
            for col in range(self.SIZE)
        ]
        self.neighbors: Dict[Cell, Set[Cell]] = {
            cell: self.checkAxes(cell) for cell in self.variables
        }
        self.domains: Domains = self._build_domains()

    def _build_domains(self) -> Domains:
        domains: Domains = {}
        for index, char in enumerate(self.puzzle):
            cell = (index // 9, index % 9)
            domains[cell] = {int(char)} if char != "0" else set(self.DIGITS)
        return domains

    def checkAxes(self, cell: Cell) -> Set[Cell]:
        row, col = cell

        row_peers = {(row, c) for c in range(9) if c != col}
        col_peers = {(r, col) for r in range(9) if r != row}

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        box_peers = {
            (r, c)
            for r in range(box_row, box_row + 3)
            for c in range(box_col, box_col + 3)
            if (r, c) != cell
        }
        return row_peers | col_peers | box_peers

    def checkIfUsed(self, cell: Cell, value: int, domains: Domains) -> bool:
        for peer in self.neighbors[cell]:
            if len(domains[peer]) == 1 and value in domains[peer]:
                return True
        return False


class SudokuSolver:
    def __init__(self, csp: SudokuCSP) -> None:
        self.csp = csp
        self.node_expansions = 0
        self.backtracks = 0
        self.ac3_revisions = 0
        self.elapsed_seconds = 0.0

    @staticmethod
    def _copy_domains(domains: Domains) -> Domains:
        return {cell: set(values) for cell, values in domains.items()}

    def revise(self, domains: Domains, xi: Cell, xj: Cell) -> bool:
        to_remove: List[int] = []

        for x in domains[xi]:
            has_support = any(x != y for y in domains[xj])
            if not has_support:
                to_remove.append(x)

        if not to_remove:
            return False

        for value in to_remove:
            domains[xi].remove(value)
            self.ac3_revisions += 1
        return True

    def ac3(
        self,
        domains: Domains,
        initial_queue: Optional[List[Tuple[Cell, Cell]]] = None,
    ) -> bool:
        if initial_queue is None:
            queue = deque(
                (xi, xj)
                for xi in self.csp.variables
                for xj in self.csp.neighbors[xi]
            )
        else:
            queue = deque(initial_queue)

        while queue:
            xi, xj = queue.popleft()

            if self.revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False

                for xk in self.csp.neighbors[xi] - {xj}:
                    queue.append((xk, xi))

        return True

    def select_unassigned_variable(self, domains: Domains) -> Optional[Cell]:
        unassigned = [
            cell for cell in self.csp.variables if len(domains[cell]) > 1
        ]
        if not unassigned:
            return None

        return min(
            unassigned,
            key=lambda cell: (len(domains[cell]), cell[0], cell[1]),
        )

    def backtrack(self, domains: Domains) -> Optional[Domains]:
        if all(len(domains[cell]) == 1 for cell in self.csp.variables):
            return domains

        cell = self.select_unassigned_variable(domains)
        if cell is None:
            return None

        for value in sorted(domains[cell]):
            self.node_expansions += 1

            if self.csp.checkIfUsed(cell, value, domains):
                self.backtracks += 1
                continue

            child_domains = self._copy_domains(domains)
            child_domains[cell] = {value}

            queue = [
                (peer, cell) for peer in self.csp.neighbors[cell]
            ] + [(cell, peer) for peer in self.csp.neighbors[cell]]

            if self.ac3(child_domains, queue):
                result = self.backtrack(child_domains)
                if result is not None:
                    return result

            self.backtracks += 1

        return None

    def solve(self) -> Domains:
        start = perf_counter()
        domains = self._copy_domains(self.csp.domains)

        if not self.ac3(domains):
            raise ValueError("Puzzle is inconsistent during AC-3 preprocessing.")

        result = self.backtrack(domains)
        self.elapsed_seconds = perf_counter() - start

        if result is None:
            raise ValueError("No valid Sudoku solution exists for this puzzle.")
        return result

    def solution_string(self, domains: Domains) -> str:
        return "".join(
            str(next(iter(domains[(row, col)])))
            for row in range(9)
            for col in range(9)
        )


def main() -> None:
    input_path = "puzzles.txt"
    output_path = "solutions.txt"

    with open(input_path, "r", encoding="utf-8") as file:
        puzzles = [line.strip() for line in file if line.strip()]

    solutions: List[str] = []

    for index, puzzle in enumerate(puzzles, start=1):
        csp = SudokuCSP(puzzle)
        solver = SudokuSolver(csp)
        solved_domains = solver.solve()
        solution = solver.solution_string(solved_domains)
        solutions.append(solution)

        print(
            f"Puzzle {index}: solved | "
            f"time={solver.elapsed_seconds:.6f}s | "
            f"nodes={solver.node_expansions} | "
            f"backtracks={solver.backtracks} | "
            f"AC3 removals={solver.ac3_revisions}"
        )

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(solutions) + "\n")

    print(f"\nWrote {len(solutions)} solution(s) to {output_path}")


if __name__ == "__main__":
    main()