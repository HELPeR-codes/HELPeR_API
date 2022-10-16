from blueprints.basic_endpoints import blueprint as basic_endpoints
from blueprints.annotation_endpoints import blueprint as annotation_endpoints
# from blueprints.keyphrase_endpoints import blueprint as keyphrase_endpoints
from multiprocessing import Process
from flask import Flask
from multiprocessing import Process
import time
from blueprints.scispacy_endpoint import  blueprint as scispacy_entpoints



from flask import  Flask
from blueprints.recsys_endpoints import blueprint as recsys_endpoints
# from blueprints.recsys_endpoints import blueprint as recsys2_endpoints
from blueprints.dbpedia_endpoints import  blueprint as dbpedia_endpoints

app = Flask(__name__)



app.config['RESTPLUS_MASK_SWAGGER'] = False
app.debug=False
app.register_blueprint(basic_endpoints)
app.register_blueprint(annotation_endpoints)
app.register_blueprint(recsys_endpoints)
# app.register_blueprint(recsys2_endpoints)
app.register_blueprint(dbpedia_endpoints)
app.register_blueprint(scispacy_entpoints)

# app.register_blueprint(keyphrase_endpoints)

# app.register_blueprint(jinja_template_blueprint)
# app.register_blueprint(documented_endpoint)

# @app.route('/documentation')
# def documentation():
#     return auto.html()


if __name__ == "__main__":
    app.run(port=10081)
