# -*- coding: utf-8 -*-


class UserState(object):
    IDLE = 0
    COMMENTING = 1
    PLAYING = 2

    def __init__(self, user_id: int):
        self._user_id = user_id
        self._state = UserState.IDLE

    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int) -> None:
        self._state = state

    def get_userid(self) -> int:
        return self._user_id
