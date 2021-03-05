from flask import jsonify, Blueprint, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, \
    create_refresh_token
)

from application.app import db
from application.config import Config
from models.member import Member, MemberSchema
from application.exceptions import EmptyList, PasswordNotInForm, \
    FullnameNotInForm, EmailNotInForm, DuplicateMemberFound, MemberNotFound


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

    hashed_password = Member.hash_password(password)
    member = Member(email, hashed_password, fullname)
    duplicate_member = Member.query \
        .filter(Member.email == member.email) \
        .first()

    if duplicate_member:
        raise DuplicateMemberFound()

    try:
        db.session.add(member)
        db.session.commit()

    except Exception:
        db.session.rollback()

    return jsonify(MemberSchema().dump(member)), 200


@blueprint.route('/login', methods=['POST'])
def login():
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

    member = Member.query \
        .filter(Member.email == email) \
        .first()
    if not member or member.is_deleted:
        raise MemberNotFound()

    expires = Config.JWT_EXPIRES_DELTA
    if check_password_hash(member.hashed_password, password):
        access_token = create_access_token(
            identity=member.id,
            additional_claims = {"email": member.email},
            expires_delta=expires,
        )
        refresh_token = create_refresh_token(identity=member.id)

        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
        ), 200

    raise MemberNotFound()

