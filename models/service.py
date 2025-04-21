from models.db import db

class Service(db.Model):
    __tablename__= 'service'

    id_service = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    cost = db.Column(db.Float, nullable = False)
    detail_service = db.Column(db.String(250), nullable = True)
    status_service = db.column(db.String(5), nullable = False)
    paid_method = db.column(db.String(20), nullable = False)
    priority = db.column (db.Integer, nullable = False)

    def __init__(self,name,cost,datail_service,status_service,paid_method,priority):
        self.name = name
        self.cost = cost
        self.datail_service = datail_service
        self.status_service = status_service
        self.paid_method = paid_method
        self.priority = priority

    def serialize(self):
        return {
            'id_service' : self.id_service,
            'name' : self.name,
            'cost' : self.cost,
            'datail_service' : self.datail_service,
            'status_service' : self.status_service,
            'paid_method' : self.paid_method,
            'priority' : self.priority,
        }
        






