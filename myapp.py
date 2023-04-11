from flask import (
    Flask, 
    render_template,
    request)
from sqlalchemy import func


from models import db, Types, Places, Friends, Frogs, FrogToFriend

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frogs.db'
db.app = app
db.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/statistics')
def stat():
    info = {}
    info['users'] = db.session.query(Frogs) \
        .group_by(Frogs.human_name) \
        .count()
    info['users_stat'] = db.session.query(Frogs.human_name, func.count(Frogs.frog_id)) \
        .group_by(Frogs.human_name)\
        .order_by(func.count(Frogs.frog_id).desc()) \
        .all()
    info['frogs'] = db.session.query(Frogs).count()
    info['frogs_stat'] = db.session.query(Frogs).all()
    info['types'] = db.session.query(Types).count()
    info['types_stat'] = db.session.query(Types.type_name, Types.type_id, func.count(Frogs.frog_id)) \
        .join(Frogs, isouter=True) \
        .group_by(Types.type_name, Types.type_id) \
        .order_by(func.count(Frogs.frog_id).desc()) \
        .all()
    info['places'] = db.session.query(Places).count()
    info['places_stat'] = db.session.query(Places.place_name, Places.place_id, func.count(Frogs.frog_id)) \
        .join(Frogs, isouter=True) \
        .group_by(Places.place_name, Places.place_id) \
        .order_by(func.count(Frogs.frog_id).desc()) \
        .all()
    info['friends'] = db.session.query(Friends).count()
    info['friends_stat'] = db.session.query(Friends.friend_name, Friends.friend_id, func.count(FrogToFriend.frog_id)) \
        .join(FrogToFriend, isouter=True) \
        .group_by(Friends.friend_name, Friends.friend_id) \
        .order_by(func.count(FrogToFriend.frog_id).desc()) \
        .all()
    return render_template("stat.html", info=info)


@app.route('/form', methods=['post', 'get'])
def form():
    return render_template("form.html")


@app.route('/new_frog', methods=['post', 'get'])
def new_frog():
    if request.method == 'POST':
        info = request.form
        place_id = db.session.query(Places) \
            .filter(Places.place_name == info["place"]) \
            .first() \
            .place_id
        type_id = db.session.query(Types) \
            .filter(Types.type_name == info["frog_type"]) \
            .first() \
            .type_id
        frog =  Frogs(
            human_name = info['human_name'],
            frog_name = info['frog_name'],
            place_id = place_id,
            frog_type_id = type_id
        )
        db.session.add(frog)
        db.session.commit()
        friends = [[], []]
        for friend in ['friend1', 'friend2', 'friend3']:
            if friend in info:
                fr_id = db.session.query(Friends)\
                    .filter(Friends.friend_name==info[friend]) \
                    .first() \
                    .friend_id
                friends[0].append(info[friend])
                friends[1].append(fr_id)
                fr2fr = FrogToFriend(
                    frog_id = frog.frog_id,
                    friend_id = fr_id
                )
                db.session.add(fr2fr)
                db.session.commit()
        pic = f".\static\{info['frog_type']}.jpg"
    return render_template('frog.html', frog=info, photo=pic, friends=friends, type_id=type_id, place_id=place_id)


@app.route('/place/<place_id>')
def place_info(place_id: int):
    place_info = Places.query.get(place_id)
    inhab = db.session.query(Frogs, Types)\
            .join(Types) \
            .filter(Frogs.place_id==place_id).all()
    return render_template("place.html", place_info=place_info, inhab=inhab)

@app.route('/frog/<frog_id>')
def frog_info(frog_id: int):
    frog = db.session.query(Frogs, Types, Places)\
            .join(Types) \
            .join(Places) \
            .filter(Frogs.frog_id==frog_id).one()
    frog_friends = db.session.query(FrogToFriend, Friends)\
            .join(Friends)\
            .filter(FrogToFriend.frog_id==frog_id).all()
    friends = [[], []]
    for friend in frog_friends:
            friends[0].append(friend.Friends.friend_name)
            friends[1].append(friend.Friends.friend_id)    
    return render_template('frog.html', frog={
        'frog_name': frog.Frogs.frog_name, 
        'frog_type': frog.Types.type_name,
        'place': frog.Places.place_name,
        'human_name': frog.Frogs.human_name,}, 
        photo=f'..\static\{frog.Types.type_img}', 
        friends=friends, 
        type_id=frog.Types.type_id, 
        place_id=frog.Places.place_id)


@app.route('/type/<type_id>')
def type_info(type_id: int):
    type_info = Types.query.get(type_id)
    frogs = db.session.query(Frogs, Places)\
            .join(Places) \
            .filter(Frogs.frog_type_id==type_id).all()
    return render_template("type.html", type_info=type_info, frogs=frogs)


@app.route('/world')
def make_world():
    places = db.session.query(Places).all()
    return render_template("world.html", places=places)


@app.route('/friend/<friend_id>')
def friend_info(friend_id):
    friend_info = Friends.query.get(friend_id)
    frogs = db.session.query(Frogs, Places, Types)\
            .join(Types) \
            .join(Places) \
            .join(FrogToFriend) \
            .filter(FrogToFriend.friend_id==friend_id).all()
    return render_template("friend.html", friend_info=friend_info, frogs=frogs)


if __name__ == '__main__':
    app.run()
