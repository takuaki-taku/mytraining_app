"""
メインアプリケーションのルートを定義するモジュール。

このモジュールは、トレーニング一覧、トレーニング詳細、ユーザーの進捗状況、管理者ページなどのルートを定義しています。
"""

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import User, Training, UserTraining


@bp.route("/")
@bp.route("/index")
def index():
    """メインページを表示する。"""
    return render_template("main/index.html")


@bp.route("/trainings")
def trainings():
    """トレーニング一覧を表示する。"""
    search = request.args.get("search", "")
    trainings = Training.query.filter(Training.name.ilike(f"%{search}%")).all()
    user_trainings = {}
    if current_user.is_authenticated:
        user_trainings = {
            ut.training_id: ut.status
            for ut in UserTraining.query.filter_by(user_id=current_user.id).all()
        }
    return render_template(
        "main/trainings.html",
        trainings=trainings,
        user_trainings=user_trainings,
        search=search,
    )


@bp.route("/training/<int:training_id>")
def training_details(training_id):
    """トレーニングの詳細情報をJSON形式で返す。"""
    training = Training.query.get_or_404(training_id)
    return jsonify(
        {
            "name": training.name,
            "category": training.category,
            "description": training.description,
            "points": training.points,
            "video_url": training.video_url,
        }
    )


@bp.route("/progress")
@login_required
def progress():
    """ユーザーのトレーニング進捗状況を表示する。"""
    user_trainings = UserTraining.query.filter_by(user_id=current_user.id).all()
    in_progress = []
    completed = []
    for ut in user_trainings:
        if ut.status == "取り組み中":
            in_progress.append(ut)
        elif ut.status == "完了":
            completed.append(ut)

    print(f"In Progress: {in_progress}")  # デバッグ用
    print(f"Completed: {completed}")  # デバッグ用

    return render_template(
        "main/user_progress.html", in_progress=in_progress, completed=completed
    )


@bp.route("/admin")
def admin():
    """管理者ページを表示する。"""
    users = User.query.all()
    trainings = Training.query.all()
    return render_template("main/admin.html", users=users, trainings=trainings)


@bp.route("/add_training", methods=["GET", "POST"])
def add_training():
    """新しいトレーニングを追加する。"""
    if request.method == "POST":
        # フォームの処理
        name = request.form["name"]
        category = request.form["category"]
        description = request.form["description"]
        points = request.form["points"]
        video_url = request.form.get("video_url")  # オプションなので get で取得
        training = Training(
            name=name,
            category=category,
            description=description,
            points=points,
            video_url=video_url,
        )
        db.session.add(training)
        db.session.commit()
        flash("トレーニングを追加しました。")
        return redirect(url_for("main.admin"))
    return render_template("main/add_training.html")


@bp.route("/toggle_admin/<int:user_id>", methods=["POST"])
def toggle_admin(user_id):
    """ユーザーの管理者権限を切り替える。"""
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash("Admin status toggled.")
    return redirect(url_for("main.admin"))


@bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    """ユーザーを削除する。"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("ユーザーを削除しました。")
    return redirect(url_for("main.admin"))


@bp.route("/edit_training/<int:training_id>", methods=["GET", "POST"])
def edit_training(training_id):
    """トレーニング情報を編集する。"""
    training = Training.query.get_or_404(training_id)
    if request.method == "POST":
        training.name = request.form["name"]
        training.category = request.form["category"]
        db.session.commit()
        flash("Training updated.")
        return redirect(url_for("main.admin"))
    return render_template("main/edit_training.html", training=training)


@bp.route("/delete_training/<int:training_id>", methods=["POST"])
def delete_training(training_id):
    """トレーニングを削除する。"""
    training = Training.query.get_or_404(training_id)
    db.session.delete(training)
    db.session.commit()
    flash("Training deleted.")
    return redirect(url_for("main.admin"))


@bp.route("/update_training_status/<int:training_id>", methods=["POST"])
def update_training_status(training_id):
    """ユーザーのトレーニングステータスを更新する。"""
    status = request.form.get("status")
    user_training = UserTraining.query.filter_by(
        user_id=current_user.id, training_id=training_id
    ).first()
    if user_training:
        user_training.status = status
    else:
        user_training = UserTraining(
            user_id=current_user.id, training_id=training_id, status=status
        )
        db.session.add(user_training)
    db.session.commit()
    flash("Training status updated.")
    return redirect(url_for("main.trainings"))
