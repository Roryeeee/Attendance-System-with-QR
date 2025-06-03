# export_attendance.py
import pandas as pd
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- SQLAlchemy setup ---
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String)
    team_name = Column(String, nullable=True)
    checked_in = Column(Boolean, default=False)
    checkin_time = Column(DateTime, nullable=True)

engine = create_engine('sqlite:///attendance.db')
Session = sessionmaker(bind=engine)
session = Session()

# --- Fetch users and export to CSV ---
users = session.query(User).all()

df = pd.DataFrame([{
    'User ID': u.user_id,
    'Name': u.name,
    'Role': u.role,
    'Team': u.team_name or '',
    'Checked In': 'Yes' if u.checked_in else 'No',
    'Check-in Time': u.checkin_time.strftime('%Y-%m-%d %H:%M:%S') if u.checkin_time else ''
} for u in users])

df.to_csv("attendance_log.csv", index=False)
print("📄 Attendance exported to 'attendance_log.csv'")
