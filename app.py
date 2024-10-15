from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime,select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env.local")

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("POSTGRES_URL")

db.init_app(app)

class Messages(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

@app.route("/")
def moans():
    messages = db.session.scalars(select(Messages).order_by(Messages.created_at.desc())).all()

    print(messages)
    return render_template('page.html', messages=messages)

@app.route("/moan", methods=["POST"])
def moan():
    if request.method == 'POST':
        moan = request.form["imoan"]
        if moan:
            db.session.add(Messages(message=moan, created_at=datetime.now()))
            db.session.commit()
    return redirect(url_for('moans'))

if __name__ == '__main__':
    pirnt(getenv("POSTGRES_URL"))
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=80 ,debug=True)
