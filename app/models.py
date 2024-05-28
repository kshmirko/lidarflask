from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from hashlib import md5



class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest=md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))



class Experiment(db.Model):
    start_time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(512))
    accum_time: so.Mapped[float] = so.mapped_column(sa.Float(), server_default="0.0")
    vert_res: so.Mapped[float]= so.mapped_column(sa.Float(), server_default="1500.0")

    __table_agrs__=(
        sa.CheckConstraint(accum_time >=0, name='check_accum_time_greater_0'),
        sa.CheckConstraint(accum_time <=120, name='check_accum_lime_less_120'),
        sa.CheckConstraint(vert_res >=1500, name='check_vert_res_greater_1500'),
        sa.CheckConstraint(vert_res <=1912.5, name='check_vert_res_less_1912.5'),
    )


class MeasurementCh1(db.Model):
    start_time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), primary_key=True)
    prof_len: so.Mapped[int] = so.mapped_column(sa.Integer(), server_default='512')
    count: so.Mapped[int] = so.mapped_column(sa.Integer())
    rep_rate: so.Mapped[int] = so.mapped_column(sa.Integer())
    experiment_time: so.Mapped[datetime] = so.mapped_column(sa.ForeignKey("experiment.start_time", name='fk_experiment_timech1'))
    prof_data: so.Mapped[sa.JSON] = so.mapped_column(sa.JSON(), nullable=True)
    experiment = so.relationship("Experiment", foreign_keys=[experiment_time])
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id", name='fk_ch1_user_id'))
    user = so.relationship("User", foreign_keys=[user_id])

    __table_agrs__ = (
        sa.CheckConstraint(prof_len>=128, name='check_prof_len_greater_128'),
        sa.CheckConstraint(prof_len<=1024, name='check_prof_len_less_1024'),
    )

class MeasurementCh2(db.Model):
    start_time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), primary_key=True)
    prof_len: so.Mapped[int] = so.mapped_column(sa.Integer(), server_default='512')
    count: so.Mapped[int] = so.mapped_column(sa.Integer())
    rep_rate: so.Mapped[int] = so.mapped_column(sa.Integer())
    experiment_time: so.Mapped[datetime] = so.mapped_column(sa.ForeignKey("experiment.start_time", name='fk_experiment_timech2'))
    prof_data: so.Mapped[sa.JSON] = so.mapped_column(sa.JSON(), nullable=True)
    experiment = so.relationship("Experiment", foreign_keys=[experiment_time])
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id", name='fk_ch2_user_id'))
    user = so.relationship("User", foreign_keys=[user_id])
    
    __table_agrs__ = (
        sa.CheckConstraint(prof_len>=128, name='check_prof_len_greater_128'),
        sa.CheckConstraint(prof_len<=1024, name='check_prof_len_less_1024'),
    )


