# -*- coding: utf-8 -*-

from userstate import UserState


class StateHandler(object):
    class __StateHandler(object):
        def __init__(self):
            self.user_list = []

        def add_user(self, user_id: int) -> None:
            self.user_list.append(UserState(user_id))

        def get_user(self, user_id: int) -> UserState:
            for userState in self.user_list:
                if userState.get_userid() == user_id:
                    return userState

            self.add_user(user_id)
            return self.get_user(user_id)

    instance = None

    def __init__(self):
        if not StateHandler.instance:
            StateHandler.instance = StateHandler.__StateHandler()

    @staticmethod
    def get_instance():
        if not StateHandler.instance:
            StateHandler.instance = StateHandler.__StateHandler()

        return StateHandler.instance
