from flask import Blueprint, render_template, url_for, request, g, flash
from werkzeug.utils import redirect

from homepage import db
from homepage.forms import RankForm
from homepage.models import Users
from homepage.views.auth_views import login_required

bp = Blueprint('rank', __name__, url_prefix='/rank')

@bp.route('/rank', method=('GET', 'POST'))
@login_required
def rank():
    return "안녕하세요"