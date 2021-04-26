CREATE DATABASE `hostel_db` ;


-- hostel_db.Hostel definition

CREATE TABLE hostel_db.`Hostel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone_no` int DEFAULT NULL,
  `total_rooms` int DEFAULT NULL,
  `total_users` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- hostel_db.Invoice definition

CREATE TABLE hostel_db.`Invoice` (
  `invoice_no` int NOT NULL AUTO_INCREMENT,
  `due_amount` int NOT NULL,
  `paid_amount` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `room_package_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`invoice_no`),
  KEY `Invoice_FK` (`room_package_id`),
  KEY `Invoice_FK_1` (`user_id`),
  CONSTRAINT `Invoice_FK` FOREIGN KEY (`room_package_id`) REFERENCES `Room_Package` (`id`),
  CONSTRAINT `Invoice_FK_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- hostel_db.Package definition

CREATE TABLE hostel_db.`Package` (
  `id` int NOT NULL AUTO_INCREMENT,
  `price` int NOT NULL DEFAULT 1000,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- hostel_db.Room definition

-- CREATE TABLE hostel_db.`Room` (
--   `price` int NOT NULL,
--   `room_no` int NOT NULL AUTO_INCREMENT,
--   `capacity` int NOT NULL DEFAULT 1,
--   `floor_no` int DEFAULT NULL,
--   `hostel_id` int NOT NULL,
--   PRIMARY KEY (`room_no`),
--   KEY `Room_FK` (`hostel_id`),
--   CONSTRAINT `Room_FK` FOREIGN KEY (`hostel_id`) REFERENCES `Hostel` (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE hostel_db.`Room` (
  `price` int NOT NULL,
  `room_no` int NOT NULL AUTO_INCREMENT,
  `capacity` int NOT NULL DEFAULT '1',
  `floor_no` int DEFAULT NULL,
  `hostel_id` int NOT NULL,
  `reserve` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`room_no`),
  KEY `Room_FK` (`hostel_id`),
  CONSTRAINT `Room_FK` FOREIGN KEY (`hostel_id`) REFERENCES `Hostel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- ALTER Table hostel_db.Room ADD reserve BOOL DEFAULT 0 NULL;
-- hostel_db.Room_Package definition

CREATE TABLE hostel_db.`Room_Package` (
  `charges` int NOT NULL DEFAULT 2000,
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL,
  `package_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Room_Package_FK` (`room_id`),
  KEY `Room_Package_FK_1` (`package_id`),
  CONSTRAINT `Room_Package_FK` FOREIGN KEY (`room_id`) REFERENCES `Room` (`room_no`),
  CONSTRAINT `Room_Package_FK_1` FOREIGN KEY (`package_id`) REFERENCES `Package` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- hostel_db.`User` definition

CREATE TABLE hostel_db.`User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `cnic` varchar(100) DEFAULT NULL,
  `contact_no` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

