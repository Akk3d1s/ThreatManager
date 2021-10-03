#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import shutil

from app.models.role import Roles, Role


def execute_command(command):
    """execute commands and handle piping"""
    try:
        subprocess.run(command, shell=True)
    except Exception:
        print("psh: command not found: {}".format(command))

def psh_init():
    """Recreate new database with migration scripts"""
    psh_delete()
    f = open("app.db", "x")
    execute_command('flask db init')
    execute_command('flask db migrate')
    execute_command('flask db upgrade')
    psh_seed()

def psh_delete():
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
          - init
          - delete
          - seed""")

def main():
    while True:
        inp = input("$ ").split(" ")
        if inp[0] == "exit":
            break
        elif inp[0] == "seed":
            psh_seed()
            break
        elif inp[0] == "delete":
            psh_delete()
            break
        elif inp[0] == "init":
            psh_init()
            break
        elif inp[0] == "help":
            psh_help()
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()
