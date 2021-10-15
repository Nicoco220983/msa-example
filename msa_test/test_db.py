import flask
from markupsafe import escape

blueprint = flask.Blueprint('test_db', __name__,
    static_folder='static'
)

def register_msa_blueprint(app):
    app.register_blueprint(blueprint, url_prefix='/msa/test/db')

def register_msa_db_models(db, _session):
    global session, Data
    session = _session

    class Data(db.Model):
        id = db.Column(db.String(80), primary_key=True)
        value = db.Column(db.Integer, nullable=False)

        def export(self):
            return {
                "id": self.id,
                "value": self.value
            }

@blueprint.route('/')
def root_endp():
    return blueprint.send_static_file('db.html')

@blueprint.route("/<id>", methods=['GET'])
def get_endp(id):
    data = Data.query.filter_by(id=escape(id)).first()
    if data is None:
        data = Data(id=escape(id), value=0)
    return {
        "data": data.export()
    }

@blueprint.route("/<id>", methods=['POST'])
def post_endp(id):
    body = flask.request.get_json()
    data = Data.query.filter_by(id=escape(id)).with_for_update().first()
    if data is None:
        data = Data(id=escape(id), value=0)
    data.value = body["value"]
    session.add(data)
    session.commit()
    return { "done": True }