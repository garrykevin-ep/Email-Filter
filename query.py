TABLE_SCHEMA = '''CREATE TABLE IF NOT EXISTS `Email` (
		`id`	TEXT UNIQUE,
		`subject`	TEXT,
		`date`	TEXT,
		`time`	TEXT,
		`body`	TEXT,
		PRIMARY KEY(`id`)
	);

	CREATE TABLE IF NOT EXISTS `Label` (
		`id`	TEXT,
		`name`	TEXT,
		PRIMARY KEY(`id`)
	);

	CREATE TABLE IF NOT EXISTS `Email_Label` (
	`email_id`	TEXT,
	`label_id`	TEXT,
	PRIMARY KEY(`email_id`,`label_id`),
	FOREIGN KEY(`email_id`) REFERENCES `Email`(`id`) ON DELETE CASCADE,
	FOREIGN KEY(`label_id`) REFERENCES `Label`(`id`) ON DELETE CASCADE
	);
	
	'''

EMAIL_INSERT = 'INSERT INTO Email (id,subject,date,time,body) VALUES ("{}","{}","{}","{}","{}")'
EMAIL_BULK_INSERT = 'INSERT OR REPLACE INTO Email (id,subject,date,time,body) VALUES (?,?,?,?,?)'
LABEL_INSERT = 'INSERT OR REPLACE INTO Label VALUES (?,?)'
EMAIL_LABEL_INSERT = 'INSERT OR REPLACE INTO Email_Label VALUES("{}",?)'