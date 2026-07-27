import os
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv()

print("=" * 60)
print("F1 Prophet - Railway MySQL Diagnostics")
print("=" * 60)
print()

# 1. Check DATABASE_URL exists
database_url = os.getenv('DATABASE_URL')
print("1. Checking DATABASE_URL...")
if not database_url:
    print("   DATABASE_URL not set!")
    print("   Go to Railway → Project → Variables")
    print("   MySQL plugin should auto-set DATABASE_URL")
    sys.exit(1)
else:
    # Mask password
    parts = database_url.split('@')
    if len(parts) == 2:
        user_part = parts[0].split('://')[-1]
        user = user_part.split(':')[0]
        host_part = parts[1]
        masked = f"mysql+pymysql://{user}:***@{host_part}"
        print(f"   Found: {masked}")
    else:
        print(f"   Found: {database_url[:50]}...")

print()

# 2. Check if it's valid format
print("2. Validating DATABASE_URL format...")
if not database_url.startswith('mysql+pymysql://'):
    print(f"   Wrong format! Should start with 'mysql+pymysql://'")
    print(f"   Got: {database_url[:40]}...")
    sys.exit(1)
else:
    print("   Format is correct")

print()

# 3. Try to parse URL
print("3. Parsing connection details...")
try:
    from urllib.parse import urlparse
    parsed = urlparse(database_url)
    print(f"   Host: {parsed.hostname}")
    print(f"   Port: {parsed.port or 3306}")
    print(f"   User: {parsed.username}")
    print(f"   Database: {parsed.path.lstrip('/')}")
except Exception as e:
    print(f"   Could not parse: {e}")
    sys.exit(1)

print()

# 4. Try to import SQLAlchemy
print("4. Checking SQLAlchemy...")
try:
    from sqlalchemy import create_engine
    print("   SQLAlchemy imported")
except Exception as e:
    print(f"   Failed: {e}")
    sys.exit(1)

print()

# 5. Try to create engine
print("5. Creating SQLAlchemy engine...")
try:
    engine = create_engine(
        database_url,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5, "charset": "utf8mb4"},
    )
    print("   Engine created")
except Exception as e:
    print(f"   Failed: {e}")
    sys.exit(1)

print()

# 6. Try to connect
print("6. Attempting to connect to MySQL...")
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("   Connected and query successful!")
        print("   MySQL is responding")
except Exception as e:
    print(f"   Connection failed: {e}")
    print()
    print("   Possible causes:")
    print("   - MySQL plugin not added to Railway project")
    print("   - MySQL plugin not running")
    print("   - Wrong credentials in DATABASE_URL")
    print("   - Network connectivity issue")
    print()
    print("   To fix:")
    print("   1. Go to Railway dashboard")
    print("   2. Click your project")
    print("   3. Click 'Add' → 'Add MySQL'")
    print("   4. Wait for MySQL to start (2-3 min)")
    print("   5. Check Variables tab for DATABASE_URL")
    print("   6. Redeploy your app")
    sys.exit(1)

print()

# 7. Check if tables exist
print("7. Checking if tables exist...")
try:
    with engine.connect() as conn:
        result = conn.execute("SHOW TABLES")
        tables = [row[0] for row in result]
        if not tables:
            print("   No tables found!")
            print("   Did you import your database dump?")
            print()
            print("   Fix:")
            print("   1. Get your database dump")
            print("   2. Import via Railway MySQL plugin")
            print("   3. Or run: mysql -h [host] -u [user] -p [db] < dump.sql")
        else:
            print(f"   Found {len(tables)} tables:")
            for table in tables[:10]:  # Show first 10
                print(f"      - {table}")
except Exception as e:
    print(f"   Could not check tables: {e}")

print()
print("=" * 60)
print("All diagnostics completed!")
print("=" * 60)