# -*- coding: utf-8 -*-
import unittest
from random import randint

from database import Database


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        # Use random IDs so that the tests don't interfere with existing data in the database file
        self.user_id = randint(10 ** 9, 10 ** 10)
        self.addCleanup(self._delete_user, self.user_id)

    def _delete_user(self, user_id):
        self.db.cursor.execute("DELETE FROM users WHERE user_id=?;", [str(user_id)])
        self.db.cursor.execute("DELETE FROM chats WHERE chat_id=?;", [str(user_id)])
        self.db.connection.commit()
        self.db.get_banned_users().discard(user_id)

    def test_unban_not_banned_user(self):
        """Unbanning a user who is not banned must not raise an error"""
        self.db.unban_user(self.user_id)
        self.assertFalse(self.db.is_user_banned(self.user_id))

    def test_ban_unknown_user_persists(self):
        """Banning a user who never used the bot must be stored in the database, not only in memory"""
        self.db.ban_user(self.user_id)

        self.assertTrue(self.db.is_user_banned(self.user_id))
        user = self.db.get_user(self.user_id)
        self.assertIsNotNone(user)
        self.assertEqual(1, user["banned"])

    def test_add_user_without_language_code(self):
        """Users without a language_code must be stored with the default language"""
        self.db.add_user(self.user_id, None, "first", "last", "username")

        self.assertIsNotNone(self.db.get_user(self.user_id))
        self.db.cursor.execute("SELECT lang_id FROM chats WHERE chat_id=?;", [str(self.user_id)])
        self.assertEqual("en", self.db.cursor.fetchone()["lang_id"])

    def test_add_user_with_existing_chat(self):
        """Users whose private chat is already stored (e.g. after using /language) must still be added"""
        self.db.set_lang_id(chat_id=self.user_id, lang_id="de")

        self.db.add_user(self.user_id, "en", "first", "last", "username")

        self.assertIsNotNone(self.db.get_user(self.user_id))
        self.db.cursor.execute("SELECT lang_id FROM chats WHERE chat_id=?;", [str(self.user_id)])
        self.assertEqual("de", self.db.cursor.fetchone()["lang_id"])


if __name__ == '__main__':
    unittest.main()
