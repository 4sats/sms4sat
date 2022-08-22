from flask import Flask, request, Response
import json
import sys
from database import Database
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import config
import requests
app = Flask(__name__)

@app.route('/<path:path>',methods=['POST'])
def foo(path):
   if request.remote_addr == "165.227.164.18":
        print(path + request.remote_addr + str(request.json)+" fuck meeeeeeee", file=sys.stderr)
        service = Database().get_service(path)
        phone = requests.get(" http://api.sms-man.com/stubs/handler_api.php?action=getNumber&api_key="+config.APIKEY_SMS+"&service="+str(service[0])+"&country="+str(service[1]))
        bot = Bot(token=config.TOKEN)
        if "NO_NUMBERS" in phone.text:
            amount = Database().get_cost(path)
            lnurlw = requests.post("https://legend.lnbits.com/withdraw/api/v1/links", data = '{"title": "'+str(path)+'", "min_withdrawable": '+str(amount)+', "max_withdrawable": '+str(amount)+', "uses": 1, "wait_time": 1, "is_unique": true}', headers = {"X-Api-Key": config.APIKEY_LN_ADMIN,"Content-type": "application/json"})
            bot.edit_message_text(chat_id=service[2],message_id=service[3], text= "Sorry there was no phone numbers for this service at the moment here is your lnurl withdraw:\n`"+lnurlw["lnurl"]+"`", parse_mode = ParseMode.MARKDOWN )
        elif "NO_BALANCE" in phone.text:
            amount = Database().get_cost(path)
            lnurlw = requests.post("https://legend.lnbits.com/withdraw/api/v1/links", data = '{"title": "'+str(path)+'", "min_withdrawable": '+str(amount)+', "max_withdrawable": '+str(amount)+', "uses": 1, "wait_time": 1, "is_unique": true}', headers = {"X-Api-Key": config.APIKEY_LN_ADMIN,"Content-type": "application/json"})
            bot.edit_message_text(chat_id=service[2],message_id=service[3], text= "Sorry the bot is not active rn here is your lnurl withdraw:\n`"+lnurlw["lnurl"]+"`", parse_mode = ParseMode.MARKDOWN)
        elif "ACCESS_NUMBER" in phone.text:
            number = phone.text.split(":")
            Database().set_sms(number[1],True, path)
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