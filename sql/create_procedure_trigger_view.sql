CREATE DEFINER=`admin`@`%` PROCEDURE `splitwise`.`AcceptInvite`(IN group_id INT, IN email varchar(255))
BEGIN
	DECLARE id INT DEFAULT 0;
	SELECT user_id FROM `user` u where u.email = email INTO id;
	INSERT INTO groups_users (group_id, user_id) VALUES (group_id, id);
	DELETE FROM group_invite gi where gi.group_id = group_id and gi.email = email;
END


CREATE DEFINER=`admin`@`%` PROCEDURE `splitwise`.`CreateGroup`(IN groupname varchar(255), IN user_id INT)
BEGIN
	DECLARE new_group_id INT DEFAULT 0;
	INSERT INTO `groups` (group_name) VALUES (groupname);
	SET new_group_id = LAST_INSERT_ID();
	INSERT INTO groups_users (group_id, user_id) VALUES (new_group_id, user_id);
END


CREATE DEFINER=`admin`@`%` PROCEDURE `splitwise`.`FindFriends`(IN userid INTEGER)
BEGIN
	SELECT u.user_id, u.name, d.bal from user u 
	right join (select user2, sum(balance) as bal from debt 
	where user1=userid group by user2) as d on u.user_id = d.user2;
END


CREATE DEFINER=`admin`@`%` PROCEDURE `splitwise`.`FriendDetail`(IN user1_id INT, IN user2_id INT)
BEGIN
	SELECT name, group_name, balance from debt d 
	join `groups` g on g.group_id = d.group_id
	join user u on d.user2 = u.user_id
	where user1=user1_id and user2=user2_id;
END


CREATE DEFINER=`admin`@`%` TRIGGER `after_user_join_group` BEFORE INSERT ON `groups_users` FOR EACH ROW BEGIN
	DECLARE done INT DEFAULT FALSE;
	DECLARE temp_id INTEGER;
	DECLARE cur CURSOR FOR SELECT user_id FROM groups_users WHERE group_id=NEW.group_id;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done := TRUE;

	OPEN cur;
		read_loop: LOOP
			FETCH cur INTO temp_id;
			IF done THEN
      			LEAVE read_loop;
    		END IF;

			INSERT INTO debt (user1, user2, group_id, balance) VALUES (NEW.user_id, temp_id, NEW.group_id, 0);
			INSERT INTO debt (user1, user2, group_id, balance) VALUES (temp_id, NEW.user_id, NEW.group_id, 0);
		END LOOP;
	CLOSE cur;

END


CREATE DEFINER=`admin`@`%` TRIGGER `user_leave_group` AFTER DELETE ON `groups_users` FOR EACH ROW BEGIN 	
DELETE FROM debt d WHERE d.user1=OLD.user_id and d.group_id=OLD.group_id; 	
DELETE FROM debt d WHERE d.user2=OLD.user_id and d.group_id=OLD.group_id; 
END


CREATE DEFINER=`admin`@`%` TRIGGER `after_expense_add` AFTER INSERT ON `sub_expense` FOR EACH ROW BEGIN
	DECLARE new_group_id INT;
	SELECT group_id from expense e2 where e2.expense_id = NEW.expense_id INTO new_group_id;
	update debt
	set balance = balance + NEW.amount
	where user1=NEW.user1 and user2=NEW.user2 and group_id = new_group_id;

	update debt
	set balance = balance - NEW.amount
	where user1=NEW.user2 and user2=NEW.user1 and group_id = new_group_id;

END


CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `splitwise`.`group_info` AS
select
    `g`.`group_id` AS `group_id`,
    `g`.`group_name` AS `group_name`,
    count(0) AS `user_count`
from
    (`splitwise`.`groups` `g`
join `splitwise`.`groups_users` `gu` on
    ((`gu`.`group_id` = `g`.`group_id`)))
group by
    `g`.`group_id`


CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `splitwise`.`user_info` AS
select
    `u`.`name` AS `name`,
    `u`.`email` AS `email`,
    `u`.`password` AS `password`,
    `u`.`user_id` AS `user_id`,
    count(0) AS `group_count`
from
    (`splitwise`.`user` `u`
join `splitwise`.`groups_users` `gu` on
    ((`gu`.`user_id` = `u`.`user_id`)))
group by
    `gu`.`group_id`