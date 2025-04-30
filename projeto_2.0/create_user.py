from app import app, db, User

with app.app_context():
    db.create_all()
    new_user = User(username='rodrigo', password='23207360')  # Em produção, use hash!
    db.session.add(new_user)
    db.session.commit()

    print("Usuário criado com sucesso!")
