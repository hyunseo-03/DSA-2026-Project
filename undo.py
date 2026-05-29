# copy를 할 때 객체의 참조가 아닌 실제 값을 복사하기 위해 deepcopy를 사용
from copy import deepcopy


#stack을 사용하여 이전 상태를 저장하는 UndoStack 클래스 정의
class UndoStack:
    def __init__(self, limit: int) -> None:
        #limit는 저장할 수 있는 최대 상태 수를 의미. limit를 초과하면 가장 오래된 상태가 삭제됨
        self.limit = limit
        self._states = []

    def push(self, state) -> None:
        #state는 현재 게임 상태를 나타내는 객체. deepcopy를 사용하여 객체의 참조가 아닌 실제 값을 복사하여 저장
        self._states.append(deepcopy(state))
        if len(self._states) > self.limit:
            self._states.pop(0)

    def pop(self):
        if not self._states:
            return None
        return self._states.pop()

    def __len__(self) -> int:
        return len(self._states)
