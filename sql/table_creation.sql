DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE IF NOT EXISTS groups (
	group_id smallserial NOT NULL,
	group_ch varchar(1) NOT NULL,
	enrollment smallint NOT NULL,
	group_num smallint NOT NULL,
	PRIMARY KEY (group_id)
);	

DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE IF NOT EXISTS students (
	student_id smallserial NOT NULL,
	last_name varchar(20) NOT NULL,
	first_name varchar(20) NOT NULL,
	patrononymic varchar(20) NULL,
	group_id smallint NOT NULL,
	PRIMARY KEY (student_id),
	
	FOREIGN KEY (group_id) 
	REFERENCES Groups (group_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS teachers CASCADE;
CREATE TABLE IF NOT EXISTS teachers (
	teacher_id smallserial NOT NULL,
	last_name varchar(20) NOT NULL,
	first_name varchar(20) NOT NULL,
	patrononymic varchar(20) NULL,
	classroom varchar(10) NOT NULL,
	PRIMARY KEY (teacher_id)
);

DROP TABLE IF EXISTS schedule CASCADE;
CREATE TABLE IF NOT EXISTS schedule (
	schedule_id serial NOT NULL,
	subject_id varchar(20) NOT NULL,
	group_id smallint NOT NULL,
	teacher_id smallint NOT NULL,
	day varchar(15) NOT NULL,
	time time NOT NULL,
	classroom varchar(10) NOT NULL,
	PRIMARY KEY (schedule_id),
	
	FOREIGN KEY (group_id) 
	REFERENCES Groups (group_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE,
	
	FOREIGN KEY (teacher_id) 
	REFERENCES Teachers (teacher_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS marks CASCADE;
CREATE TABLE IF NOT EXISTS marks (
	mark_id serial NOT NULL,
	student_id smallint NOT NULL,
	subject_id varchar(20) NOT NULL,
	teacher_id smallint NOT NULL,
	date date NOT NULL,
	mark smallint NOT NULL,
	PRIMARY KEY (mark_id),
	
	FOREIGN KEY (student_id) REFERENCES Students (student_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE,
	
	FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS homework CASCADE;
CREATE TABLE IF NOT EXISTS homework (
	task_id serial NOT NULL,
	teacher_id smallint NOT NULL,
	subject_id varchar(20) NOT NULL,
	group_id smallint NOT NULL,
	date date NOT NULL,
	info text NOT NULL,
	PRIMARY KEY (task_id),
	
	FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE,
	
	FOREIGN KEY (group_id) REFERENCES Groups (group_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS achievements CASCADE;
CREATE TABLE IF NOT EXISTS achievements (
	achievement_id serial NOT NULL,
	student_id smallint NOT NULL,
	name varchar(255) NOT NULL,
	place integer NULL,
	PRIMARY KEY (achievement_id),
	
	FOREIGN KEY (student_id) 
	REFERENCES Students (student_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS faults CASCADE;
CREATE TABLE IF NOT EXISTS faults (
	fault_id serial NOT NULL,
	teacher_id smallint NOT NULL,
	student_id smallint NOT NULL ,
	info text NOT NULL,
	PRIMARY KEY (fault_id),
	
	FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE,
	
	FOREIGN KEY (student_id) 
	REFERENCES Students (student_id)
	ON UPDATE RESTRICT
	ON DELETE CASCADE
);