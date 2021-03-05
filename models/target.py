from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db, ma
from application.mixin import SoftDeleteMixin


class TargetMember(db.Model):
    __tablename__ = 'target_member'

    target_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('target.id'),
        primary_key=True,
    )
    member_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('member.id'),
        primary_key=True,
    )

    member = db.relationship(
        'Member',
        foreign_keys=[member_id],
    )
    target = db.relationship(
        'Target',
        foreign_keys=[target_id],
    )

    def init(self, member_id, target_id):
        self.member_id = member_id
        self.target_id = target_id

    def to_dict(self):
        return dict(
            member_id=self.member_id,
            target_id=self.target_id,
        )


class TargetMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TargetMember
        load_instance = True


class Target(db.Model, SoftDeleteMixin):
    __tablename__ = 'target'

    id = db.Column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
    )
    last_message_id = db.Column(
        UUID(as_uuid=True),
        nullable=True,
    )
    type = db.Column(
        db.String(25),
        nullable=False,
    )

    messages = db.relationship(
        'Message',
    )

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type,
    }

    def to_dict(self):
        return dict(
            id=self.id,
            last_message_id=self.last_message_id,
            members = [m.member_id for m in self.target_members],
            is_deleted = True if self.removed_at is not None else False,
            removed_at = self.removed_at,
            created_at=self.created_at,
        )


class TargetSchema(ma.SQLAlchemyAutoSchema):
#    members = ma.Method("get_target_members")
#    is_deleted = ma.Method("get_removed_status")

    class Meta:
        model = Target

#    def get_target_members(self, obj):
#        members = [m.member_id for m in obj.target_members]
#        return members
#
#    def get_removed_status(self, obj):
#        status = True if obj.is_deleted else False
#        return status

