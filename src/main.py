from sqls import *
import readline

## Tab completer
def completer(text, state):
    commands = ['login', 'sign-up', 'add-to-group', 'dash', 'test', 'invites', 'exit',
    'viewGroup', 'help', 'leave-group', 'info', 'friendList', 
    'friendDetail','createGroup','groupActivity','activityDetail','settleBalance',
    'addInvite','acceptInvite','declineInvite','updateProfile','changePassword',
    'addExpense']

    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)


def cInput(text):
    res = input(text)


class UserInfo():

    def __init__(self, email='s@gmail.com', name='s', password='', userid='59'):
        self.credentials = {
            'email': email,
            'name': name,
            'userid': userid,
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
        self.prevState = 'welcome'
        self.help = ['login', 'sign-up', 'add-to-group', 'dash', 'test', 'invites', 'exit',
    'viewGroup', 'help', 'leave-group', 'info', 'friendList', 
    'friendDetail','createGroup','groupActivity','activityDetail','settleBalance',
    'addInvite','acceptInvite','declineInvite','updateProfile','changePassword',
    'addExpense']
        self.stateLookup = {
            'exit':'login', 
            'test': 'test',
            'login':'login',
            'sign-up':'sign-up',
            'invites':'invites',
            'dash':'dash',
            'info':'info',
            'viewGroup':'viewGroup',
            'leave-group':'leave-group',
            'friendDetail':'friendDetail',
            'logout':'welcome',        
            'friendList':'friendList',
            'createGroup':'createGroup',
            'groupActivity':'groupActivity',
            'activityDetail':'activityDetail', #
            'settleBalance':'settleBalance', 
            'addInvite':'addInvite', 
            'acceptInvite':'acceptInvite', 
            'declineInvite':'declineInvite', 
            'updateProfile':'updateProfile', 
            'changePassword':'changePassword',
            'addExpense':'addExpense' 
        }

    def stateChanger(self, x):
        nextState = self.stateLookup.get(x)
        if nextState:
            self.prevState = self.state
            self.state = nextState


    def nextStateOpt(self):
        print()
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
                    print()
                    self.user = UserInfo()
                    self.state = 'info'
                    continue
                if userLogin(email, passw):
                    me = userLogin(email, passw)[0]
                    self.user = UserInfo(*me)
                    self.state = 'info'


            # This is what the user logs in sees, his/her debts
            if self.state == 'info':
                print('*************************************************')
                print("****** Displaying your account information ******")
                print('*************************************************')
                print(self.user.info())
                res = friendList(self.user.credentials.get('userid'))
                print('*************** Your Friends: **************\n')
                print(res)
                groups = groupList(self.user.credentials.get('userid'))
                print('*************** Your Groups: ***************\n')
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
                #####################
                print("========= Your info: =========")
                print("email:", email)
                print('name:', name)
                print('password:', password)
                print('Processing your data...')
                #####################



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
                    insertNewUser(email, name, password)
                    self.stateChanger('login')
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
            if self.state == 'viewGroup':
                print('*************************************************')
                print("************ Groups that you're in **************")
                print('*************************************************')

                res = groupList(self.user.credentials.get('userid'))
                print(res)

                self.nextStateOpt()
                continue

            if self.state == 'friendList':
                print('*************************************************')
                print("***************** friendList ********************")
                print('*************************************************')
                res = friendList(self.user.credentials.get('userid'))
                print(res)
                self.nextStateOpt()
                continue

            if self.state == 'createGroup':
                print('*************************************************')
                print("***************** createGroup *******************")
                print('*************************************************')

                groupName = input('Please enter group name:\n')
                if groupName and createGroup(groupName, self.user.credentials.get('userid')):
                    print('Group created!')
                else:
                    print('Failed to create group')
                self.nextStateOpt()
                continue

            if self.state == 'groupActivity':
                print('*************************************************')
                print("**************** groupActivity ******************")
                print('*************************************************')
                res = groupList(self.user.credentials.get('userid'))
                print(res)
                if res:
                    groupToDisplay = input('Which group would you like to view?\n')
                    groupActivity(groupToDisplay)
                else:
                    print('You are not in any group.')
                self.nextStateOpt()
                continue

            if self.state == 'activityDetail':
                print('*************************************************')
                print("**************** activityDetail *****************")
                print('*************************************************')

                expense = input('Which expense would you like to view?\n')

                res = activityDetail(expense)
                print('Your activity:\n', res)
                self.nextStateOpt()
                continue

            if self.state == 'settleBalance':
                print('*************************************************')
                print("***************** settleBalance *****************")
                print('*************************************************')

                toSettle = input('Who do you want to settle balance?\n')

                if toSettle and settleBalance(self.user.credentials.get('userid'), toSettle):
                    print('Balanced settled!')
                else:
                    print('Settle failed.')

                self.nextStateOpt()
                continue

            if self.state == 'addInvite':
                print('*************************************************')
                print("******************* addInvite *******************")
                print('*************************************************')
                toInvite = input('Enter the email of user to invite(Separated by space)\n')
                groupToInvite = input('Enter the group to invite\n') 
                if toInvite and groupToInvite and addInvite(toInvite.split(), groupToInvite):
                    print('{} invited'.format(toInvite))
                else:
                    print('Invitation failed!')
                self.nextStateOpt()
                continue

            if self.state == 'acceptInvite':
                print('*************************************************')
                print("***************** acceptInvite ******************")
                print('*************************************************')

                groupToAccept = input('To which group do you agree to join?\n')

                if groupToAccept and acceptInvite(groupToAccept, self.user.credentials.get('email')):
                    print('Joined {}'.format(groupToAccept))
                else:
                    print('Join failed')
                self.nextStateOpt()
                continue

            if self.state == 'declineInvite':
                print('*************************************************')
                print("**************** declineInvite ******************")
                print('*************************************************')  

                groupToDecline = input('Which group invitation would you like to decline?\n')

                if groupToDecline and declineInvite(groupToDecline, self.user.credentials.get('email')):
                    print('Invitation to {} declined'.format(groupToDecline))
                else:
                    print('Failed to decline.')
                self.nextStateOpt()
                continue

            if self.state == 'updateProfile':
                print('*************************************************')
                print("*************** Update Profile ******************")
                print('*************************************************') 

                newName = input('Enter new name:\n')
                newEmail = input('Enter new email:\n')
                if newName and newEmail and updateProfile(self.user.credentials.get('userid'), {'name': newName, 'email': newEmail}):
                    print('Profile updated!')
                    self.user.credentials['name'] = newName
                    self.user.credentials['email'] = newEmail
                else:
                    print('Failed to update profile')
                self.nextStateOpt()
                continue

            if self.state == 'changePassword':
                print('*************************************************')
                print("*************** Change Password *****************")
                print('*************************************************') 

                oldPass = input('Please enter old password:\n')
                newPass = input('Please enter new password:\n')
                confirmNewPassword = input('Please confirm new password:\n')

                if oldPass and newPass  \
                and confirmNewPassword and changePassword(self.user.credentials.get('userid'), oldPass, newPass) \
                and oldPass == newPass:
                    print('Password updated!')
                else:
                    print('Failed to update password')
                self.nextStateOpt()
                continue

            if self.state == 'addExpense':
                print('*************************************************')
                print("****************** Add Expense ******************")
                print('*************************************************') 

                payer = input('Who is paying the bill?\n')
                debtor = input('Who is splitting the bill with you?(Separated by space)\n')
                amoutToSplit = input('How much is the bill?\n')
                groupToSplit = input('Which group is splitting the bill?\n')
                billName = input('What is the name of the bill?\n')
                if payer and debtor and amoutToSplit and groupToSplit and billName and \
                 addExpense(payer, debtor.split(), amoutToSplit, groupToSplit, billName):
                    print('Expense added')
                else:
                    print('Failed to add expense')
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



            else:
                print('Not Inplemented.')
                self.state = self.prevState
                continue
                



    def validate(self, string, kind):
        if kind == 'email':
            if '@' not in string:
                print('******please enter a valid email address******')
                return False

if __name__ == '__main__':
    app = Splitwise()
    app.run()
