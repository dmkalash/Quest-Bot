# -*- coding: utf-8 -*-

from bot import bot
from threading import Timer
from timer import check_time
import config
import handlers

import os
from flask import Flask, request
import logging
import telebot

if __name__ == '__main__':
    if config.MODE == config.OFFLINE:
        t = Timer(config.CHECKER_TIME, check_time)
        t.start()

    if "HEROKU" in list(os.environ.keys()):
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)

        server = Flask(__name__)

        @server.route("/main", methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200

        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(url="https://vmkquest.herokuapp.com/main") # мб /main
            return "?", 200

        server.run(host="0.0.0.0", port=os.environ.get('PORT', 80)) # мб || os.PORT
    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)

    # bot.infinity_polling()
