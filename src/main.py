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
        self.state = 'login'
        self.help = 'login \ntest \ninvites \nsign-up \nexit'

    def stateChanger(self, x):
        if x == 'exit':
            self.state = 'login'
        elif x == 'test':
            self.state = 'test'
        elif x == 'login':
            self.state = 'login'
        elif x == 'sign-up':
            self.state = 'sign-up'
        elif x == 'invites':
            self.state = 'invites'
        return



    def run(self):
        
        while 1:

            # Login
            if self.state == 'login':
                x = input('Please log in:')
                print('logged in as default user')
                print('1@user.com','user1','12345','21','America/Los_Angeles','USD','English',
                    'https://avatar-bucket-splitwise.s3.us-west-1.amazonaws.com/1616181139user-icon.png')

                print('======')
                print(self.help)
                x = input("what's next?")
                self.stateChanger(x)
                continue

            # Sign up
            if self.state == 'sign-up':
                email = input('Please enter email address (required) \n')
                if not self.validate(email, 'email'):
                    continue
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
                print('Processing your data...')
                #####################

                # if user exists: login
                valid = True
                allUsers = returnAllUsers()
                for user in allUsers:
                    if email == user[0]:
                        print('User exists, please re-enter user info')
                        valid = False
                        continue

                if valid:
                    insertNewUser(email, name, password, timezone, currency, lang, avatar)
                    self.stateChanger('test')
                    continue
                else:
                    print('insert failed')
                    print('======')
                    print(self.help)
                    x = input("what's next?")
                    self.stateChanger(x)
                    continue


            # admin testing tool
            if self.state == 'test':
                print("Fetching users...")
                print(returnAllUsers())
                print('======')
                print(self.help)
                x = input("what's next?")
                self.stateChanger(x)
                continue


            # case when user logins into the dashboard
            if self.state == 'dash':
                print("What do you want to do?")
                print("1. Add group")
                print("2. Quit from a group")
                print("3. See group info")
                print("test - admin tool")
                print('======')
                print(self.help)
                x = input("what's next?")
                self.stateChanger(x)
                continue


            # TODOs:
            # display user balance
            # display groupsthat user is in
            # Split bill between groups
            # 

            # view invitations
            if self.state == 'invites':
                res = invitations(self.credentials.email)
                print(res)
                print('======')
                print(self.help)
                x = input("what's next?")
                self.stateChanger(x)
                continue



            else:
                return



    def validate(self, string, kind):
        if kind == 'email':
            if '@' not in string:
                print('******please enter a valid email address******')
                return False

if __name__ == '__main__':
    app = Splitwise()
    app.run()
