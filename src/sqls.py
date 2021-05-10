import bcrypt
import hashlib
import mysql.connector
hostname = 'database-1.c1sqwxkauabb.us-west-1.rds.amazonaws.com'
username = 'admin'
password = '19950808'
database = 'splitwise'


mydb = mysql.connector.connect(
    host=hostname,
    user=username,
    password=password,
    database=database
)

# mycursor = mydb.cursor()


# mycursor.execute("INSERT INTO `splitwise`.`user` (`email`, `name`) VALUES ('user50@user.com', 'user500');")

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")

# for x in mycursor:
#   print(x)


def insertNewUser(email, name, password):
    ''' For sign-up purposes '''

    mycursor = mydb.cursor()

    # encodedPassword = hashlib.sha256(password.encode())

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)
    sql = "INSERT INTO user (email, name, password) VALUES (%s, %s, %s)"
    val = (email, name, hashedPassword)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


def userLogin(email, password):
    sql = "select email, name, password from user where email = '{}'".format(
        str(email))
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    res = []
    for x in mycursor:
        res.append(x)
    hashed_password = res[0][2].encode('utf8')

    # if the password is correct, return the user information. Otherwise, return empty list
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return res
    else:
        return []


def returnAllUsers():
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user")
    res = []
    for x in mycursor:
        res.append(x)
    return res


def invitations(whoami):
    ''' View active invitations from the invite table '''
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT DISTINCT * FROM group_invite WHERE email = '{}'".format(str(whoami)))
    res = []
    for x in mycursor:
        res.append(x)
    return res


def returnDebts(whoami):
    ''' Returns the debts that are invloved with me '''
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT DISTINCT * FROM debt WHERE user1 = '{}'".format(str(whoami)))
    res = []
    for x in mycursor:
        res.append(x)
    return res


def groupList(whoami):
    ''' This function returns the groups that I am currently in '''
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()

    # For some reason 'groups' is a reserved word in mysql..., so have to use backtick ` to avoid it
    mycursor.execute(
        "SELECT DISTINCT * FROM groups_users NATURAL JOIN `groups` WHERE user_id = '{}'".format(str(whoami)))
    res = []
    for x in mycursor:
        res.append(x)
    return res


def leaveGroup(whoami, groupNo):
    try:
        mydb = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM groups_users WHERE user_id = '{}' and group_id = '{}'".format(
            str(whoami), str(groupNo)))

    except:
        print('Something went wrong in leaveGroup')
    finally:
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        return


def addToGroup(whomToAdd, groupNo):
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO groups_users (group_id, user_id) VALUES (%s, %s)"
    val = (groupNo, whomToAdd)

    mycursor.execute(sql, val)

    mydb.commit()
    print(mycursor.rowcount, "record(s) added")
    return


# display all the friends and debt
def friendList(whoami):
    sql = "CALL FindFriends({})".format(whoami)

    mycursor = mydb.cursor()
    mycursor.execute(sql)
    res = []
    for x in mycursor:
        res.append(x)

    return res


# display detail for a certain friend, like how much is owed in which group
def friendDetail(whoami, friend_id):
    sql = "CALL FriendDetail({}, {})".format(whoami, friend_id)

    mycursor = mydb.cursor()
    mycursor.execute(sql)
    res = []
    for x in mycursor:
        res.append(x)

    return res


# Create group will create a group and add the user created it to the group
def createGroup(group_name, user_id):
    sql = "CALL CreateGroup(\"{}\", {});".format(group_name, user_id)

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


# This should return all the activity inside this group
def groupActivity(group_id):
    sql = "select * from `groups` g join expense e on g.group_id = e.group_id where g.group_id = {} ORDER BY e.`time` DESC ".format(
        group_id)

    mycursor = mydb.cursor()
    mycursor.execute(sql)
    res = []
    for x in mycursor:
        res.append(x)

    return res

# sample response:
# {'detail': [{'owedBy': 'user1', 'amount': 10.0}, {'owedBy': 'user2', 'amount': 10.0}, {'owedBy': 'user3', 'amount': 10.0}], 'name': 'test4', 'paidBy': 'charles', 'totalAmount': 40.0}
# detail is how much each user owes the user paid this expense. other is detail of this expense


