from sqls import *

class UserInfo():
    def __init__(self):
        self.credentials = {
            'email': "",
            'name': "",
            'userid': "",
            'timezone': "America/Los_Angeles",
            'currency': "USD",
            'lang': "English",
            'avatar': "https://avatar-bucket-splitwise.s3.us-west-1.amazonaws.com/1616181139user-icon.png",
            'admin': []
        }
    def userBuilder(self, key, value):
        ''' Builds the user info '''
        self.credentials[key] = value
        return self

    def Print(self):
        print(self.credentials)




class Splitwise():
    
    '''states: login, sign-up, test, dash'''

    def __init__(self):
        self.user = None
        self.state = 'login'
        self.help = 'login \ntest(fetches all users)\
         \ninvites \nsign-up \nexit'

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

    def nextStateOpt(self):
        print('======')
        print(self.help)
        x = input("what's next?")
        self.stateChanger(x)



    def run(self):
        
        while 1:

            # Login
            if self.state == 'login':
                x = input('Please log in:')




                print('logged in as default user')
                print('1@user.com','user1','21','America/Los_Angeles','USD','English',
                    'https://avatar-bucket-splitwise.s3.us-west-1.amazonaws.com/1616181139user-icon.png')
                self.user = UserInfo('1@user.com','user1','21','America/Los_Angeles','USD','English',
                    'https://avatar-bucket-splitwise.s3.us-west-1.amazonaws.com/1616181139user-icon.png')

                self.nextStateOpt()
                continue

            # Sign up
            if self.state == 'sign-up':
                email = input('Please enter email address (required) \n')
                # if not self.validate(email, 'email'):
                #     continue
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
                if lang == "": lang = None
                if avatar == "": avatar = None
                if currency == "": currency = None
                if timezone == "": timezone = None


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
                    self.nextStateOpt()
                    continue


            # admin testing tool
            if self.state == 'test':
                print("Fetching users...")
                print(returnAllUsers())
                self.nextStateOpt()
                continue


            # case when user logins into the dashboard
            if self.state == 'dash':
                print("What do you want to do?")
                print("1. Add group")
                print("2. Quit from a group")
                print("3. See group info")
                print("test - admin tool")
                self.nextStateOpt()
                continue


            # TODOs:
            # display user balance
            # display groupsthat user is in
            # Split bill between groups
            # 

            # view invitations
            if self.state == 'invites':
                res = invitations(self.user.credentials.get('email'))
                if res:
                    print(res)
                    self.nextStateOpt()
                    continue
                else:
                    print('You have no pending invitations.')
                    self.nextStateOpt()
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
