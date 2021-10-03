
from app import db
from app.models import UserRole, ThreatStatus, ThreatCategory

role = UserRole(role='Citizen')
db.session.add(role)
role = UserRole(role='Editor')
db.session.add(role)
role = UserRole(role='Approver')
db.session.add(role)
role = UserRole(role='Admin')
db.session.add(role)

status = ThreatStatus(status='Pending')
db.session.add(status)
status = ThreatStatus(status='Resolving')
db.session.add(status)
status = ThreatStatus(status='Resolved')
db.session.add(status)

category = ThreatCategory(category='Minor')
db.session.add(category)
category = ThreatCategory(category='Monitor')
db.session.add(category)
category = ThreatCategory(category='Normal')
db.session.add(category)
category = ThreatCategory(category='Serious')
db.session.add(category)

db.session.commit()