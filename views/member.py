from flask import jsonify, Blueprint, request

from application.app import db
from models.member import Member, MemberSchema
from application.exceptions import EmptyList, PasswordNotInForm, \
    FullnameNotInForm, EmailNotInForm


blueprint = Blueprint('models/member', __name__, url_prefix='/api/v1/member')


@blueprint.route('/register', methods=['POST'])
def register():
    if not request.json:
        raise EmptyList()

    if 'email' not in request.json and 'email' not in request.form:
        raise EmailNotInForm()

    if 'password' not in request.json and 'password' not in request.form:
        raise PasswordNotInForm()

    email = request.json.get('email')
    if not email:
        email = request.form.get('email')

    if not email:
        raise EmailNotInForm()

    password = request.json.get('password')
    if not password:
        password = request.form.get('password')

    if not password:
        raise PasswordNotInForm()

    fullname = request.json.get('fullname')
    if not fullname:
        fullname = request.form.get('fullname')

    if not fullname:
        raise FullnameNotInForm()

    member = Member()
    member.email = email
    member.hashed_password = member.hash_password(password)
    member.fullname = fullname
    duplicate_member = Member.query \
        .filter(Member.email == member.email) \
        .first()

    if duplicate_member:
        return jsonify(message="400 Membert Already Exists"), 400

    try:
        db.session.add(member)
        db.session.commit()

    except Exception:
        db.session.rollback()

    return jsonify(MemberSchema().dump(member)), 200

