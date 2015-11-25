import bcrypt

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String
    )

from colanderalchemy import SQLAlchemySchemaNode

from c2corg_api.models import Base, users_schema

import colander


class PasswordUtil():
    """
    Utility class abstracting low-level password primitives.
    """
    @staticmethod
    def encrypt_password(plain_password):
        return bcrypt.hashpw(plain_password, bcrypt.gensalt())

    @staticmethod
    def is_password_valid(plain, encrypted):
        if isinstance(encrypted, unicode):
            encrypted = encrypted.encode("UTF-8")
        return bcrypt.hashpw(plain, encrypted) == encrypted


class User(Base):
    """
    Class containing the users' private and authentication data.
    """
    __tablename__ = 'user'
    __table_args__ = {"schema": users_schema}

    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    email_validated = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)
    _password = Column("password", String(255), nullable=False)
    temp_password = Column(String(255))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = PasswordUtil.encrypt_password(password)

    def set_temp_password(self, password):
        """When the user forgot her password, she may ask for a temporary
        password. This password is generated by the application and stored
        in the user table. At this stage, the user may log with either the
        temporary password or her old password.
        """
        self.temp_password = PasswordUtil.encrypt_password(password)

    def validate_password(self, plain_password, db_session):
        """Check the password against existing credentials.
        If the provided password is valid against the main password, the
        method returns True. If a temporary password exists and is valid,
        the password is updated, the user flushed to the database and the
        method returns True.
        Otherwise False is returned.
        """
        if PasswordUtil.is_password_valid(plain_password, self._password):
            return True
        if self.temp_password is not None and \
           self.temp_password != "" and \
           PasswordUtil.is_password_valid(plain_password, self.temp_password):
            self._password = self.temp_password
            self.temp_password = None
            db_session.add(self)
            db_session.flush()
            return True
        return False

    password = property(_get_password, _set_password)


schema_user = SQLAlchemySchemaNode(
    User,
    # whitelisted attributes
    includes=[
        'id', 'username', 'email', 'email_validated', 'admin'],
    overrides={
        'id': {
            'missing': None
        }
    })


schema_create_user = SQLAlchemySchemaNode(
    User,
    # whitelisted attributes
    includes=['username', 'email'],
    overrides={
        'email': {
            'validator': colander.Email()
        }
    })
