# from sqlalchemy import Column, Integer, String, Text, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# class UserRecord(Base):
#     __tablename__ = 'user_records'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(100), nullable=False)
#     symptoms = Column(Text, nullable=True)
#     diagnosis = Column(Text, nullable=True)
#     report_text = Column(Text, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
