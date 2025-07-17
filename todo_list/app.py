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
                        find_todo_by_id,
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
        return render_template('list.html', lst=lst, todo=todo)

    lst['todos'].append({
        'id': str(uuid4()),
        'title': todo,
        'completed': False
        })

    flash('The todo item has been created.', 'success')
    session.modified = True

    return redirect(url_for('display_list', list_id=lst['id']))

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=['POST'])
def toggle_todo_completion(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        abort(404)

    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        abort(404)

    todo['completed'] = request.form['completed'] == 'True'

    flash('Todo marked as completed.', 'success')
    session.modified = True

    return redirect(url_for('display_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=['POST'])
def delete_todo_item(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        abort(404)

    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        abort(404)

    lst['todos'].remove(todo)

    flash('Todo item successfully deleted.', 'success')
    session.modified = True

    return redirect(url_for('display_list', list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=8080)