from sqlalchemy 	import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy 	import Column, Integer, String
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase): pass

class Person(Base):
    __tablename__ = "users"
 
    id 							= Column(Integer, primary_key=True, index=True)
    login 						= Column(String)
    password					= Column(String)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

session 	= sessionmaker(autoflush=False, bind=engine)
db 			= session()
db_query	= db.query()
