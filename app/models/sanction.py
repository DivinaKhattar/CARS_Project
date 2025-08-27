from app import db

class SanctionLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), unique=True, nullable=False)
    contact_number = db.Column(db.String(20))
    date = db.Column(db.Date)
    sanction_pdf = db.Column(db.String(200))

    costs = db.relationship('SanctionCostEntry', backref='sanction_letter', cascade="all, delete-orphan")
    schedule_milestones = db.relationship('SanctionScheduleEntry', backref='sanction_letter', cascade="all, delete-orphan")
    cars_milestones = db.relationship('SanctionCARSEntry', backref='sanction_letter', cascade="all, delete-orphan")


class SanctionCostEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sanction_letter_id = db.Column(db.Integer, db.ForeignKey('sanction_letter.id'))
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)


class SanctionScheduleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sanction_letter_id = db.Column(db.Integer, db.ForeignKey('sanction_letter.id'))
    date = db.Column(db.Date)
    amount = db.Column(db.Float)


class SanctionCARSEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sanction_letter_id = db.Column(db.Integer, db.ForeignKey('sanction_letter.id'))
    milestone_description = db.Column(db.String(200))  # e.g., Milestone I
    deliverables = db.Column(db.String(300))
    duration_months = db.Column(db.Integer)
