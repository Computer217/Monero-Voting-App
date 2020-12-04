import random
import time 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import subprocess

#from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)


class CreateAccountWindow(Screen):
    wallet_name = ObjectProperty(None)
    password = ObjectProperty(None)

    #need to test this!!!
    def submit(self):
        if self.wallet_name.text != "" and self.password.text != "":
            db.add_user(self.wallet_name.text,self.password.text)
            self.reset()
            sm.current = "login"
        else:
            invalidForm()
    
    def login(self):
        self.reset()
        sm.current = "login"
    
    def reset(self):
        self.wallet_name.text = ""
        self.password.text = ""


#LogIn Screen
class LoginWindow(Screen):
    wallet_name = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.wallet_name.text, self.password.text):
            MainWindow.current = self.wallet_name.text
            MainWindow.passcode = self.password.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()
    
    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.wallet_name.text = ""
        self.password.text = ""


#Voting Screen
class MainWindow(Screen):
    candidate1 = ObjectProperty(None)
    candidate2 = ObjectProperty(None)
    candidate3 = ObjectProperty(None)
    candidate4 = ObjectProperty(None)
    current = ""
    password = ""

    def logOut(self):
        sm.current = "login"

    def results(self):
        sm.current = "results"
    
    def on_enter(self, *args):
        self.candidate1.text, self.candidate2.text, self.candidate3.text, self.candidate4.text  = db.get_candidates()
        
    def vote(self):
        if subprocess.call(["Python3", "GUI_VOTE.PY"]) == 0:
            #erase wallet 
            sm.current = "login"



#deals with transitions
class WindowManager(ScreenManager):
    pass



def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid Wallet Name or Wallet Password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


with open("wallets.txt", "r") as f:
    wallets = f.readlines()
    wallets = [x.strip("\n") for x in wallets] 

kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase("./monero/", wallets)

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
        sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        #if doesnt work switch sm to kv
        return sm

if __name__ == "__main__":
    app=MyMainApp()
    app.run()