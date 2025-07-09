from flask import Flask, render_template, g, redirect, request
import re

app = Flask(__name__)

# Helper functions
def bold(text, query):
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    def replacer(match):
        return f'<strong>{match.group(0)}</strong>'

    return pattern.sub(replacer, text)

def in_paragraphs(text):
    paragraphs = text.split('\n\n')
    formatted_paragraphs = [
                            f'<p>{paragraph}</p>'
                            for paragraph in paragraphs
                            if paragraph
                            ]

    return ''.join(formatted_paragraphs)

def chapters_matching(query):
    if not query:
        return []

    results = []

    for index, name in enumerate(g.contents, start=1):
        results_dict = {'number': None, 'index': None, 'paragraphs': [],}

        with open(f'book_viewer/data/chp{index}.txt', 'r') as file:
            chapter_content=file.read()

        for para_num, paragraph in enumerate(chapter_content.split('\n\n'), start=1):
            if query in paragraph.lower():
                results_dict['number'] = index
                results_dict['name'] = name
                results_dict['paragraphs'].append({'text': paragraph, 'para_num': para_num,})

        if results_dict['paragraphs']:
            results.append(results_dict)

    return results

# Register filters
app.jinja_env.filters['in_paragraphs'] = in_paragraphs
app.jinja_env.filters['bold'] = bold

# Request hooks
@app.before_request
def load_contents():
    with open('book_viewer/data/toc.txt', 'r') as file:
        g.contents = file.readlines()

# Route handlers
@app.route('/')
def index():
    return render_template('home.html', contents=g.contents)

@app.route('/chapters/<page_num>')
def chapter(page_num):
    if page_num.isdigit() and (1 <= int(page_num) <= len(g.contents)):
        chapter_name = g.contents[int(page_num) - 1]
        chapter_title = f'Chapter {page_num}: {chapter_name}'

        with open(f'book_viewer/data/chp{page_num}.txt') as file:
            chapter_content = file.read()

        paragraphs = chapter_content.split('\n\n')

        return render_template('chapter.html',
                                chapter_title=chapter_title,
                                contents=g.contents,
                                paragraphs=paragraphs)
    else:
        return render_template('redirect_countdown.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = chapters_matching(query) if query else []

    return render_template('search.html', query=query, results=results)

# Error handlers
@app.errorhandler(404)
def page_not_found(_error):
    return render_template('redirect_countdown.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)