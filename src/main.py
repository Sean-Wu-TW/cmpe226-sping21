from sqls import *
import readline
import time

## Tab completer
def completer(text, state):
    commands = ['login', 'sign-up', 'add-to-group', 'dash', 'test', 'invites', 'exit',
    'viewGroup', 'help', 'leaveGroup', 'info', 'friendList', 
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



class UserInfo():

    def __init__(self, email='s@gmail.com', name='s', password='', userid='66'):

        self.credentials = {
            'email': email,
            'name': name,
            'userid': userid
        }
    def userBuilder(self, key, value):
        ''' Builds the user info '''
        self.credentials[key] = value
        return self

    def info(self):
        print(self.credentials)
        # output groups that your are currently in


class EZLedger():
    
    '''states: login, sign-up, test, dash, invites, dash, info, groups'''

    def __init__(self):
        self.loggedIn = False
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
            'leaveGroup':'leaveGroup',
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

    def checkUserExists(self, userid):
        # Check if user exists
        allUsers = returnAllUsers()
        if not userid:
            print('WARNING: User missing.')
            return False
        if int(userid) not in [int(a[3]) for a in allUsers]:
            print('WARNING: User not exist.')
            return False
        else:
            return True

    def checkGroupExists(self, groupid):
        # Check if user exists
        allGroups = returnAllGroups()
        if not groupid:
            print('WARNING: Groupid missing.')
            return False
        if int(groupid) not in [int(a[0]) for a in allGroups]:
            print('WARNING: Group not exist.')
            return False
        else:
            return True

    def stateChanger(self, x):
        nextState = self.stateLookup.get(x)
        if nextState == 'exit':
            self.loggedIn = False
            self.prevState == 'welcome'
        if nextState:
            self.prevState = self.state
            self.state = nextState
        else:
            print('Oops! That is invalid!')
            time.sleep(1)
            if self.loggedIn:
                self.prevState = self.state
                self.state = 'info'


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
                print("************** Welcome to EZLedger **************")
                print('*************************************************')
                x = input('login or sign-up?\n')
                self.stateChanger(x)
                continue

            # Login
            if self.state == 'login':
                email = input('Please log in (email):')
                passw = input('Please log in (password):')
                if not email and not passw:
                    self.loggedIn = True
                    print('logged in as default user')
                    print()
                    self.user = UserInfo()
                    self.state = 'info'
                    continue
                if userLogin(email, passw):
                    self.loggedIn = True
                    me = userLogin(email, passw)[0]
                    self.user = UserInfo(*me)
                    self.state = 'info'
                else:
                    print('Log in failed.')
                    self.state = 'welcome'
                    continue



            # This is what the user logs in sees, his/her debts
            if self.state == 'info':
                print('*************************************************')
                print("****** Displaying your account information ******")
                print('*************************************************')
                print(self.user.info())
                res = friendList(self.user.credentials.get('userid'))
                print('*************** Your Friends: **************\n')
                for x in res:
                    print('userid: {}, name: {}, debt: {}'.format(x[0], x[1], x[2]))
                groups = groupList(self.user.credentials.get('userid'))
                print('*************** Your Groups: ***************\n')
                for y in groups:
                    print('groupid: {}, group name: {}'.format(y[0], y[2]))
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
                    print('Passwords does not match.')
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
                    print('Sign up failed')
                    self.state = 'welcome'
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
                    for x in res:
                        print('From group: {}'.format(x[0]))
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
                for x in res:
                    print('Group id: {}, Group name: {}'.format(x[0], x[2]))

                self.nextStateOpt()
                continue

            if self.state == 'friendList':

                print('*************************************************')
                print("***************** friendList ********************")
                print('*************************************************')
                res = friendList(self.user.credentials.get('userid'))
                for x in res:
                    print('Friend id: {}, Name: {}, Debt: {}'.format(x[0], x[1], x[2]))
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
                print('Your groups:\n')
                for x in res:
                    print('Group id: {}, Group name: {}'.format(x[0], x[2]))
                if res:
                    groupToDisplay = input('Which group would you like to view?\n')


                    if not self.checkGroupExists(groupToDisplay):
                        self.nextStateOpt()
                        continue
                    activity = groupActivity(groupToDisplay)
                    print("group_id, group name, expense_id, user_id, name, cost, time")
                    for row in activity:
                        print(row[0], row[1], row[2], row[5], row[6], row[7])
                else:
                    print('You are not in any group.')
                self.nextStateOpt()
                continue

            if self.state == 'settleBalance':
                print('*************************************************')
                print("***************** settleBalance *****************")
                print('*************************************************')
                toSettle = input('Who do you want to settle balance(userid)?\n')

                if not self.checkUserExists(toSettle):
                    self.nextStateOpt()
                    continue

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
                toInvite = input('Enter the email of user to invite(Email Separated by space)\n')
                groupToInvite = input('Enter the group to invite(group_id)\n') 

                allUsers = returnAllUsers()
                if toInvite and toInvite not in [a[0] for a in allUsers]:
                    print([a[0] for a in allUsers])
                    print('WARNING: User not exist.')
                    self.nextStateOpt()
                    continue

                if groupToInvite and not self.checkGroupExists(groupToInvite):
                    continue

                # Perform add 
                if addInvite(toInvite.split(), groupToInvite):
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

                if not self.checkGroupExists(groupToAccept):
                    self.nextStateOpt()
                    continue

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

                if not self.checkGroupExists(groupToDecline):
                    self.nextStateOpt()
                    continue

                if declineInvite(groupToDecline, self.user.credentials.get('email')):
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


                payer = input('Who is paying the bill?(user_id)\n')
                debtor = input('Who is splitting the bill with you?(Separated by space, user_id)\n')
                amoutToSplit = input('How much is the bill?\n')
                groupToSplit = input('Which group is splitting the bill?(group_id)\n')
                billName = input('What is the name of the bill?\n')

                valid = True
                for user in debtor.split():
                    if not self.checkUserExists(user):
                        valid = False
                        break

                if not valid:
                    self.nextStateOpt()
                    continue


                if not self.checkGroupExists(groupToSplit):
                    self.nextStateOpt()
                    continue

                if payer and debtor and amoutToSplit and groupToSplit and billName and \
                 addExpense(payer, debtor.split(), amoutToSplit, groupToSplit, billName):
                    print('Expense added')
                else:
                    print('Failed to add expense')
                self.nextStateOpt()
                continue

            if self.state == 'friendDetail':
                print('*************************************************')
                print("***************** Friend Detail *****************")
                print('*************************************************') 

                friendToView = input('Which friend would you like to view?(user_id)\n')
                if not self.checkUserExists(friendToView):
                    self.nextStateOpt()
                    continue
                if friendToView:
                    detail = friendDetail(self.user.credentials.get('userid'), friendToView)
                    print(detail)
                self.nextStateOpt()
                continue


            # Leave a group, require safty check on whether I have
            # unsettled balance in that group
            if self.state == 'leaveGroup':
                print('*************************************************')
                print("***************** Leave Group *******************")
                print('*************************************************')

                groupInfo = groupList(self.user.credentials.get('userid'))
                for x in groupInfo:
                    print('Group id: {}, Group name: {}'.format(x[0], x[1]))
                res = returnDebts(self.user.credentials.get('userid'))
                print(res)

                groupToLeave = input('Which group would you like to leave?\n')

                if not self.checkGroupExists(groupToLeave):
                    self.nextStateOpt()
                    continue

                if any(True if str(x[2]) == str(groupToLeave) and int(x[3]) != 0 else False for x in res):
                    print('Cannot leave group, you have unsettled debts.')
                    self.nextStateOpt()
                    continue
                else:
                    leaveGroup(self.user.credentials.get('userid'), groupToLeave)
                    self.nextStateOpt()
                    continue



            ##################################################################
            ########################## Under Dev #############################
            ##################################################################

            # TODOs:
            # Split bill between groups
            # 

            # expense id look up?
            if self.state == 'activityDetail':
                print('*************************************************')
                print("**************** activityDetail *****************")
                print('*************************************************')

                expense = input('Which expense would you like to view?(expense_id)\n')

                res = activityDetail(expense)
                print('Your activity:\n')
                print("expense name: " + res['name'])
                print("paid by: " + res['paidBy'])
                print("total amount: " + str(res['totalAmount']))
                for user in res['detail']:
                    print("------" + user['owedBy'] + " owes " + str(user['amount']) + " to " + res['paidBy'])

                comments = getComment(expense)
                print("Comments:")
                for comment in comments:
                    print(comment[0] + ": " + comment[1])
                self.nextStateOpt()
                continue

            # Leave a group, require safty check on whether I have
            # unsettled balance in that group
            if self.state == 'leave-group':
                print('************* Under Development *****************')
                print("***************** Leave Group *******************")
                print('*************************************************')

                groupInfo = groupList(self.user.credentials.get('userid'))
                for group in groupInfo:
                    print("group name: " + group[2] + " | id: " + str(group[1]))
                groupToLeave = input('Which group would you like to leave? (enter group id)\n')
                leaveGroup(self.user.credentials.get('userid'), groupToLeave)




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
    app = EZLedger()
    app.run()
