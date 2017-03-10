__author__ = 'Rico'


# game_handler handles the blackJack-game-objects. When a new object is created, it is saved in "GameList"
# get_index_by_chatid returns the index of a running game in the list
class GameHandler(object):

    GameList = []*0         # List, where the running Games are stored in

    def get_index_by_chatid(self, chat_id):
        index = 0
        for game in self.GameList:
            if game.chat_id == chat_id:
                return index
            index += 1
        return -1

    def gl_create(self):
        self.GameList = []*0

    def gl_remove(self, chat_id):
        index = self.get_index_by_chatid(chat_id)
        if not index == -1:
            self.GameList.pop(index)

    def add_game(self, blackjackgame):
        self.GameList.append(blackjackgame)

    def get_game_by_chatid(self, chat_id):
        index = self.get_index_by_chatid(chat_id)
        return self.GameList[index]

    def get_game_by_index(self, index):
        return self.GameList[index]

    def __init__(self):
        self.GameList = []*0
