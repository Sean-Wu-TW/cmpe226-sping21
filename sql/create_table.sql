-- # SJSU CMPE 226 Spring 2021 TEAM4
CREATE TABLE `user` (
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`email`),
  UNIQUE KEY `user_id` (`user_id`)
)

CREATE TABLE `groups` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) DEFAULT NULL,
  UNIQUE KEY `group_id` (`group_id`),
  UNIQUE KEY `group_name` (`group_name`)
)

CREATE TABLE `sub_expense` (
  `expense_id` int NOT NULL,
  `user1` int NOT NULL,
  `user2` int NOT NULL,
  `amount` double DEFAULT NULL,
  PRIMARY KEY (`expense_id`,`user1`,`user2`),
  KEY `user1` (`user1`),
  KEY `user2` (`user2`),
  CONSTRAINT `sub_expense_ibfk_1` FOREIGN KEY (`expense_id`) REFERENCES `expense` (`expense_id`),
  CONSTRAINT `sub_expense_ibfk_2` FOREIGN KEY (`user1`) REFERENCES `user` (`user_id`),
  CONSTRAINT `sub_expense_ibfk_3` FOREIGN KEY (`user2`) REFERENCES `user` (`user_id`)
)

CREATE TABLE `groups_users` (
  `group_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `groups_users_FK` (`group_id`),
  CONSTRAINT `groups_users_FK` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `groups_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
)



CREATE TABLE `group_invite` (
  `group_id` int NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  KEY `group_id` (`group_id`),
  KEY `email` (`email`),
  CONSTRAINT `group_invite_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `group_invite_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `group_invite_ibfk_4` FOREIGN KEY (`email`) REFERENCES `user` (`email`)
)

CREATE TABLE `expense` (
  `expense_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `cost` double DEFAULT NULL,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`expense_id`),
  KEY `user_id` (`user_id`),
  KEY `expense_FK` (`group_id`),
  CONSTRAINT `expense_FK` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `expense_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
)

CREATE TABLE `debt` (
  `user1` int NOT NULL,
  `user2` int NOT NULL,
  `group_id` int NOT NULL,
  `balance` double DEFAULT NULL,
  PRIMARY KEY (`user1`,`user2`,`group_id`),
  CONSTRAINT `debt_CHECK` CHECK ((`user1` <> `user2`))
)

CREATE TABLE `comment` (
  `expense_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `expense_id` (`expense_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`expense_id`) REFERENCES `expense` (`expense_id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
)