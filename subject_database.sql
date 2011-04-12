CREATE TABLE email (
	id INTEGER NOT NULL, 
	address VARCHAR(128), 
	subject_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject_id) REFERENCES subject (id)
);
CREATE TABLE phone (
	id INTEGER NOT NULL, 
	number VARCHAR(24), 
	subject_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject_id) REFERENCES subject (id)
);
CREATE TABLE subject (
	id INTEGER NOT NULL, 
	entrydate DATE, 
	lastname VARCHAR(64), 
	firstname VARCHAR(64), 
	age INTEGER, 
	sex VARCHAR(6), 
	ethnicity VARCHAR(22), 
	amerind BOOLEAN, 
	afram BOOLEAN, 
	pacif BOOLEAN, 
	asian BOOLEAN, 
	white BOOLEAN, 
	unknown BOOLEAN, 
	other_race VARCHAR(32), 
	ur_student BOOLEAN, 
	gradyear INTEGER, 
	hearing_normal BOOLEAN, 
	hearing_problems TEXT, 
	vision_normal VARCHAR(38), 
	vision_other TEXT, 
	more_expts BOOLEAN, 
	PRIMARY KEY (id), 
	CHECK (more_expts IN (0, 1)), 
	CHECK (sex IN ('Male', 'Female')), 
	CONSTRAINT name_constraint UNIQUE (firstname, lastname), 
	CHECK (amerind IN (0, 1)), 
	CHECK (asian IN (0, 1)), 
	CHECK (ur_student IN (0, 1)), 
	CHECK (unknown IN (0, 1)), 
	CHECK (afram IN (0, 1)), 
	CHECK (vision_normal IN ('Normal uncorrected', 'Corrected-to-normal with glasses', 'Corrected-to-normal with soft contacts', 'Corrected-to-normal with hard contacts', 'Other')), 
	CHECK (white IN (0, 1)), 
	CHECK (ethnicity IN ('Hispanic or Latino', 'Not Hispanic or Latino')), 
	CHECK (hearing_normal IN (0, 1)), 
	CHECK (pacif IN (0, 1))
);