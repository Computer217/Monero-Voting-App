#widget onscreen control that the user interacts with 
#kivy not found bc of the interpreter used by visual code 



import random
import time 
import sys

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from database import DataBase

from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from decimal import Decimal

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

candidates = 4
names = ["Bob", "Alice", "Eve", "Mal"]

with open("wallets.txt", "r") as f:
    wallets = f.readlines()
    wallets = [x.strip("\n") for x in wallets] 
db = DataBase("./monero/", wallets)


class Voting_Screen(App):
    def build(self):
        layout = BoxLayout(padding=10,orientation='vertical')
        colors = [green, blue, red, purple]

        #an entry for each number of candidates
        for i in range(candidates):
            btn = Button(text="Candidate"+ str(names[i]) + "#%s" % (i+1),
                         background_color=colors[i]
                         )

            btn.bind(on_press=self.on_press_button)
            layout.add_widget(btn)
        return layout

    def on_press_button(self, instance, voter = db.current_voter()):
        candidate = instance.text
        address = db.get_address(candidate)

        try:
            login = "monero-wallet-rpc --testnet --wallet-file" + str(voter[0]) + "--password" + str(voter[1])+ "--rpc-bind-port 28088 --disable-rpc-login"
            child = pexpect.spawn(login, encoding='utf-8')
        except:
            print("error voting")

        w = Wallet(JSONRPCWallet(port=28088))

        #send 1 vote
        txs = w.transfer(address, Decimal('1.0'))
        
        #destroy wallet 
        wallets = db.current_wallets()
        db = DataBase("./monero/", wallets)


        print("You voted for " + candidate)
        sys.exit()

        return 0


class LoginScreen(App):
    def build(self):
        pass


if __name__ == "__main__":
    app = Voting_Screen()
    app.run()
    