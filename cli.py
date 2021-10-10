#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import shutil

from app.models.user import User
from app.models.user_role import UserRole, UserRoles
from app.models.threat_status import ThreatStatus, ThreatStatuses
from app.models.threat_category import ThreatCategory, ThreatCategories
from app.models.threat_attachment import ThreatAttachment
from app.models.threat_attachment_extension import ThreatAttachmentExtension



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

def psh_testing():
	"""offers some automated security testing"""
	tests = str(input(print("What do you want to test? |security| code quality"))) 
	if tests == "security":
		execute_command('safety check --full-report')
	else:
		print("Command not found")
		
def psh_seed():
    """seed data into tables"""
    roles = [str(UserRoles.PUBLIC), str(UserRoles.READ), str(UserRoles.EDITOR), str(UserRoles.APPROVER), str(UserRoles.DEVELOPER), str(UserRoles.ADMIN)]
    for r in roles:
        role = UserRole(role=r.replace('UserRoles.', ''))
        role.save()
    statuses = [str(ThreatStatuses.PENDING), str(ThreatStatuses.APPROVINGNEWCASE), str(ThreatStatuses.RESOLVING), str(ThreatStatuses.APPROVINGENDCASE), str(ThreatStatuses.RESOLVED), str(ThreatStatuses.REJECTED)]
    for s in statuses:
        status = ThreatStatus(status=s.replace('ThreatStatuses.', ''))
        status.save()
    categories = [str(ThreatCategories.LOW), str(ThreatCategories.MEDIUM), str(ThreatCategories.HIGH), str(ThreatCategories.CRITICAL)]
    for c in categories:
        category = ThreatCategory(category=c.replace('ThreatCategories.', ''))
        category.save()
    admin = User(first_name="Police", surname="Admin", email="admin@police.com", role_id=6)
    admin.set_password("admin")
    admin.save()
    # attachment = ThreatAttachment()
    # attachment.save()

    

def psh_help():
    print("""psh: shell implementation in Python.
          Supports all basic shell commands in addition to custom commands such as: 
          - init
          - delete
          - seed
		  - testing""")

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
        elif inp[0] == "testing":
            psh_testing()
            break
        elif inp[0] == "help":
            psh_help()
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()
