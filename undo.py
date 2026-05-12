from copy import deepcopy


class UndoStack:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self._states = []

    def push(self, state) -> None:
        self._states.append(deepcopy(state))
        if len(self._states) > self.limit:
            self._states.pop(0)

    def pop(self):
        if not self._states:
            return None
        return self._states.pop()

    def __len__(self) -> int:
        return len(self._states)
