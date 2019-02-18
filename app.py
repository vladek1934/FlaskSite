from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Caesar',
        'title': '1',
        'content': '1',
        'date_posted': 'March 20, 2012'
    },
    {
        'author': 'Caesar',
        'title': '2',
        'content': '2',
        'date_posted': 'january 20, 2018'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
