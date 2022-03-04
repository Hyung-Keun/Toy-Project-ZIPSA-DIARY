from datetime import datetime
from bson.objectid import ObjectId
import base64
import datetime as dt
import jwt
import hashlib
import json
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)
SECRET_KEY = 'ZIPSADIARY'

client = MongoClient('mongodb+srv://toyprojects:sparta@cluster0.wqxmi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbtoyprojects

@ app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect("diary")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@ app.route('/login')
def login():
    token_expired = request.args.get("token_expired")
    return render_template('login.html', token_expired=token_expired)


@ app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token.decode('utf8')})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@ app.route('/signup')
def register():
    return render_template('signup.html')


@ app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pwConfirm_receive = request.form['pwConfirm_give']
    phone_give_receive = request.form['phone_give']
    birthday_give_receive = request.form['birthday_give']
    sex_give_receive = request.form['sex_give']

    check_duplicate_user = db.user.find_one({'id': id_receive})

    if check_duplicate_user is not None:
        if check_duplicate_user['id'] == id_receive:
            return jsonify({'result': 'fail', 'msg': '중복된 아이디가 존재!.'})

    if pw_receive != pwConfirm_receive:
        return jsonify({'result': 'fail', 'msg': '비밀번호가 서로 불일치!'})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'phone': phone_give_receive, 'birthday': birthday_give_receive, 'sex': sex_give_receive})

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token.decode('utf8')})
    else:
        return jsonify({'result': 'fail', 'msg': '예기치 못한 오류가 발생하였습니다.'})


@app.route('/diary', methods=['GET'])
def show_diary():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        total_count = int(db.diary.estimated_document_count())
        diary_data = list(db.diary.find({}).sort("diary_create_date", 1).limit(12))
        diary = []

        for num in diary_data:
            num['_id'] = str(num['_id'])
            diary.append(num)
        return render_template('diary.html', diary=diary, count=len(diary),total_count=total_count)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/api/diary', methods=['GET'])
def get_diary_by_index():
    skipIndex = int(request.args.get("skipIndex"))
    limit = int(request.args.get("limit"))
    diary_data = list(db.diary.find({}).sort("diary_create_date", 1).skip(skipIndex).limit(limit))
    diary = []
    for num in diary_data:
        num['_id'] = str(num['_id'])
        diary.append(num)
    return jsonify({'diary': diary})


@app.route('/posting')
def posting():

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('posting.html', id=payload['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))

@app.route('/diary/<diary_id>', methods=['GET'])
def diary_detail(diary_id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        diary = db.diary.find_one({'_id': ObjectId(diary_id)})
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('diary_detail.html', diary=diary, user=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@ app.route('/diary_update/<id_data>')
def diary_update(id_data):
    author_info = db.diary.find_one({"_id": ObjectId(id_data)})
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        if author_info['author'] == payload['id']:
            return render_template('diary_update.html', id=payload['id'], data=author_info)
        else:
            return redirect("/diary/" + id_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@ app.route('/api/diary', methods=['POST'])
def save_diary():
    title = request.form['title_give']
    content = request.form['content_give']
    file = request.files["file_give"]
    friend_name = request.form['friend_name_give']
    friend_age = request.form['friend_age_give']
    friend_sex = request.form["friend_sex_give"]
    friend_species = request.form["friend_species_give"]

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.user.find_one({"id": payload['id']})

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/img/{filename}.{extension}'

    file.save(save_to)

    doc = {
        'diary_title': title,
        'diary_content': content,
        'friend_name': friend_name,
        'friend_age': friend_age,
        'friend_sex': friend_sex,
        'friend_species': friend_species,
        'diary_file': f'{filename}.{extension}',
        'diary_create_date': today.strftime('%Y.%m.%d.%H.%M.%S'),
        'author': user_info['id']
    }

    db.diary.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@ app.route('/api/diary', methods=['PUT'])
def update_diary():
    title = request.form['title_give']
    content = request.form['content_give']
    file_id = request.form['id_give']
    file = request.files.get("file_give")
    friend_name = request.form['friend_name_give']
    friend_age = request.form['friend_age_give']
    friend_sex = request.form['friend_sex_give']
    friend_species = request.form['friend_species_give']


    today = datetime.now()

    doc = {
        'diary_title': title,
        'diary_content': content,
        'diary_modified_date': today.strftime('%Y.%m.%d.%H.%M.%S'),
        'friend_name': friend_name,
        'friend_age': friend_age,
        'friend_sex': friend_sex,
        'friend_species': friend_species

    }

    if file is not None:
        extension = file.filename.split('.')[-1]
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}'
        save_to = f'static/img/{filename}.{extension}'
        file.save(save_to)
        doc['diary_file'] = f'{filename}.{extension}'

    db.diary.update_one({'_id': ObjectId(file_id)}, {'$set': doc})

    return jsonify({'msg': '수정 완료!'})


@ app.route('/api/diary', methods=['DELETE'])
def delete_diary():

    file_id = request.args.get("id_give")

    db.diary.delete_one({'_id': ObjectId(file_id)})

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
