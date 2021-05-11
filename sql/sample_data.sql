-- # SJSU CMPE 226 Spring 2021 TEAM4
-- 5 sample user
INSERT INTO `user` (email, name, password) VALUES ("1@sample.com", "sample 1", "12345")
SET @user1_id = LAST_INSERT_ID() 

INSERT INTO `user` (email, name, password) VALUES ("2@sample.com", "sample 2", "12345")
SET @user2_id = LAST_INSERT_ID() 

INSERT INTO `user` (email, name, password) VALUES ("3@sample.com", "sample 3", "12345")
SET @user3_id = LAST_INSERT_ID()  

INSERT INTO `user` (email, name, password) VALUES ("4@sample.com", "sample 4", "12345")
SET @user4_id = LAST_INSERT_ID() 

INSERT INTO `user` (email, name, password) VALUES ("5@sample.com", "sample 5", "12345")
SET @user5_id = LAST_INSERT_ID() 

-- 2 sample group
INSERT INTO `groups` (group_name) VALUES ("sample group 1")
SET @group1_id = LAST_INSERT_ID() 

INSERT INTO `groups` (group_name) VALUES ("sample group 2")
SET @group2_id = LAST_INSERT_ID() 



INSERT INTO groups_users (group_id, user_id) VALUES (@group1_id, @user1_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group1_id, @user2_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group1_id, @user3_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group1_id, @user4_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group1_id, @user5_id)

INSERT INTO groups_users (group_id, user_id) VALUES (@group2_id, @user1_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group2_id, @user2_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group2_id, @user3_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group2_id, @user4_id)
INSERT INTO groups_users (group_id, user_id) VALUES (@group2_id, @user5_id)

INSERT INTO expense (user_id, group_id, name, cost) VALUES (@user1_id, @group1_id, "expense 1 group 1", 50)
SET @expense11_id = LAST_INSERT_ID()
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense11_id, @user1_id, @user2_id, 25)


INSERT INTO expense (user_id, group_id, name, cost) VALUES (@user2_id, @group1_id, "expense 2 group 1", 100)
SET @expense21_id = LAST_INSERT_ID()
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense21_id, @user2_id, @user1_id, 25)
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense21_id, @user2_id, @user3_id, 25)
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense21_id, @user2_id, @user4_id, 25)


INSERT INTO expense (user_id, group_id, name, cost) VALUES (@user1_id, @group2_id, "expense 1 group 2", 160)
SET @expense12_id = LAST_INSERT_ID()
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense12_id, @user1_id, @user2_id, 40)
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense12_id, @user1_id, @user3_id, 40)
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense12_id, @user1_id, @user4_id, 40)


INSERT INTO expense (user_id, group_id, name, cost) VALUES (@user2_id, @group2_id, "expense 2 group 2", 300)
SET @expense22_id = LAST_INSERT_ID()
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense22_id, @user2_id, @user3_id, 100)
INSERT INTO sub_expense (expense_id, user1, user2, amount) VALUES(@expense22_id, @user2_id, @user4_id, 100)



