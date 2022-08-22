from flask import Flask, request, Response
import json
import sys
from database import Database
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
import config
import requests
app = Flask(__name__)

@app.route('/<path:path>',methods=['POST'])
def foo(path):
   if request.remote_addr == "165.227.164.18":
        print(path + request.remote_addr + str(request.json)+" fuck meeeeeeee", file=sys.stderr)
        service = Database().get_service(path)
        phone = requests.get(" http://api.sms-man.com/stubs/handler_api.php?action=getNumber&api_key="+config.APIKEY_SMS+"&service="+str(service[0])+"&country="+str(service[1]))
        number = phone.text.split(":")
        Database().set_sms(number[1],True, path)
        bot = Bot(token=config.TOKEN)
        keyboard = [
        [
            InlineKeyboardButton("Get Code", callback_data="check_sms"),
        ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id=service[2],message_id=service[3], text= "Send verification code to this phone number: +"+number[2] , reply_markup=reply_markup)
   return Response(status=200)

if __name__ == '__main__':
   app.run()