# -*- coding: utf-8 -*-
# Orshak Ivan, 24.04.2020

import random
import psycopg2
import datetime
import os
import hashlib
from getpass import getpass


class User:
    """Front line class, working with users data."""

    # Constructor.
    def __init__(self):
        self.db_name = None
        self.username = None
        self.password = None
        self.host = None
        self.auth = 0
        self.db = None

    # Destructor.
    def __del__(self):
        del self.db

    # Connection to database.
    def connect(self):
        self.get_login()
        self.db = Db(self.db_name, self.username, self.password, self.host)

        if self.db.connected == 1:
            self.auth = 1

    # Disconnection from database.
    def disconnect(self):
        del self.db
        self.__init__()

    # Getting user credentials.
    def get_login(self):
        self.db_name = input("DB name:")
        self.username = input("Username:")
        self.password = getpass('Password: ')
        self.host = input("Host IP:")


class GetData:
    """Getting data from data.dat."""

    # Constructor.
    def __init__(self):
        try:
            self.file = open("data\\data.dat", 'r', encoding='utf-8')
        except FileNotFoundError:
            print(Db.report_handler[18])
        else:
            self.data_file = self.file.readlines()

    # Destructor.
    def __del__(self):
        self.file.close()

    # Comparing hashes from system file and vars given.
    def chk_data(self, db_name, user_name, pswd, host_addr):
        db_name = db_name.encode("utf-8")
        user_name = user_name.encode("utf-8")
        pswd = pswd.encode("utf-8")
        host_addr = host_addr.encode("utf-8")

        if hashlib.md5(db_name).hexdigest() == self.data_file[0].rstrip('\n'):
            if hashlib.md5(user_name).hexdigest() == self.data_file[1].rstrip('\n'):
                if hashlib.md5(pswd).hexdigest() == self.data_file[2].rstrip('\n'):
                    if hashlib.md5(host_addr).hexdigest() == self.data_file[3].rstrip('\n'):
                        return 0
                    else:
                        return 4
                else:
                    return 3
            else:
                return 2
        else:
            return 1


class Logging:
    """Database change logging module."""

    # Constructor.
    # Creating a file every new connection to database.
    # Creating logs directory if it doesn't found.
    def __init__(self):
        try:
            os.mkdir("logs")
        except FileExistsError:
            print("Failed to creating directory \"logs\" or it is already exists.")
            os.system("pause")

        self.day = datetime.datetime.now()
        self.day = self.day.strftime('%d-%m-%Y_%H-%M-%S')
        self.name = "logs\\log_" + str(self.day) + ".dat"
        self.log_file = open(self.name, 'w')

    # Destructor.
    def __del__(self):
        self.log_file.close()

    # The main method of class.
    # Writing data in the log file log_[date].dat.
    def write_log(self, flag, log_info, conn):
        time = datetime.datetime.now().time()
        time = time.strftime('%H:%M:%S')

        if flag == "-1":
            self.log_file.write(time + " Action done with result: " + str(log_info) + "\n")
        else:
            try:
                cursor = conn.cursor()
            except Exception:
                self.log_file.write(time + " Action done with result: " + Db.report_handler[8] + "\n")
            else:
                self.log_file.write(time + " Action done with result: " + Db.report_handler[9] + "\n")
                query = "SELECT * FROM public." + str(log_info)

                try:
                    cursor.execute(query)
                except Exception:
                    self.log_file.write(time + " Action done with result: " + Db.report_handler[16] + "\n")
                else:
                    self.log_file.write(time + " Action done with result: " + Db.report_handler[17] + "\n")
                    result = cursor.fetchall()

                    self.log_file.write(time + " Editing table: " + str(log_info) + "\n")

                    for i in result:
                        self.log_file.write(str(i) + "\n")

                    try:
                        conn.commit()
                    except:
                        self.log_file.write(time + " Action done with result: " + Db.report_handler[12] + "\n")
                    else:
                        self.log_file.write(time + " Action done with result: " + Db.report_handler[13] + "\n")

                        try:
                            cursor.close()
                        except Exception:
                            self.log_file.write(time + " Action done with result: " + Db.report_handler[14] + "\n")
                        else:
                            self.log_file.write(time + " Action done with result: " + Db.report_handler[15] + "\n")


