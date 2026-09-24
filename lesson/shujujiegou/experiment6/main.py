"""Sequential storage linear list with insert and delete operations.

Command line: interactive prompts for insert/delete operations.
Output the list after each successful operation, or an error message on failure.
"""

MAX_SIZE = 100


class SeqList:
    """Linear list implemented with a fixed-size array."""

    def __init__(self) -> None:
        self._data: list[int] = []
        self._max_size = MAX_SIZE

    @property
    def length(self) -> int:
        return len(self._data)

    def insert(self, pos: int, elem: int) -> bool:
        """Insert elem at position pos (1-indexed). Return True on success."""
        if pos < 1 or pos > self.length + 1:
            return False
        if self.length >= self._max_size:
            return False
        self._data.insert(pos - 1, elem)
        return True

    def delete(self, pos: int) -> tuple[bool, int | None]:
        """Delete element at position pos (1-indexed). Return (success, element)."""
        if pos < 1 or pos > self.length:
            return False, None
        elem = self._data.pop(pos - 1)
        return True, elem

    def display(self) -> str:
        return "(" + ",".join(str(x) for x in self._data) + ")"


def main() -> None:
    lst = SeqList()

    while True:
        choice = input("是否要对线性表进行插入和删除？（Y/N）").strip().upper()
        if choice != "Y":
            break

        op = input("进行插入还是删除？（1--插入，2--删除）").strip()
        if op == "1":
            parts = input("请输入插入位置和元素（空格分隔）：").split()
            pos, elem = int(parts[0]), int(parts[1])
            if lst.insert(pos, elem):
                print(lst.display())
            else:
                print("插入位置有误")
        elif op == "2":
            pos = int(input("请输入删除位置："))
            ok, _ = lst.delete(pos)
            if ok:
                print(lst.display())
            else:
                print("删除位置有误")


if __name__ == "__main__":
    main()
