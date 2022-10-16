# from blueprints.basic_endpoints import blueprint as basic_endpoints
from flask import  Flask
from blueprints.jinja_endpoint import blueprint as jinja_template_blueprint
# from blueprints.documented_endpoints import blueprint as documented_endpoint
from blueprints.annotation_endpoints import blueprint as annotation_endpoints

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False

# app.register_blueprint(basic_endpoints)
app.register_blueprint(jinja_template_blueprint)
# app.register_blueprint(documented_endpoint)
app.register_blueprint(annotation_endpoints)
# @app.route('/documentation')
# def documentation():
# return auto.html()

if __name__ == "__main__":
    app.run(port=10081)