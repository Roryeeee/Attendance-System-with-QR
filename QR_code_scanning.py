# qr_scanner.py
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime

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

# --- QR Scanner ---
cap = cv2.VideoCapture(0)
print("🔄 Scanner running. Show QR codes. Press ESC to exit.")

scanned_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    decoded_objects = decode(frame, symbols=[ZBarSymbol.QRCODE])

    for obj in decoded_objects:
        try:
            qr_data = obj.data.decode('utf-8')
            data = json.loads(qr_data)
        except:
            data = {"raw": qr_data}

        user_id = data.get("user_id")
        if not user_id or user_id in scanned_ids:
            continue

        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            if user.checked_in:
                status = "⚠️ Already checked in."
                color = (0, 0, 255)
            else:
                user.checked_in = True
                user.checkin_time = datetime.now()  # ← Uses PC local time
                session.commit()
                scanned_ids.add(user_id)
                status = "✅ Checked in!"
                color = (0, 255, 0)

            print(f"{status} - {user.name} ({user.role})")
        else:
            status = "❌ Unknown user."
            color = (0, 165, 255)

        pts = obj.rect
        cv2.rectangle(frame, (pts.left, pts.top), (pts.left + pts.width, pts.top + pts.height), color, 2)
        cv2.putText(frame, status, (pts.left, pts.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow('QR Scanner', frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
