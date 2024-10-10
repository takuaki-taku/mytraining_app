"""
認証関連のルートを定義するモジュール。
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app import db
from app.auth import bp
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    ログインページの処理を行う。
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Invalid username or password")
    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    ユーザー登録ページの処理を行う。
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered successfully. Please log in.")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("管理者権限が必要です。")
        return redirect(url_for("main.admin"))

    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("管理者ユーザーは削除できません。")
        return redirect(url_for("main.admin"))

    try:
        # ユーザーに関連するUserTrainingレコードを削除
        UserTraining.query.filter_by(user_id=user.id).delete()

        # ユーザーを削除
        db.session.delete(user)
        db.session.commit()
        flash(f"ユーザー {user.username} を削除しました。")
    except Exception as e:
        db.session.rollback()
        flash(f"ユーザーの削除中にエラーが発生しました: {str(e)}")

    return redirect(url_for("main.admin"))
