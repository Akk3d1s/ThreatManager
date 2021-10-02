#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import shutil
from app.models import Role, Roles


def execute_command(command):
    """execute commands and handle piping"""
    try:
        subprocess.run(command, shell=True)
    except Exception:
        print("psh: command not found: {}".format(command))

def psh_recreate_db():
    """Recreate new database with migration scripts"""
    psh_delete_db()
    f = open("app.db", "x")
    execute_command('flask db init')
    execute_command('flask db migrate')
    execute_command('flask db upgrade')
    psh_seed()

def psh_delete_db():
    """delete database"""
    if os.path.exists("app.db"):
        os.remove("app.db")
    else:
        print("Database does not exist")

    if os.path.exists("migrations"):
        shutil.rmtree('migrations')
    else:
        print("migrations does not exist")


def psh_seed():
    """seed data into tables"""
    roles = [str(Roles.PUBLIC), str(Roles.READ), str(Roles.EDITOR), str(Roles.APPROVER), str(Roles.DEVELOPER), str(Roles.ADMIN)]
    for r in roles:
        role = Role(role=r.replace('Roles.', ''))
        role.save()

def psh_help():
    print("""psh: shell implementation in Python.
          Supports all basic shell commands in addition to custom commands such as: 
          - add
          - list""")

def main():
    while True:
        inp = input("$ ").split(" ")
        if inp[0] == "exit":
            break
        elif inp[0] == "seed":
            psh_seed()
            break
        elif inp[0] == "delete-db":
            psh_delete_db()
            break
        elif inp[0] == "recreate-db":
            psh_recreate_db()
            break
        elif inp[0] == "help":
            psh_help()
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()
