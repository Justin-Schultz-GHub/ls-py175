from uuid import uuid4
from flask import (
                    abort,
                    flash,
                    Flask,
                    redirect,
                    render_template,
                    request,
                    session,
                    url_for,
                    )
from todos.utils import (
                        error_for_list_title,
                        find_list_by_id,
                        error_for_todo_item_name,
                        )

app = Flask(__name__)
app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route('/')
def index():
    return redirect(url_for('get_lists'))

@app.route('/lists/new')
def add_todo_list():
    return render_template('new_list.html')

@app.route('/lists/<list_id>')
def display_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])

    if lst:
        return render_template('list.html', lst=lst)

    abort(404)

@app.route('/lists')
def get_lists():
    return render_template('lists.html', lists=session['lists'])

@app.route('/lists', methods=['POST'])
def create_list():
    title = request.form['list_title'].strip()

    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, 'error')
        return render_template('new_list.html', title=title)

    session['lists'].append({
        'id': str(uuid4()),
        'title': title,
        'todos': [],
    })

    flash('The list has been created.', 'success')
    session.modified = True

    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>/todos', methods=['POST'])
def create_todo(list_id):
    todo = request.form['todo'].strip()
    lst = find_list_by_id(list_id, session['lists'])

    if not lst:
        abort(404)

    error = error_for_todo_item_name(todo)

    if error:
        flash(error, 'error')
        return render_template('list.html', lst=lst,todo=todo)

    lst['todos'].append({
        'id': str(uuid4()),
        'title': todo,
        'completed': False
        })

    flash('The todo item has been created.', 'success')
    session.modified = True

    return redirect(url_for('display_list', list_id=lst['id']))

if __name__ == "__main__":
    app.run(debug=True, port=8080)