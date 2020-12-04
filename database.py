#Database file incharged of interacting with the monero 
#CLI Wallet 
import pexpect
import time


global voter

class DataBase:
    def __init__(self,path, wallets):
        self.path = path
        self.users = None
        self.file = None
        self.wallets = wallets

    def add_user(self, wallet, password):
        """
        this function creates a new wallet entry in the "data base" for new users signing up
        """

        if str(wallet) not in self.wallets:
            file1 = open("wallets.txt","w") 
            file1.write(str(wallet) + " \n") 
            file1.close() #to change file access modes 

            creation_wallet = self.path + "monero-wallet-cli --testnet --generate-new-wallet testnet/" + str(wallet) + ".bin  --password " + str(password) + " --log-file testnet/" + str(wallet) + ".log"
            print(creation_wallet)
            child = pexpect.spawn(creation_wallet, encoding='utf-8')

            try:
                child.expect("choice:")
                child.sendline("1")
                print("complete generation")
                child.expect("now?")
                child.sendline("No")
                print("complete verification")
                child.expect(".*") #started
                child.sendline("exit")
                print("success")
            except:
                print("oops, wallet did not generate :(")
                print(str(child))
        else:
            print("wallet already exists")

    def get_candidates(self):
        """
        this function returns a list of the candidates that are being voted 
        """
        w = "Mal"
        x = "Bob"
        y = "Alice"
        z = "Eve"

        return x,y,z,w

    def current_wallets(self):
        return voter

    def get_address(self, candidate):
        address = {"Mal": "9yXRNZCnbYdPtZi9rHe7Pd38LLyf8kXtdgcjHe7LEKhMC8VZDLKWQc6YyzrqD6sp2vVUB3YUV9YWvV2oM266WYdq6yya9MF",
        "Bob":"9y8cPFZbDVzDK53bgUaudu7kDW4UxBpyWLggepNYSJm2BTshStgbnjtNweZiyYGK4ZK1SpRULBntJF1BpF7ohVT5PGE8jKB",
        "Alice": "9wviCeWe2D8XS82k2ovp5EUYLzBt9pYNW2LXUFsZiv8S3Mt21FZ5qQaAroko1enzw3eGr9qC7X1D7Geoo2RrAotYPwq9Gm8",
        "Eve": "9yFZgFZbDVzDK53bgUaudu7kDW4UxBpyWLggepNYSJm2BTshStgbnjtNweZiyYGK4ZK1SpRULBntJF1BpF7ohVT5PGE8jKB"}

        return address[candidate]




    def validate(self, walletname, password):
        """
        this function logs into the wallet
        if login is successful, voting option will be prompted 
        """

        validate_login = self.path + "monero-wallet-rpc --testnet --wallet-file /testnet/"+ str(walletname) + "  --password "+ str(password) + " --rpc-bind-port 28089 --disable-rpc-login"
        print(validate_login)

        try:
            child = pexpect.spawn(validate_login, encoding='utf-8')
            child.expect(".*") #wallet initialized correctly
            child.sendline("exit")
            voter = (walletname, password)
            print(voter[0])
            return True

        except:
            print("validation of wallet failed ")
            return False
    
        
    
