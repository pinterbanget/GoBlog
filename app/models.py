# Model for user database.
# TODO: change this to just post database

import sqlalchemy as sa
import sqlalchemy.orm as orm
from app import db, login
from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), index=True, unique=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(128))

    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    

class Post(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    body: orm.Mapped[str] = orm.mapped_column(sa.String(140))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(User.id), index=True)
    
    author: orm.Mapped[User] = orm.relationship(back_populates='posts')
    
    def __repr__(self):
        return f'<Post {self.body}>'
    

@login.user_loader
def load_user(id: int):
    return db.session.get(User, int(id))