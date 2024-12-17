from dotenv import load_dotenv
import os

# SQLAlchemy related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Create MySQL database connection URL
MYSQL_URL = (f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
             f"{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:"
             f"{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")

# Connect to the database and create a connection pool
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Get session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
