"""
アプリケーションのデータベースモデルを定義するモジュール。

このモジュールは、ユーザー、トレーニング、ユーザーとトレーニングの関係を表すモデルを定義しています。
"""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    """ユーザーを表すモデル。"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    user_trainings = db.relationship(
        "UserTraining",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        """パスワードをハッシュ化して保存する。"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """パスワードが正しいかどうかを確認する。"""
        return check_password_hash(self.password_hash, password)


class Training(db.Model):
    """トレーニングを表すモデル。"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer)
    video_url = db.Column(db.String(200))
    user_trainings = db.relationship(
        "UserTraining", back_populates="training", lazy="dynamic"
    )


class UserTraining(db.Model):
    """ユーザーとトレーニングの関係を表すモデル。"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey("training.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    user = db.relationship("User", back_populates="user_trainings")
    training = db.relationship("Training", back_populates="user_trainings")


@login_manager.user_loader
def load_user(user_id):
    """ユーザーIDからユーザーオブジェクトを取得する。"""
    return User.query.get(int(user_id))
