from app import create_app, db
from app.models import User, Training, UserTraining

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Training": Training, "UserTraining": UserTraining}


if __name__ == "__main__":
    app.run(debug=True, port=8001)

# アプリケーションの起動時
with app.app_context():
    db.session.rollback()
