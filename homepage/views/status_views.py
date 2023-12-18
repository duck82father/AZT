from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

# from homepage import db
from homepage.forms import ChatForm
from homepage.models import Users, azquiz, Solved
from homepage.views.auth_views import login_required
from homepage.client import chatbot_client

import re

bp = Blueprint('status', __name__, url_prefix='/status')

@bp.route('/show/', methods=('GET', 'POST'))
@login_required
def show():
    quizs = azquiz.query
    solved = Solved.query.filter_by(user_id=g.user.id).first()
    return render_template('status.html', quizs=quizs, solved=solved)

@bp.route('/show/api/endpoint', methods=['POST'])
def api_endpoint():
    data = request.json  # JSON 형식의 데이터를 받기 위해 request.json 사용

    requestkey, quiznumber = data['key'], data['quiznumber']    
    result = re.findall(r'\d+', requestkey)
    
    if (result != [] and requestkey[-1:] == "번") or (result != [] and requestkey[-2:] == "문제"):
                result = int(result[0])
                if result > 120:
                    result = "문제가 없습니다. [ 범위 1 ~ 120번 ]"
                    resulttype = "order" 
                else: 
                    resulttype = "quiz"

    elif int(quiznumber) > 0 :
        target_quiz = azquiz.query.get(quiznumber)
        if "힌트" in requestkey or "hint" in requestkey.lower():
            result = target_quiz.hint
            resulttype = "order"
        else:
            if requestkey == target_quiz.answer:
                result = '<b class="fw-bold">정답</b>입니다🥳'
                resulttype = "answer"
            else :
                result = "다시 한 번 고민해보세요!"
                resulttype = "order"
    
    else :      
        result = chatbot_client(requestkey)
        resulttype = "order"
    
    return {'result':f'{result}', 'resulttype':f'{resulttype}'}