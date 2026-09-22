import os
import logging
from flask import g
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

logger = logging.getLogger(__name__)

Base = declarative_base()

_engine = None
_session_factory = None

def init_db(app):
    global _engine, _session_factory
    
    raw_url = os.getenv('DATABASE_URL')
    
    if raw_url:
        if "?" in raw_url:
            raw_url = raw_url.split("?")[0]
            
        database_url = f"{raw_url}?charset=utf8mb4"
    else:
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', 'password_missing')
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = os.getenv('MYSQL_PORT', '3306')
        db_name = os.getenv('MYSQL_DATABASE', 'f1prophet')
        database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    
    app.config['DATABASE_URL'] = database_url
    
    _engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=1,
        max_overflow=2,
        pool_recycle=120,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": 5,
            "autocommit": False
        },
        echo=False,
        future=True,
    )


    @event.listens_for(_engine, "connect")
    def receive_connect(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES'")
            cursor.close()
        except Exception as e:
            logger.warning(f"Could not set MySQL session: {e}")
    
    @event.listens_for(_engine, "engine_disposed")
    def receive_engine_disposed(engine):
        logger.info("SQLAlchemy engine disposed")
    
    _session_factory = sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=True,
        autocommit=False,
    )
    
    try:
        from app.models import Base
        Base.metadata.create_all(bind=_engine)
        logger.info("Database schemas verified and initialized safely.")
    except Exception as err:
        logger.error(f"Schema generation hook skipped or failed: {err}")
    
    app.teardown_appcontext(close_db)
    logger.info("Database initialized (aggressive pooling for Railway)")


def get_db():
    if 'db_session' not in g:
        if _session_factory is None:
            raise RuntimeError("Database not initialized")
        try:
            g.db_session = scoped_session(_session_factory)
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise
    return g.db_session

def close_db(e=None):
    """Close database session safely"""
    db_session = g.pop('db_session', None)
    if db_session is not None:
        try:
            db_session.remove()
        except Exception as ex:
            logger.warning(f"Error closing session: {ex}")

def health_check():
    try:
        from sqlalchemy import text
        with _engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Database OK"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def register_health_check(app):
    @app.route('/api/health')
    def health():
        is_healthy, message = health_check()
        status_code = 200 if is_healthy else 503
        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'message': message,
            'database': 'connected' if is_healthy else 'disconnected'
        }, status_code