def activityDetail(expense_id):
    sql = "SELECT u1.name as paid_username, e.name, e.cost as total_amount, u2.name as owe_username, se.amount FROM sub_expense se JOIN expense e on se.expense_id=e.expense_id JOIN user u1 on e.user_id = u1.user_id JOIN user u2 on se.user2 = u2.user_id WHERE e.expense_id={}".format(
        expense_id)

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    res = {}

    res['detail'] = []
    for x in mycursor:
        res['name'] = x[1]
        res['paidBy'] = x[0]
        res['totalAmount'] = x[2]
        res['detail'].append({'owedBy': x[3], 'amount': x[4]})

    return res


def settleBalance(user1, user2):
    sql = "UPDATE debt set balance = 0 where user1={} AND user2={} OR user1={} AND user2={}".format(
        user1, user2, user2, user1)

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    mydb.commit()

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


# add invite, user_list is a list of user email that the user has invited to the group
# sample usage: addInvite(user_list=["1@user.com", "2@user.com"], group_id=51)
# if false, abort all add invite query.
def addInvite(user_list, group_id):
    val = []
    for user in user_list:
        val.append((group_id, user))

    sql = "INSERT INTO group_invite (group_id, email) VALUES (%s, %s)"

    mycursor = mydb.cursor()
    mycursor.executemany(sql, val)

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


# accept invite, need user's email and the group_id user invited to
def acceptInvite(group_id, email):
    sql = "CALL AcceptInvite({}, \"{}\")".format(group_id, str(email))

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


# decline invite, just delete that invite
def declineInvite(group_id, email):
    sql = "DELETE FROM group_invite WHERE group_id = {} and email = \'{}\'".format(
        group_id, email)

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


def updateProfile(user_id, new_profile):
    sql = "UPDATE user SET name = '{}', email = '{}' WHERE user_id={}".format(
        new_profile['name'], new_profile['email'], user_id)

    mycursor = mydb.cursor()
    mycursor.executemany(sql, val)

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


def changePassword(user_id, orig_password, new_password):
    sql = "select email, name, password from user where user_id = '{}'".format(
        user_id)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    res = []
    for x in mycursor:
        res.append(x)
    hashed_password = res[0][2].encode('utf8')

    # if the password is correct, hash the new password and store it
    if bcrypt.checkpw(orig_password.encode('utf8'), hashed_password):
        print("orig confirmed")

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(new_password.encode(), salt)
        new_sql = "UPDATE user SET password = '{}' WHERE user_id={}".format(
            hashedPassword.decode('utf-8'), user_id)
        print(new_sql)
        mycursor.execute(new_sql)

        if mycursor.rowcount > 0:
            mydb.commit()
            return True
        else:
            return False
    else:
        return False


def addExpense(paid_by, user_list, amount, group_id, name):
    sql = "INSERT INTO expense(user_id, group_id, `name`, cost) VALUES (%s, %s, %s, %s)"
    val = (paid_by, group_id, name, amount)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)

    if mycursor.rowcount > 0:
        mydb.commit()

    expense_id = mycursor.lastrowid

    avg_amount = amount / len(user_list)
    for user in user_list:
        if user != paid_by:
            sql = "INSERT INTO sub_expense(expense_id, user1, user2, amount) VALUES (%s, %s, %s, %s)"
            val = (expense_id, paid_by, user, avg_amount)
            mycursor.execute(sql, val)

    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False


def addComment(expense_id, user_id, content):
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO comment(expense_id, user_id, content) VALUES(%s, %s, %s)"
    val = (expense_id, user_id, content)
    mycursor.execute(sql, val)
    if mycursor.rowcount > 0:
        mydb.commit()
        return True
    else:
        return False

def getComment(expense_id):
    mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()

    sql = "SELECT u.name, c.content, time FROM comment c JOIN user u on c.user_id=u.user_id WHERE expense_id={}".format(expense_id)
    mycursor.execute(sql)
    
    res = []
    for x in mycursor:
        res.append(x)

    return res
