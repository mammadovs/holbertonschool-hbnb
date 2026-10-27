#!/usr/bin/python3
from app.persistence.repository import Repository

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def add(self, obj):
        from app import db
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        from app import db
        return db.session.get(self.model, obj_id)

    def get_all(self):
        from app import db
        return db.session.query(self.model).all()

    def update(self, obj_id, data):
        from app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        from app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        from app import db
        query = {attr_name: attr_value}
        return db.session.query(self.model).filter_by(**query).first()
