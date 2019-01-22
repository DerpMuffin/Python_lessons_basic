CREATE TABLE `weather` (
	`city_id`	INTEGER NOT NULL,
	`city`	VARCHAR(255) NOT NULL,
	`date`	DATE NOT NULL,
	`temperature`	INTEGER NOT NULL,
	`weather_id`	INTEGER NOT NULL,
	`weather_icon`  VARCHAR(4) NOT NULL,
	PRIMARY KEY(`city_id`)
);