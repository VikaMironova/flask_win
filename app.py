from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://demo_f:0806@localhost:5432/demo_fl"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owners = db.Column(db.String(60), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'AD %r' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("homef.html")


@app.route('/posts')
def posts():
    ads = AD.query.order_by(AD.date.desc()).all()
    return render_template("posts.html", ads=ads)


@app.route('/posts/<int:id>')
def posts_page(id):
    adi = AD.query.get(id)
    return render_template("posts_id.html", adi=adi)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    adi = AD.query.get_or_404(id)

    try:
        db.session.delete(adi)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Ошибка!"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    adi = AD.query.get(id)
    if request.method == "POST":
        adi.owners = request.form['owners']
        adi.title = request.form['title']
        adi.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка!"
    else:

        return render_template("posts_up.html", adi=adi)


@app.route('/create_ad', methods=['POST', 'GET'])
def create_ad():
    if request.method == "POST":
        owners = request.form['owners']
        title = request.form['title']
        text = request.form['text']

        ad = AD(owners=owners, title=title, text=text)

        try:
            db.session.add(ad)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка!"
    else:
        return render_template("create_ad.html")


if __name__ == "__main__":
    app.run(debug=True)
