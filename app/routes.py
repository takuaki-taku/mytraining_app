from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from app.models import User, Training, UserTraining
from app import db
from functools import wraps

bp = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.all()
    trainings = Training.query.all()
    return render_template('admin.html', users=users, trainings=trainings)

@bp.route('/admin/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"ユーザー {user.username} の管理者権限が{'付与' if user.is_admin else '削除'}されました。")
    return redirect(url_for('main.admin'))

@bp.route('/admin/edit_training/<int:training_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_training(training_id):
    training = Training.query.get_or_404(training_id)
    if request.method == 'POST':
        training.name = request.form['name']
        training.category = request.form['category']
        training.description = request.form['description']
        training.points = request.form['points']
        training.video_url = request.form['video_url']
        db.session.commit()
        flash('トレーニングが更新されました。')
        return redirect(url_for('main.admin'))
    return render_template('edit_training.html', training=training)

@bp.route('/admin/delete_training/<int:training_id>', methods=['POST'])
@login_required
@admin_required
def delete_training(training_id):
    training = Training.query.get_or_404(training_id)
    db.session.delete(training)
    db.session.commit()
    flash('トレーニングが削除されました。')
    return redirect(url_for('main.admin'))

@bp.route('/')
def index():
    return render_template('overview.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/trainings')
def trainings():
    trainings = Training.query.all()
    return render_template('trainings.html', trainings=trainings)

@bp.route('/progress')
@login_required
def progress():
    in_progress = UserTraining.query.filter_by(user_id=current_user.id, status='in_progress').all()
    completed = UserTraining.query.filter_by(user_id=current_user.id, status='completed').all()
    return render_template('user_progress.html', in_progress=in_progress, completed=completed)

@bp.route('/register', methods=['GET', 'POST'])  #ユーザー登録機能
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@bp.route('/add_training', methods=['GET', 'POST'])
@login_required
def add_training():
    if not current_user.is_admin:
        abort(403)
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        points = request.form['points']
        video_url = request.form['video_url']
        
        new_training = Training(name=name, category=category, description=description, points=points, video_url=video_url)
        db.session.add(new_training)
        db.session.commit()
        
        flash('New training added successfully.')
        return redirect(url_for('main.trainings'))
    
    return render_template('add_training.html')

@bp.route('/update_training_status/<int:training_id>', methods=['POST'])
@login_required
def update_training_status():
    training_id = request.form['training_id']
    new_status = request.form['status']
    
    user_training = UserTraining.query.filter_by(user_id=current_user.id, training_id=training_id).first()
    
    if user_training:
        user_training.status = new_status
    else:
        new_user_training = UserTraining(user_id=current_user.id, training_id=training_id, status=new_status)
        db.session.add(new_user_training)
    
    db.session.commit()
    flash('Training status updated successfully.')
    return redirect(url_for('main.progress'))

