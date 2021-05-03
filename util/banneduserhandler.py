# -*- coding: utf-8 -*-
import logging

from telegram.ext import TypeHandler

import database


class BannedUserHandler(TypeHandler):
    logger = logging.getLogger()

    def check_update(self, update):
        db = database.Database()
        user = update.effective_user

        if user is None:
            self.logger.warning(f"User is None! Update: {update}")
            return False

        if db.is_user_banned(user.id):
            return True

        return False
