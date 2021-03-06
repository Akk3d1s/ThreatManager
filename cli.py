#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import shutil
import io

from app.models.user import User
from app.models.user_role import UserRole, UserRoles
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus, ThreatStatuses
from app.models.threat_category import ThreatCategory, ThreatCategories
from app.models.comment import Comment
from app.models.file import CommentFile


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


def psh_security():
    """offers some automated security testing of packages and code"""
    execute_command('safety check --full-report')
    execute_command('bandit -r app')


def psh_seed():
    """seed data into tables"""
    roles = [str(UserRoles.PUBLIC), str(UserRoles.READ), str(UserRoles.EDITOR), str(UserRoles.APPROVER), str(UserRoles.DEVELOPER), str(UserRoles.ADMIN)]
    for r in roles:
        role = UserRole(role=r.replace('UserRoles.', ''))
        role.save()
    statuses = [str(ThreatStatuses.PENDING), str(ThreatStatuses.APPROVINGNEWCASE), str(ThreatStatuses.RESOLVING), str(ThreatStatuses.APPROVINGENDCASE), str(ThreatStatuses.RESOLVED), str(ThreatStatuses.REJECTED), str(ThreatStatuses.CANCELED)]
    for s in statuses:
        status = ThreatStatus(status=s.replace('ThreatStatuses.', ''))
        status.save()
    categories = [str(ThreatCategories.LOW), str(ThreatCategories.MEDIUM), str(ThreatCategories.HIGH), str(ThreatCategories.CRITICAL)]
    for c in categories:
        category = ThreatCategory(category=c.replace('ThreatCategories.', ''))
        category.save()
    justin = User(first_name="Justin", surname="Lo", email="justin@gmail.com", role_id=1, totp_secret="4HMSIHRWLTJM25VFB37FAGYSSZG2LER6", is_active=1)
    justin.set_password("justin")
    justin.save()
    hendrik = User(first_name="Hendrik", surname="Rooyen", email="hendrik@police.com", role_id=3, totp_secret="4HMSIHRWLTJM25VFB37FAGYSSZG2LER6", is_active=1)
    hendrik.set_password("hendrik")
    hendrik.save()
    jonny = User(first_name="Jonny", surname="Mason", email="jonny@police.com", role_id=4, totp_secret="4HMSIHRWLTJM25VFB37FAGYSSZG2LER6", is_active=1)
    jonny.set_password("jonny")
    jonny.save()
    developer = User(first_name="Developer", surname="King", email="developer@police.com", role_id=5, totp_secret="4HMSIHRWLTJM25VFB37FAGYSSZG2LER6", is_active=1)
    developer.set_password("developer")
    developer.save()
    admin = User(first_name="Police", surname="Admin", email="admin@police.com", role_id=6, totp_secret="4HMSIHRWLTJM25VFB37FAGYSSZG2LER6", is_active=1)
    admin.set_password("admin")
    admin.save()
    citizen = User(first_name="Darth", surname="Citizen", email="citizen@gmail.com", role_id=1, totp_secret="4HMSIHRWLTJM25VFB37FAGYSSZG2LER6", is_active=1)
    citizen.set_password("citizen")
    citizen.save()
    threat = Threat(title='Seed Threat', description='This is a seed threat for testing', reproduce_steps='Seed created this threat and used for testing', user_id=1, status_id=1, category_id=1)
    threat.save()
    comment = Comment(comment='Seed Comment', user_id=3, threat_id=threat.id)
    comment.save()
    commentFile = CommentFile(file='seed_comment_file', comment_id=comment.id)
    commentFile.save()


def psh_help():
    print("""psh: shell implementation in Python.
          Supports all basic shell commands in addition to custom commands such as: 
          - init
          - delete
          - seed
          - security""")


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
        elif inp[0] == "security":
            psh_security()
            break
        elif inp[0] == "help":
            psh_help()
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()
