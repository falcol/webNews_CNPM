from __init__ import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(1000), nullable=False)
    title = db.Column(db.String(1000), nullable=False)
    href = db.Column(db.String(1000), nullable=False)
    sapo = db.Column(db.String(1000), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('news', lazy=True))

    def __repr__(self):
        return '<News %r>' % self.title


class Corona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    territory = db.Column(db.String(1000), nullable=False)
    infection = db.Column(db.String(1000), nullable=False)
    death = db.Column(db.String(1000), nullable=False)
    serious = db.Column(db.String(1000), nullable=False)
    cure = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Corona %r>' % self.territory


class Corona_VN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(1000), nullable=False)
    infection = db.Column(db.String(1000), nullable=False)
    death = db.Column(db.String(1000), nullable=False)
    cured = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Corona_VN %r>' % self.place
