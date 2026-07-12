from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from flask import g

Base = declarative_base()

_engine = None
_session_factory = None

def init_db(app):
    global _engine, _session_factory
    
    database_url = app.config.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL not configured in environment variables")
    
    _engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        pool_pre_ping=True,
        
        connect_args={
            "connect_timeout": 10,
            "read_timeout": 30,
            "write_timeout": 30,
            "charset": "utf8mb4"
        },
        
        echo=False,
        future=True,
    )
    
    @event.listens_for(_engine, "connect")
    def on_connect(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES'")
            cursor.execute("SET SESSION max_connections=1000")
            cursor.close()
        except Exception as e:
            print(f"Warning: Could not set MySQL session variables: {e}")
    
    _session_factory = sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=True,
        autocommit=False
    )
    
    app.teardown_appcontext(close_db)
    
    Base.metadata.create_all(_engine)
    
    print("Database initialized successfully")

def get_db():
    if 'db_session' not in g:
        if _session_factory is None:
            raise RuntimeError(
                "Database not initialized. Call init_db(app) in your app factory."
            )
        g.db_session = scoped_session(_session_factory)
    return g.db_session

def close_db(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        try:
            db_session.remove()
        except Exception as ex:
            print(f"Error closing database session: {ex}")

def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine not initialized")
    return _engine

def health_check():
    try:
        with _engine.connect() as conn:
            conn.execute("SELECT 1")
        return True, "Database connection OK"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"