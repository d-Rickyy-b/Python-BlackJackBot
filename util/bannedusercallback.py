# -*- coding: utf-8 -*-

def banned_user_callback(update, context):
    """Gets called by the dispatcher when it's found that the user sending the update was banned from using the bot"""
    banned_text = "You have been banned from using this bot!"
    
    if update.callback_query:
        update.callback_query.answer(banned_text)
    else:
        update.effective_message.reply_text(banned_text)
