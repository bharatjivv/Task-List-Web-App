from config import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    entity_name = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)
    task_time = db.Column(db.DateTime, nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(10), default='open')
    
    def to_json(self):
        return {
            "id" : self.id,
            "dateCreated" : self.date_created,
            "entityName" : self.entity_name,
            "taskType" : self.task_type,
            "taskTime" : self.task_time,
            "contactPerson" : self.contact_person,
            "note" : self.note,
            "status" : self.status
        }