from __future__ import absolute_import
import pickle

from datetime import timedelta, datetime
from uuid import uuid4
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
_table_name = "sessions"
_data_serializer = pickle


def set_db_session_interface(app, table_name=None, data_serializer=None):
    global _table_name, _data_serializer
    if table_name is not None:
        _table_name = table_name
    if data_serializer is not None:
        _data_serializer = data_serializer
    db.init_app(app)
    app.session_interface = SQLAlchemySessionInterface()
    return app


class SQLAlchemySession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):

        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class SQLAlchemySessionInterface(SessionInterface):

    def __init__(self):
        # this could be your mysql database or sqlalchemy db object
        pass

    def generate_sid(self):
        return str(uuid4())

    def open_session(self, app, request):
        # query your cookie for the session id
        ret = None
        sid = request.cookies.get(app.session_cookie_name)

        if not sid:
            sid = self.generate_sid()
            ret = SQLAlchemySession(sid=sid, new=True)
        else:
            val = Session.query.get(sid)
            if val is not None:
                data = _data_serializer.loads(val.data)
                ret = SQLAlchemySession(data, sid=sid)
            else:
                ret = SQLAlchemySession(sid=sid, new=True)
        return ret

    def save_session(self, app, session, response):
        # save the sesion data if exists in db
        # return a response cookie with details
        domain = self.get_cookie_domain(app)

        val = Session.query.get(session.sid)
        now = datetime.utcnow()
        if not session:
            if val is not None:
                db.session.delete(val)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)

        else:
            data = _data_serializer.dumps(dict(session))
            if val is None:
                val = Session(session_id=session.sid, data=data, atime=now)
            else:
                val.atime = now
                val.data = data

            db.session.add(val)
            db.session.commit()

        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=now + timedelta(days=1), httponly=False,
                            domain=domain)


class Session(db.Model):
    __tablename__ = _table_name
    session_id = db.Column(db.String(129), unique=True, primary_key=True)
    atime = db.Column(db.DateTime())
    data = db.Column(db.Text())
