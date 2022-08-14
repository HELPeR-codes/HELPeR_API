# blueprints/jinja_endpoint/__init__.py
from flask import Blueprint, request, render_template
import blueprints.jinja_endpoint.init_db
connection_neo = init_db.connection
blueprint = Blueprint('jinja_template', __name__, url_prefix='/jinja_template')

main_query = """MATCH (n:MainTopic) RETURN n """
sub_query = """MATCH ({name :'{main_topic}'})-[:OvCa_MainTopic]-(n)
RETURN n  """
concept_query = """MATCH ({name :'{main_topic}'})-[:OvCa_SubTopic]-(concept)
RETURN concept  """

@blueprint.route('')
def get_template():
    x = connection_neo.run(main_query).data()
    print(x)
    return render_template('maintopics.html',posts=x)

@blueprint.route('/maintopics')
def get_maintopics():
    x = connection_neo.run(main_query).data()
    print(x)
    return render_template('maintopics.html',posts=x)

@blueprint.route('/subtopics')
def get_subtopics():
    print(request.args.get('topic'))
    x = connection_neo.run(sub_query.replace('{main_topic}', request.args.get('topic'))).data()
    topics = connection_neo.run(main_query).data()
    return render_template('subtopics.html',posts=x,maintopic=request.args.get('topic'),topics=topics)

@blueprint.route('/concepts')
def get_conceptlist():
    print(request.args.get('subtopic'))
    print(request.args.get('maintopic'))
    x = connection_neo.run(concept_query.replace('{main_topic}', request.args.get('subtopic'))).data()
    topics = connection_neo.run(main_query).data()
    # print(x)
    return render_template('concepts.html',posts=x,maintopic=request.args.get('maintopic'),subtopic=request.args.get('subtopic'),topics=topics)

# @blueprint.route('/maintopics')
# def index():
#
#     return render_template('maintopics.html', posts=x)