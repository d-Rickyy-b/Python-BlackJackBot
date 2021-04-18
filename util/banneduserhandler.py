# -*- coding: utf-8 -*-
from telegram.ext import TypeHandler

import database


class BannedUserHandler(TypeHandler):

    def check_update(self, update):
        db = database.Database()
        if db.is_user_banned(update.effective_user.id):
            return True
        return False
