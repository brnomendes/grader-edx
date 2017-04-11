CREATE DATABASE IF NOT EXISTS `grader`;
USE `grader`;

DROP TABLE IF EXISTS `Submissions`;

CREATE TABLE `Submissions` (
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`timestamp` TIMESTAMP NOT NULL,
	`student_id` VARCHAR(255) NOT NULL,
	`program` TEXT NOT NULL,
	`test` TEXT NOT NULL
);

DROP TABLE IF EXISTS `TestResults`;

CREATE TABLE `TestResults` (
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`submission_id` INT NOT NULL,
	`student_id_test` VARCHAR(255) NOT NULL,
	`tests` INT NOT NULL,
	`errors` INT NOT NULL,
	`failures` INT NOT NULL,
	`coverage` FLOAT NOT NULL,
	`time` FLOAT NOT NULL
);