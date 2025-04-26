import sqlite3

# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Example using SQLite
engine = create_engine("sqlite:///assistant_doctor.db", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

# تأكد من إنشاء الجداول عند التشغيل الأول فقط
Base.metadata.create_all(engine)

# إنشاء الاتصال
def create_connection():
    conn = sqlite3.connect("doctor_assistant.db")
    return conn

# إنشاء جدول المرضى
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            symptoms TEXT,
            report_text TEXT,
            diagnosis TEXT
        )
    """)
    conn.commit()
    conn.close()

# حفظ بيانات جديدة
def insert_record(name, symptoms, report_text, diagnosis):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (name, symptoms, report_text, diagnosis) VALUES (?, ?, ?, ?)",
                   (name, symptoms, report_text, diagnosis))
    conn.commit()
    conn.close()

# عرض كل السجلات
def get_all_records():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    conn.close()
    return records
