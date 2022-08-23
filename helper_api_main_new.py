# from blueprints.basic_endpoints import blueprint as basic_endpoints
# from blueprints.annotation_endpoints import blueprint as annotation_endpoints
# from blueprints.keyphrase_endpoints import blueprint as keyphrase_endpoints
from blueprints.dbpedia_endpoints import  blueprint as dbpedia_endpoints
from flask import  Flask
# from blueprints.jinja_endpoint import blueprint as jinja_template_blueprint
# from blueprints.documented_endpoints import blueprint as documented_endpoint
# from blueprints.recsys_endpoints import blueprint as recsys_endpoints
app = Flask(__name__)


app.config['RESTPLUS_MASK_SWAGGER'] = False
app.debug=True
# app.register_blueprint(basic_endpoints)
# app.register_blueprint(annotation_endpoints)
# app.register_blueprint(recsys_endpoints)
# app.register_blueprint(keyphrase_endpoints)
app.register_blueprint(dbpedia_endpoints)
# app.register_blueprint(jinja_template_blueprint)
# app.register_blueprint(documented_endpoint)

# @app.route('/documentation')
# def documentation():
#     return auto.html()

if __name__ == "__main__":
    app.run(port=10087)