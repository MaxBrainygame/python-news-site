from getpass import getpass
import sys
from webapp import create_app
from webapp.db import db
# from webapp.news.models import User - он импортит User вроде его надо не оттуда

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():
        print('такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_passowrd(password)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))


