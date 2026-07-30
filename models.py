from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student' or 'admin'
    has_premium_access = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    progress_records = db.relationship('UserProgress', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_completed_lesson(self, lesson_id):
        progress = UserProgress.query.filter_by(user_id=self.id, lesson_id=lesson_id).first()
        return progress.completed if progress else False

    def get_progress_percentage(self):
        total_lessons = Lesson.query.count()
        if total_lessons == 0:
            return 0
        completed_lessons = UserProgress.query.filter_by(user_id=self.id, completed=True).count()
        return round((completed_lessons / total_lessons) * 100)

    def get_module_progress(self, module_id):
        module_lessons = Lesson.query.filter_by(module_id=module_id).all()
        if not module_lessons:
            return 0
        lesson_ids = [l.id for l in module_lessons]
        completed_count = UserProgress.query.filter_by(user_id=self.id, completed=True)\
            .filter(UserProgress.lesson_id.in_(lesson_ids)).count()
        return round((completed_count / len(module_lessons)) * 100)


class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False, default=1)
    is_free = db.Column(db.Boolean, default=False, nullable=False)  # True for Module 1, False for 2, 3, 4
    icon = db.Column(db.String(50), default="fa-book")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    lessons = db.relationship('Lesson', backref='module', lazy=True, order_by="Lesson.order", cascade="all, delete-orphan")


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(255), nullable=False)
    pdf_filename = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False, default=1)
    duration_minutes = db.Column(db.Integer, default=15)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    progress_records = db.relationship('UserProgress', backref='lesson', lazy=True, cascade="all, delete-orphan")


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=True, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_id', name='_user_lesson_uc'),
    )
