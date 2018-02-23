# -*- coding: utf-8 -*-
import logging


class UserState(object):
    IDLE = 0
    COMMENTING = 1
    PLAYING = 2
    state_names = ["IDLE", "COMMENTING", "PLAYING"]

    def __init__(self, user_id: int):
        self.logger = logging.getLogger(__name__)
        self._user_id = user_id
        self._state = UserState.IDLE

    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int) -> None:
        self.logger.debug("Set {}'s state to {}!".format(self._user_id, self.state_names[state]))
        self._state = state

    def get_userid(self) -> int:
        return self._user_id
