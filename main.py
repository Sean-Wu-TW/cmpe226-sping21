from sqls import *

class UserInfo():
    def __init__(self, email, name, userid, timezone, currency, lang, avatar):
        self.credentials = {
            'email': email,
            'name': name,
            'userid': userid,
            'timezone': timezone,
            'currency': currency,
            'lang': lang,
            'avatar': avatar
        }


class Splitwise():
    
    '''states: login, sign-up, test, dash'''

    def __init__(self):
        self.user = None
        self.state = 'sign-up'

    def stateChanger(self, x):
        if x == 'exit':
            self.state = 'login'
        elif x == 'test':
            self.state = 'test'
        elif x == 'login':
            self.state = 'login'
        elif x == 'sign-up':
            self.state = 'sign-up'
        return



    def run(self):
        while 1:

            # case when user wants to login
            if self.state == 'login':
                x = input('Enter your name:')
                if x == 'exit':
                    self.state = 'login'
                    continue
                self.state = 'dash'
                continue

            # case when new user sign up
            if self.state == 'sign-up':
                email = input('Please enter email address (required) \n')
                name = input('Please enter your name (required)\n')
                password = input('Please enter password (required)\n')
                lang = input('Please enter preferred language (English)\n')
                avatar = input('Please enter avatar (https://avatar-bucket-splitwise.s3.us-west-1.amazonaws.com/1616138183icon-user-default.png)\n')
                currency = input('Please enter preferred currency (USD)\n')
                timezone = input('Please enter preferred currency (America/Los_Angeles)\n')
                #####################
                print("========= Your info: =========")
                print("email:", email)
                print('name:', name)
                print('password:', password)
                print('land:',lang)
                print('avatar:',avatar)
                print('currency:',currency)
                print('timezone:',timezone)
                #####################
                insertNewUser(email, name, password, timezone, currency, lang, avatar)
                self.stateChanger('test')
                continue

            # admin testing tool
            if self.state == 'test':
                print("Fetching users...")
                print(returnAllUsers())
                x = input("now what?")
                self.stateChanger(x)
                continue


            # case when user logins into the dashboard
            if self.state == 'dash':
                print("What do you want to do?")
                print("1. Add group")
                print("2. Quit from a group")
                print("test - admin tool")
                x = input()
                
                if x == 'exit':
                    self.state = 'login'
                    continue
                else:
                    self.state = x
                continue
            # TODOs:
            # display user balance
            # display groupsthat user is in
            # Split bill between groups
            # 



            else:
                return

if __name__ == '__main__':
    app = Splitwise()
    app.run()
