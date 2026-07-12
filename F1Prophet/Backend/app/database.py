from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from flask import g

Base = declarative_base()

_engine = None
_session_factory = None

def init_db(app):
    """Initialize database connection - DO NOT create tables here"""
    global _engine, _session_factory
    
    database_url = app.config.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL not configured")
    
    _engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=2,
        max_overflow=5,
        pool_recycle=300,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": 10,
            "charset": "utf8mb4"
        },
        echo=False,
    )
    
    _session_factory = sessionmaker(
        bind=_engine,
        expire_on_commit=False
    )
    
    app.teardown_appcontext(close_db)
    
    print("Database initialized (tables must exist in MySQL)")

def get_db():
    if 'db_session' not in g:
        if _session_factory is None:
            raise RuntimeError("Database not initialized")
        g.db_session = scoped_session(_session_factory)
    return g.db_session

def close_db(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        try:
            db_session.remove()
        except:
            pass