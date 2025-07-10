from flask import Flask, render_template, redirect, url_for
import yaml

app = Flask(__name__)

with open('users.yaml', 'r') as file:
    users = yaml.safe_load(file)
    total_users = len(users)

def total_interests(users):
    return sum(len(user['interests']) for user in users.values())

@app.route('/')
def index():
    return (render_template('index.html',
            total_interests=total_interests(users),
            total_users= total_users
            ))

@app.route('/users')
def users_list():
    return (render_template('users.html',
            users=users,
            total_interests=total_interests(users),
            total_users= total_users
            ))

@app.route('/users/<user_name>')
def user_profile(user_name):
    data = users.get(user_name)
    if data:
        return (render_template('user.html',
                users=users,
                data=data,
                user_name=user_name,
                total_interests=total_interests(users),
                total_users= total_users
                ))
    else:
        return redirect(url_for('users_list'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)