from flask import render_template, flash, redirect, url_for, request
from app import db
from app.main import bp
from app.models import User, Training, UserTraining

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html')

@bp.route('/trainings')
def trainings():
    return render_template('main/trainings.html')

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
        return redirect(url_for('main.trainings'))
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