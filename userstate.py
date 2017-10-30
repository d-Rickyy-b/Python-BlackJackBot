class UserState(object):
    IDLE = 0
    COMMENTING = 1
    PLAYING = 2

    def __init__(self, user_id):
        self._user_id = user_id
        self._state = UserState.IDLE

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def get_userid(self):
        return self._user_id
