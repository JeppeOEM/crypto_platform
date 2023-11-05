from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


# Additionally it will prefix the endpoint of the function with the name of the blueprint
# which was given to the Blueprint constructor (in this case also simple_page).
# The blueprint’s name does not modify the URL, only the endpoint.

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)
