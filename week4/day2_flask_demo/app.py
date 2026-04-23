from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def profile():
    return render_template('profile.html',
        title='我的信息',
        name='张',
        major='软件技术',
        city='武汉',
        salary='5000+'
    )

@app.route('/projects')
def projects():
    project_list = ['hello.py', '记账本CLI', '记账本MySQL版', 'Flask学习项目']
    return render_template('projects.html', student='张', projects=project_list)

@app.route('/about')
def about():
    return render_template('about.html', name='张', major='软件技术')

@app.route('/score')
def score():
    return render_template('score.html', name='张', score=85)

@app.route('/skills')
def skills():
    return render_template('skills.html', skills=['Python', 'MySQL', 'Flask', 'Git', 'pymysql'])

if __name__ == '__main__':
    app.run(debug=True)
