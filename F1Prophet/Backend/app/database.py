from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, StaticPool
from flask import g
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

_engine = None
_session_factory = None

def init_db(app):
    global _engine, _session_factory
    
    database_url = app.config.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL not configured")
    
    _engine = create_engine(
        database_url,
        poolclass=QueuePool,
        
        pool_size=1,
        max_overflow=2,
        
        pool_recycle=120,
        pool_pre_ping=True,
        
        connect_args={
            "connect_timeout": 5,
            "charset": "utf8mb4",
            "autocommit": False,
        },
        
        # Logging
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
        with _engine.connect() as conn:
            conn.execute("SELECT 1")
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