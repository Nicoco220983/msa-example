import flask

blueprint = flask.Blueprint('test_base', __name__,
    static_folder='static'
)

def register_msa_blueprint(app):
    app.register_blueprint(blueprint, url_prefix='/msa/test/base')

@blueprint.route('/')
def root_endp():
    return blueprint.send_static_file('base.html')

COUNTER = 0

@blueprint.route("/counter", methods=['GET'])
def get_counter_endp():
    return { "counter": COUNTER }

@blueprint.route("/counter", methods=['POST'])
def post_counter_endp():
    global COUNTER
    COUNTER += 1
    return { "done": True }