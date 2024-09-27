from flask import render_template
from flask_login import login_required, current_user
from app.main import bp
from app.models import Training, UserTraining

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html')

@bp.route('/trainings')
@login_required
def trainings():
    trainings = Training.query.all()
    return render_template('main/trainings.html', trainings=trainings)

@bp.route('/progress')
@login_required
def progress():
    user_trainings = UserTraining.query.filter_by(user_id=current_user.id).all()
    return render_template('main/progress.html', user_trainings=user_trainings)