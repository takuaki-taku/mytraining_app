from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from app import db
from app.main import bp
from app.models import User, Training, UserTraining

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html')

@bp.route('/trainings')
def trainings():
    user_trainings = {}
    if current_user.is_authenticated:
        user_trainings = {
            ut.training_id: ut.status
            for ut in UserTraining.query.filter_by(user_id=current_user.id).all()
        }
    trainings = Training.query.all()
    return render_template('main/trainings.html', trainings=trainings, user_trainings=user_trainings)

@bp.route('/progress')
def progress():
    return render_template('main/user_progress.html')

@bp.route('/admin')
def admin():
    users = User.query.all()
    trainings = Training.query.all()
    return render_template('main/admin.html', users=users, trainings=trainings)

@bp.route('/add_training', methods=['GET', 'POST'])
def add_training():
    if request.method == 'POST':
        # フォームの処理
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        points = request.form['points']
        video_url = request.form.get('video_url')  # オプションなので get で取得
        training = Training(name=name, category=category, description=description, points=points, video_url=video_url)
        db.session.add(training)
        db.session.commit()
        flash('トレーニングを追加しました。')
        return redirect(url_for('main.admin'))
    return render_template('main/add_training.html')

@bp.route('/toggle_admin/<int:user_id>', methods=['POST'])
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Admin status toggled.')
    return redirect(url_for('main.admin'))

@bp.route('/edit_training/<int:training_id>', methods=['GET', 'POST'])
def edit_training(training_id):
    training = Training.query.get_or_404(training_id)
    if request.method == 'POST':
        training.name = request.form['name']
        training.category = request.form['category']
        db.session.commit()
        flash('Training updated.')
        return redirect(url_for('main.admin'))
    return render_template('main/edit_training.html', training=training)

@bp.route('/delete_training/<int:training_id>', methods=['POST'])
def delete_training(training_id):
    training = Training.query.get_or_404(training_id)
    db.session.delete(training)
    db.session.commit()
    flash('Training deleted.')
    return redirect(url_for('main.admin'))

@bp.route('/update_training_status/<int:training_id>', methods=['POST'])
def update_training_status(training_id):
    status = request.form.get('status')
    user_training = UserTraining.query.filter_by(user_id=current_user.id, training_id=training_id).first()
    if user_training:
        user_training.status = status
    else:
        user_training = UserTraining(user_id=current_user.id, training_id=training_id, status=status)
        db.session.add(user_training)
    db.session.commit()
    flash('Training status updated.')
    return redirect(url_for('main.trainings'))