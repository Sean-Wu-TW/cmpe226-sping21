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
    sql = "select email, name, password from user where email = '{}'".format(str(email))
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

