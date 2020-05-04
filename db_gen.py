# -*- coding: utf-8 -*-
# Orshak Ivan, 24.04.2020

import classes
import os


# Console easy menu.
def show_menu(flag):
    os.system("cls")

    if flag == 0:
        print("S -> Connect  |  E -> Exit")
    else:
        print("1. Fill the \"Groups\"\n2. Fill the \"Students\"\n3. Fill the \"Teachers\"\n4. Fill the \"Marks\"\n"
              "5. Fill the \"Achievements\"\n6. Fill the \"Faults\"\n7. Fill the \"Homework\"\n8. Query from file\n"
              "9. Disconnect")


# The handler of user commands.
def handler(user):
    command = input("Type your command:")

    if user.auth == 0:
        if command == 's' or command == 'S' or command == 'ы' or command == 'Ы':
            os.system("cls")
            user.connect()
        elif command == 'e' or command == 'E' or command == 'у' or command == 'У':
            del user
            os.system("cls")
            os.system(exit(0))
        else:
            print("Unknown command.")
            os.system("pause")
            os.system("cls")
    elif user.auth == 1:
        if command == '1':
            user.db.groups_gen()
        elif command == '2':
            user.db.students_gen()
        elif command == '3':
            user.db.teachers_gen()
        elif command == '4':
            user.db.marks_gen()
        elif command == '5':
            user.db.achievements_gen()
        elif command == '6':
            user.db.faults_gen()
        elif command == '7':
            user.db.homework_gen()
        elif command == '8':
            print("Put your .sql file in \"sql\" directory and type its name:", end='')
            user.db.load_query(input())
        elif command == '9':
            user.disconnect()
        else:
            print("Unknown command.")
            os.system("pause")
            os.system("cls")


# The main program function with infinity loop.
def main_loop():
    user = classes.User()

    while True:
        if user.auth == 0:
            show_menu(0)
        else:
            show_menu(1)

        handler(user)


# Start here.
if __name__ == '__main__':
    main_loop()