class Db:
    """The basic class using in work with your Postgres DB."""

    # List of reports for logging system.
    report_handler = ['Signed in!', 'Wrong DB name!', 'Wrong user name!', 'Wrong password!', 'Wrong host adress!',
                      'Cannot connect to database!', 'Cannot close connection!', 'Connection closed!',
                      'Some cursor connection problems!', 'Cursor connected!', 'Failed to write in table!',
                      'Successfully written in table!', 'Failed to commit transaction!', 'Transaction commited!',
                      'Cannot close cursor!', 'Cursor closed!', 'Failed to read from table!',
                      'Successfully read from table!', 'Cannot open file!', 'File is opened!', 'Groups table is empty!',
                      'Teachers table is empty!', 'Students table is empty!', 'User request failed!',
                      'User request completed!', 'Transaction has been finished correctly!', 'No database response!',
                      'Subjects list is empty!', 'Achievements list is empty!', 'Faults list is empty!',
                      'NULL name have been got!']

    # Constructor.
    # Opening DB connection, starting logging system.
    # Getting data from system file.
    # Connection data is stored in a "data.dat" file in MD5 format.
    def __init__(self, db_name, user_name, pswd, host_addr):
        self.log = Logging()
        self.data = GetData()
        self.result = self.data.chk_data(db_name, user_name, pswd, host_addr)
        self.conn = None
        self.connected = 0

        if self.result == 0:
            try:
                self.conn = psycopg2.connect(dbname=db_name, user=user_name, password=pswd, host=host_addr)
            except Exception:
                self.log.write_log("-1", Db.report_handler[5], self.conn)
            else:
                self.connected = 1

        self.log.write_log("-1", Db.report_handler[self.result], self.conn)

    # Destructor.
    # Closing DB connection, removing logging system.
    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            self.log.write_log("-1", Db.report_handler[6], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[7], self.conn)

        del self.data
        del self.log

    # Important part of every method filling DB tables.
    def finish_transaction(self, cursor, table_name):
        try:
            self.conn.commit()
        except Exception:
            self.log.write_log("-1", Db.report_handler[12], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[13], self.conn)

            try:
                cursor.close()
            except Exception:
                self.log.write_log("-1", Db.report_handler[14], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[15], self.conn)

                print(Db.report_handler[25])
                os.system("pause")

        self.log.write_log("0", table_name, self.conn)

    # Getting random name.
    def name_rand(self):
        name = [0, 0, 0]

        try:
            # Random gender choice.
            if random.randint(0, 1) == 0:
                l_file = open(r'dicts\l_names_m.dat', 'r', encoding='utf-8')
                l_name = l_file.readlines()

                f_file = open(r'dicts\f_names_m.dat', 'r', encoding='utf-8')
                f_name = f_file.readlines()

                patronymic_file = open(r'dicts\patronymics_m.dat', 'r', encoding='utf-8')
                patronymic = patronymic_file.readlines()
            else:
                l_file = open(r'dicts\l_names_f.dat', 'r', encoding='utf-8')
                l_name = l_file.readlines()

                f_file = open(r'dicts\f_names_f.dat', 'r', encoding='utf-8')
                f_name = f_file.readlines()

                patronymic_file = open(r'dicts\patronymics_f.dat', 'r', encoding='utf-8')
                patronymic = patronymic_file.readlines()

            l_name = random.choice(l_name)
            f_name = random.choice(f_name)
            patronymic = random.choice(patronymic)
        except FileNotFoundError:
            self.log.write_log("-1", Db.report_handler[18], self.conn)

            return 0
        else:
            self.log.write_log("-1", Db.report_handler[19], self.conn)

            name[0] = l_name.rstrip('\n')
            name[1] = f_name.rstrip('\n')
            name[2] = patronymic.rstrip('\n')

            l_file.close()
            f_file.close()
            patronymic_file.close()

            return name

    # Getting random subject.
    def subject_rand(self, digit):
        try:
            # The choice between two dictionaries (junior or high school), depending on the class digit.
            if digit < 5:
                sub_file = open(r'dicts\subjects_jun.dat', 'r', encoding='utf-8')
                sub_list = sub_file.readlines()
            else:
                sub_file = open(r'dicts\subjects_high.dat', 'r', encoding='utf-8')
                sub_list = sub_file.readlines()
        except FileNotFoundError:
            self.log.write_log("-1", Db.report_handler[18], self.conn)

            return 0
        else:
            self.log.write_log("-1", Db.report_handler[19], self.conn)

            sub_file.close()

            return sub_list

    # Getting random date.
    @staticmethod
    def date_rand():
        return str(random.randint(1, 28)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(2019, 2020))

    # Generation "groups" table.
    def groups_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)
            now = datetime.datetime.now()

            try:
                for i in range(int(self.data.data_file[4].rstrip('\n'))):
                    enrollment = now.year - i

                    if now.month < 9:
                        enrollment -= 1
                    group_num = now.year - enrollment

                    if now.month >= 9:
                        group_num += 1

                    for j in range(0, random.randint(1, 4)):
                        cursor.execute(
                            'INSERT INTO public.groups (group_ch, enrollment, group_num) VALUES (%s, %s, %s)',
                            (chr(j + 1072), str(enrollment), str(group_num)))
            except Exception:
                self.log.write_log("-1", Db.report_handler[10], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[11], self.conn)

            self.finish_transaction(cursor, "Groups")

    # Generation "students" table.
    def students_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)

            try:
                cursor.execute('SELECT group_id FROM public.groups')
                groups_id = cursor.fetchall()
            except Exception:
                self.log.write_log("-1", Db.report_handler[16], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[17], self.conn)

                if len(groups_id) != 0:
                    try:
                        for i in groups_id:
                            for j in range(int(self.data.data_file[11].rstrip('\n')),
                                           int(self.data.data_file[12].rstrip('\n'))):
                                name = self.name_rand()
                                if name != 0 and len(name) != 0:
                                    cursor.execute(
                                        'INSERT INTO public.students (last_name, first_name, patrononymic, group_id) '
                                        'VALUES (%s, %s, %s, %s)', (name[0], name[1], name[2], i[0]))
                                else:
                                    self.log.write_log("-1", Db.report_handler[30], self.conn)
                    except Exception:
                        self.log.write_log("-1", Db.report_handler[10], self.conn)
                    else:
                        self.log.write_log("-1", Db.report_handler[11], self.conn)
                else:
                    self.log.write_log("-1", Db.report_handler[20], self.conn)

            self.finish_transaction(cursor, "Students")

    # Generation "teachers" table.
    def teachers_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)

            try:
                for i in range(int(self.data.data_file[5].rstrip('\n'))):
                    name = self.name_rand()

                    if name != 0 and len(name) != 0:
                        cursor.execute('INSERT INTO public.teachers (last_name, first_name, patrononymic, classroom) '
                                       'VALUES (%s, %s, %s, %s)', (name[0], name[1], name[2], str(i)))
                    else:
                        self.log.write_log("-1", Db.report_handler[30], self.conn)
            except Exception:
                self.log.write_log("-1", Db.report_handler[10], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[11], self.conn)

            self.finish_transaction(cursor, "Teachers")

    # Generation "marks" table.
    def marks_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)

            try:
                cursor.execute('SELECT group_id, group_num FROM public.groups')
                groups = cursor.fetchall()
            except Exception:
                self.log.write_log("-1", Db.report_handler[16], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[17], self.conn)

                if len(groups) != 0:
                    for i in groups:
                        subject = self.subject_rand(i[1])

                        if len(subject) != 0 and subject != 0:
                            try:
                                cursor.execute('SELECT student_id FROM public.students '
                                               'WHERE group_id = {0}'.format(i[0]))
                                student_id = cursor.fetchall()

                                cursor.execute('SELECT teacher_id FROM public.teachers')
                                teacher_id = cursor.fetchall()
                            except Exception:
                                self.log.write_log("-1", Db.report_handler[16], self.conn)
                            else:
                                self.log.write_log("-1", Db.report_handler[17], self.conn)

                                try:
                                    for j in student_id:
                                        date = self.date_rand()

                                        for k in range(int(self.data.data_file[13].rstrip('\n')),
                                                       int(self.data.data_file[14].rstrip('\n'))):
                                            cursor.execute(
                                                'INSERT INTO public.marks (student_id, subject_id, teacher_id, date, '
                                                'mark) VALUES (%s, %s, %s, %s, %s)',
                                                (j[0], str(random.choice(subject).rstrip('\n')),
                                                 str(random.choice(teacher_id)[0]), date,
                                                 str(random.randint(int(self.data.data_file[6].rstrip('\n')),
                                                                    int(self.data.data_file[7].rstrip('\n'))))))
                                except Exception:
                                    self.log.write_log("-1", Db.report_handler[10], self.conn)
                                else:
                                    self.log.write_log("-1", Db.report_handler[11], self.conn)
                        else:
                            self.log.write_log("-1", Db.report_handler[27], self.conn)

                else:
                    self.log.write_log("-1", Db.report_handler[20], self.conn)

            self.finish_transaction(cursor, "Marks")

    # Generation "homework" table.
    def homework_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)

            try:
                cursor.execute('SELECT group_id, group_num FROM public.groups')
                groups = cursor.fetchall()

                cursor.execute('SELECT teacher_id FROM public.teachers')
                teacher_id = cursor.fetchall()
            except Exception:
                self.log.write_log("-1", Db.report_handler[16], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[17], self.conn)

                if len(groups) != 0:
                    if len(teacher_id) != 0:
                        try:
                            for i in groups:
                                subject = self.subject_rand(i[1])

                                if subject != 0 and len(subject) != 0:
                                    for j in range(int(self.data.data_file[8].rstrip('\n')),
                                                   int(self.data.data_file[9].rstrip('\n'))):
                                        task = "Стр. " + str(random.randint(1, 150)) + ", №" + \
                                               str(random.randint(1, 90))
                                        date = self.date_rand()

                                        cursor.execute(
                                            'INSERT INTO public.homework (teacher_id, subject_id, group_id, info, date)'
                                            'VALUES (%s, %s, %s, %s, %s)',
                                            (str(random.choice(teacher_id)[0]),
                                             str(random.choice(subject).rstrip('\n')), i[0], task, date))
                                else:
                                    self.log.write_log("-1", Db.report_handler[27], self.conn)
                        except Exception:
                            self.log.write_log("-1", Db.report_handler[10], self.conn)
                        else:
                            self.log.write_log("-1", Db.report_handler[11], self.conn)
                    else:
                        self.log.write_log("-1", Db.report_handler[21], self.conn)
                else:
                    self.log.write_log("-1", Db.report_handler[20], self.conn)

            self.finish_transaction(cursor, "Homework")

    # Generation "achievements" table.
    def achievements_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)
    
            try:
                cursor.execute('SELECT student_id FROM public.students')
                student_id = cursor.fetchall()
    
                cursor.execute('SELECT COUNT (*) FROM public.students')
                student_cnt = cursor.fetchall()
                student_cnt = int(student_cnt[0][0])
            except Exception:
                self.log.write_log("-1", Db.report_handler[16], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[17], self.conn)
    
                if student_cnt != 0:
                    try:
                        achv_file = open(r'dicts\achvs.dat', 'r', encoding='utf-8')
                        achv = achv_file.readlines()
                    except FileNotFoundError:
                        self.log.write_log("-1", Db.report_handler[18], self.conn)
                    else:
                        self.log.write_log("-1", Db.report_handler[19], self.conn)
    
                        try:
                            if len(achv) != 0:
                                for i in range(1, random.randint(1, student_cnt)):
                                    cursor.execute('INSERT INTO public.achievements (student_id, name, place) '
                                                   'VALUES (%s, %s, %s)',
                                                   (random.choice(student_id), random.choice(achv).rstrip('\n'),
                                                    random.randint(1, int(self.data.data_file[10].rstrip('\n')))))
                            else:
                                self.log.write_log("-1", Db.report_handler[28], self.conn)
                        except Exception:
                            self.log.write_log("-1", Db.report_handler[10], self.conn)
                        else:
                            self.log.write_log("-1", Db.report_handler[11], self.conn)
    
                        achv_file.close()
                else:
                    self.log.write_log("-1", Db.report_handler[22], self.conn)
    
            self.finish_transaction(cursor, "Achievements")

    # Generation "faults" table.
    def faults_gen(self):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)
    
            try:
                cursor.execute('SELECT student_id FROM public.students')
                student_id = cursor.fetchall()
    
                cursor.execute('SELECT COUNT (*) FROM public.students')
                student_cnt = cursor.fetchall()
                student_cnt = int(student_cnt[0][0])
    
                cursor.execute('SELECT teacher_id FROM public.teachers')
                teacher_id = cursor.fetchall()
            except Exception:
                self.log.write_log("-1", Db.report_handler[16], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[17], self.conn)
    
                if student_cnt != 0:
                    if len(teacher_id) != 0:
                        try:
                            fault_file = open(r'dicts\faults.dat', 'r', encoding='utf-8')
                            fault = fault_file.readlines()
                        except FileNotFoundError:
                            self.log.write_log("-1", Db.report_handler[18], self.conn)
                        else:
                            self.log.write_log("-1", Db.report_handler[19], self.conn)
    
                            if len(fault) != 0:
                                try:
                                    for i in range(1, random.randint(1, student_cnt)):
                                        cursor.execute('INSERT INTO public.faults (teacher_id, student_id, info) '
                                                       'VALUES (%s, %s, %s)',
                                                       (str(random.choice(teacher_id)[0]),
                                                        str(random.choice(student_id)[0]),
                                                        random.choice(fault).rstrip('\n')))
                                except Exception:
                                    self.log.write_log("-1", Db.report_handler[10], self.conn)
                                else:
                                    self.log.write_log("-1", Db.report_handler[11], self.conn)
                            else:
                                self.log.write_log("-1", Db.report_handler[29], self.conn)
    
                            fault_file.close()
                    else:
                        self.log.write_log("-1", Db.report_handler[21], self.conn)
                else:
                    self.log.write_log("-1", Db.report_handler[22], self.conn)
    
            self.finish_transaction(cursor, "Faults")

    # Execution user's requests.
    def load_query(self, name):
        try:
            cursor = self.conn.cursor()
        except Exception:
            self.log.write_log("-1", Db.report_handler[8], self.conn)
        else:
            self.log.write_log("-1", Db.report_handler[9], self.conn)
    
            try:
                path = "sql\\" + name
                query_file = open(path, 'r', encoding='utf-8')
            except FileNotFoundError:
                self.log.write_log("-1", Db.report_handler[18], self.conn)
                print("No such file found.\n")
            else:
                self.log.write_log("-1", Db.report_handler[19], self.conn)
                query_strs = query_file.readlines()
                query = ''
    
                for i in query_strs:
                    query += i.rstrip('\n')
    
                try:
                    result = "User request done with: "
                    cursor.execute(query)
    
                    try:
                        result += str(cursor.fetchall())
                    except Exception:
                        self.log.write_log("-1", Db.report_handler[26], self.conn)
                    else:
                        self.log.write_log("-1", result, self.conn)
                except Exception:
                    self.log.write_log("-1", Db.report_handler[23], self.conn)
                else:
                    self.log.write_log("-1", Db.report_handler[24], self.conn)
    
                query_file.close()
    
            try:
                self.conn.commit()
            except Exception:
                self.log.write_log("-1", Db.report_handler[12], self.conn)
            else:
                self.log.write_log("-1", Db.report_handler[13], self.conn)
    
                try:
                    cursor.close()
                except Exception:
                    self.log.write_log("-1", Db.report_handler[14], self.conn)
                else:
                    self.log.write_log("-1", Db.report_handler[15], self.conn)
    
                    print(Db.report_handler[25])
                    os.system("pause")
