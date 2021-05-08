from sqls import *
import readline

## Tab completer
def completer(text, state):
    commands = ['login', 'sign-up', 'add-to-group', 'dash', 'test', 'invites', 'exit',
    'groups', 'help', 'leave-group', 'info', 'delete-invite']

    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)



class UserInfo():

    def __init__(self):
        self.credentials = {
            'email': "1@user.com",
            'name': "user1",
            'userid': "21",
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

    def info(self):
        print(self.credentials)
        # output groups that your are currently in


class Splitwise():
    
    '''states: login, sign-up, test, dash, invites, dash, info, groups'''

    def __init__(self):
        self.user = None
        self.state = 'welcome'
        self.help = ['login', 'sign-up', 'add-to-group', 'dash', 'test', 'invites', 'exit',
    'groups', 'help', 'leave-group', 'info', 'delete-invite']
        self.stateLookup = {
            'exit':'login', 
            'test': 'test',
            'login':'login',
            'sign-up':'sign-up',
            'invites':'invites',
            'dash':'dash',
            'info':'info',
            'groups':'groups',
            'leave-group':'leave-group',
            'add-to-group':'add-to-group',
            'logout':'welcome',
            'delete-invite': 'delete-invite'
        }

    def stateChanger(self, x):
        nextState = self.stateLookup.get(x)
        if nextState:
            self.state = nextState


    def nextStateOpt(self):
        print('======')
        x = input("what's next? \n")
        while x == 'help':
            print(self.help)
            x = input("what's next? \n")
        self.stateChanger(x)





    def run(self):
        
        while 1:

            # welcome
            if self.state == 'welcome':
                print('*************************************************')
                print("************** Welcome to Splitwise *************")
                print('*************************************************')
                x = input('login or sign-up?\n')
                self.stateChanger(x)
                continue

            # Login
            if self.state == 'login':
                email = input('Please log in (email):')
                passw = input('Please log in (password):')
                if not email and not passw:
                    print('logged in as default user')
                    print('1@user.com','user1','21','America/Los_Angeles','USD','English',
                        'https://avatar-bucket-splitwise.s3.us-west-1.amazonaws.com/1616181139user-icon.png')
                    self.user = UserInfo()
                    self.state = 'info'
                    continue

            # This is what the user logs in sees, his/her debts
            if self.state == 'info':
                print('*************************************************')
                print("****** Displaying your account information ******")
                print('*************************************************')
                print(self.user.info())
                res = returnDebts(self.user.credentials.get('userid'))
                if res:
                    print('*************** Your debts: ***************\n')
                    print(res)
                groups = groupList(self.user.credentials.get('userid'))
                print(groups)
                self.nextStateOpt()
                continue


            #### Sign up ###
            if self.state == 'sign-up':
                print('*************************************************')
                print("******************* Sign up *********************")
                print('*************************************************')
                email = input('Please enter email address (required) \n')
                name = input('Please enter your name (required)\n')
                password = input('Please enter password (required)\n')
                confirmPassword = input('Please confirm password (required)\n')
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

                if confirmPassword != password or not email or not password or not name:
                    print('Password incorrent.')
                    valid = False

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
            ##### End Sign up #####


            # admin testing tool, returns all users
            if self.state == 'test':
                print('*************************************************')
                print("**************** Fetching users *****************")
                print('*************************************************')
                print(returnAllUsers())
                self.nextStateOpt()
                continue


            # case when user logins into the dashboard
            if self.state == 'dash':
                print('*************************************************')
                print("****************** Dashbaord ********************")
                print('*************************************************')
                print("What do you want to do?")
                print("1. Add group")
                print("2. Quit from a group")
                print("3. See group info")
                print("4. View group invitations")
                print("test - admin tool")
                self.nextStateOpt()
                continue

            # view invitations
            if self.state == 'invites':
                print('*************************************************')
                print("***************** Invitations *******************")
                print('*************************************************')
                res = invitations(self.user.credentials.get('email'))
                if res:
                    print(res)
                    self.nextStateOpt()
                    continue
                else:
                    print('You have no pending invitations.')
                    self.nextStateOpt()
                    continue

            ### End invites


            # See groups I'm in
            if self.state == 'groups':
                print('*************************************************')
                print("************ Groups that you're in **************")
                print('*************************************************')

                res = groupList(self.user.credentials.get('userid'))
                print(res)

                self.nextStateOpt()
                continue



            ##################################################################
            ########################## Under Dev #############################
            ##################################################################

            # TODOs:
            # Split bill between groups
            # 

            # Leave a group, require safty check on whether I have
            # unsettled balance in that group
            if self.state == 'leave-group':
                print('************* Under Development *****************')
                print("***************** Leave Group *******************")
                print('*************************************************')

                groupInfo = groupList(self.user.credentials.get('userid'))
                print(groupInfo)
                groupToLeave = input('Which group would you like to leave?\n')
                leaveGroup(self.user.credentials.get('userid'), groupToLeave)

                self.nextStateOpt()
                continue

            # Add a person to group directly, requires privilege
            if self.state == 'add-to-group':
                print('************* Under Development *****************')
                print("************ Add Person To Group ****************")
                print('*************************************************')


                toAdd = input('Whom to add?\n')
                groupNo = input('Which Group?\n')
                addToGroup(toAdd, groupNo)
                self.nextStateOpt()
                continue

            if self.state == 'delete-invite':
                print('************* Under Development *****************')
                print("*************** Delete invite *******************")
                print('*************************************************')
                invitationsToDelete = invitations(self.user.credentials.get('email'))
                print('groups that you are in:')
                print(invitationsToDelete)
                inviteToDelete = input('Which invitation would you like to delete?\n')
                print(inviteToDelete)
                deleteInvitation(self.user.credentials.get('userid'))
                self.nextStateOpt()
                continue

            # if self.state == 'move-person-to-another-group':

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
