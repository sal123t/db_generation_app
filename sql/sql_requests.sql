-- 1
SELECT * FROM groups, students, teachers, marks, homework, achievements, faults; -- Select all data from all tables

-- 2
SELECT * FROM students 
	WHERE (first_name IN ('Вячеслав', 'Елизавета', 'Игорь', 'Владислава', 'Роман', 'Иван')) 
		AND (group_id BETWEEN 5 AND 20) 
		AND (patrononymic LIKE '%ов%');
--
SELECT * FROM homework 
	WHERE (subject_id IN ('Математика', 'Естествознание', 'Химия')) 
		AND (group_id BETWEEN 5 AND 20) 
		AND (info LIKE 'Стр. _5%');
--
SELECT * FROM faults 
	WHERE (teacher_id IN ('1', '3', '7', '15', '35', '36', '40', '41', '42')) 
		AND (student_id BETWEEN 22 AND 300) 
		AND (info LIKE '%е%'); 

-- 3
SELECT SUM(mark) / COUNT(*) AS average FROM marks WHERE subject_id = 'Математика';

-- 4
SELECT * FROM teachers ORDER BY last_name, first_name, patrononymic;

-- 5
SELECT AVG(mark) AS average, COUNT(*) AS tasks FROM marks, homework WHERE marks.subject_id = 'Математика' AND homework.subject_id = 'Математика';

-- 6
SELECT last_name, first_name, patrononymic, info 
	FROM students 
	RIGHT OUTER JOIN faults 
		ON students.student_id = faults.student_id
	ORDER BY last_name, first_name, patrononymic;
--
SELECT last_name, first_name, patrononymic, subject_id, group_id, info, date 
	FROM teachers 
	LEFT OUTER JOIN homework 
		ON teachers.teacher_id = homework.teacher_id
	ORDER BY last_name, first_name, patrononymic;

-- 7
SELECT name, COUNT(*) AS cnt FROM achievements GROUP BY name HAVING COUNT(*) > 30 ORDER BY cnt;

-- 8
SELECT mark FROM marks
	WHERE student_id = (SELECT COUNT(*) FROM students WHERE group_id = 2);
	
-- 9
INSERT INTO groups (group_ch, enrollment, group_num) VALUES ('а', '2009', '11');
--
INSERT INTO students (last_name, first_name, patrononymic, group_id) VALUES ('Зарецкая', 'Елизавета', 'Сергеевна', 1);
--
INSERT INTO teachers (last_name, first_name, patrononymic, classroom) VALUES ('Осетрин', 'Александр', 'Сергеевич', 228);
--
INSERT INTO marks (student_id, subject_id, teacher_id, date, mark) VALUES (25, 'Математика', 2, '2020-05-06', 5);
--
INSERT INTO homework (teacher_id, subject_id, group_id, info, date) VALUES (23, 'Естествознание', 5, 'Выполнение стандартных sql запросов.', '2020-05-06');
--
INSERT INTO achievements (student_id, name, place) VALUES (2, 'ГТО', 1);
--
INSERT INTO faults (teacher_id, student_id, info) VALUES (31, 300, 'Кинул тряпкой в одноклассницу!');

-- 10
UPDATE marks SET mark = 4 WHERE mark = 2;

-- 11
DELETE FROM marks WHERE mark > (SELECT MIN(mark) FROM marks);

-- 12
DELETE FROM students WHERE student_id NOT IN (SELECT student_id FROM achievements);
