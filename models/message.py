from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db, ma
from application.mixin import SoftDeleteMixin


class Message(db.Model, SoftDeleteMixin):
    __tablename__ = 'message'

    id = db.Column(
        UUID(as_uuid=True),
        default=uuid4, primary_key=True
    )
    body = db.Column(
        db.String,
        nullable=False,
    )
    sender_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('member.id')
    )
    reciever_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('member.id')
    )
    target_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('target.id'),
    )

    sender = db.relationship(
        "Member",
        foreign_keys=[sender_id],
        uselist=False
    )
    reciever = db.relationship(
        "Member",
        foreign_keys=[reciever_id],
        uselist=False
    )

    def __init__(self, body, sender_id, reciever_id, target_id):
        self.body = body
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.target_id = target_id


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message

