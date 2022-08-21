from flask import Flask, request, Response
import json
import sys
from database import Database
from telegram import Bot
import config
import requests
app = Flask(__name__)

@app.route('/<path:path>',methods=['POST'])
def foo(path):
   if request.remote_addr == "165.227.164.18":
        print(path + request.remote_addr + str(request.json)+" fuck meeeeeeee", file=sys.stderr)
        service = Database().get_service(path)
        phone = requests.get(" http://api.sms-man.com/stubs/handler_api.php?action=getNumber&api_key=$api_key&service="+str(service[0])+"&country="+str(service[1]))
        print(phone.text)
        #Database().set_balance(path,int(request.json["amount"]/1000))
        #bot = Bot(token=config.BOT_TOKEN)
        #bot.send_message(chat_id=path, text="Deposited "+str(int(request.json["amount"]/1000))+"sats!")

   #update balance
   #send message to user about it
   return Response(status=200)

if __name__ == '__main__':
   app.run()