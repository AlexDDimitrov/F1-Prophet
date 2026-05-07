from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask import current_app, g

Base = declarative_base()

def get_engine():
    cfg = current_app.config
    connection_string = (
        f"mysql+pymysql://{cfg['MYSQL_USER']}:{cfg['MYSQL_PASSWORD']}"
        f"@{cfg['MYSQL_HOST']}:{cfg['MYSQL_PORT']}/{cfg['MYSQL_DATABASE']}"
    )
    return create_engine(connection_string, pool_pre_ping=True)

def get_db():
    if 'db_session' not in g:
        engine = get_engine()
        session_factory = sessionmaker(bind=engine)
        g.db_session = scoped_session(session_factory)
    return g.db_session

def close_db(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.remove()

def init_db(app):
    app.teardown_appcontext(close_db)