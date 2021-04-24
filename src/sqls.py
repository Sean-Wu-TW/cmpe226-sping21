hostname = 'database-1.c1sqwxkauabb.us-west-1.rds.amazonaws.com'
username = 'admin'
password = '19950808'
database = 'splitwise'

import mysql.connector

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



def insertNewUser(email, name, password, timezone=None, currency=None, lang=None, avatar=None):


    mycursor = mydb.cursor()

    sql = "INSERT INTO user (email, name, password, timezone, currency, lang, avatar) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (email, name, password, timezone, currency, lang, avatar)

    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")



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
    mydb = mysql.connector.connect(
      host=hostname,
      user=username,
      password=password,
      database=database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DISTINCT * FROM group_invite WHERE email = '{}'".format(str(whoami)))
    res = []
    for x in mycursor:
      res.append(x)
    return res


