from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask import current_app, g

Base = declarative_base()

_engine = None
_session_factory = None

def init_db(app):
    global _engine, _session_factory
    
    cfg = app.config
    
    connection_string = (
        f"mysql+pymysql://{cfg['MYSQL_USER']}:{cfg['MYSQL_PASSWORD']}"
        f"@{cfg['MYSQL_HOST']}:{cfg['MYSQL_PORT']}/{cfg['MYSQL_DATABASE']}"
        f"?client_flag=2"
    )
    
    _engine = create_engine(
        connection_string,
        connect_args={
            "connect_timeout": 60,
            "read_timeout": 60,
            "write_timeout": 60
        },
        pool_recycle=60,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )
    
    _session_factory = sessionmaker(bind=_engine)
    app.teardown_appcontext(close_db)

def get_db():
    if 'db_session' not in g:
        if _session_factory is None:
            raise RuntimeError("Database not initialized. Call init_db(app) first.")
        g.db_session = scoped_session(_session_factory)
    return g.db_session

def close_db(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.remove()
