# import streamlit as st
# import openai
# import pytesseract
# from PIL import Image
# from dotenv import load_dotenv
# from googletrans import Translator
# # import pytesseract
# import os

# load_dotenv()
# openai.api_key = os.getenv("OPEN_API_KEY")
# # pytesseract.pytesseract.tesseract_cmd = r"E:\Download\Tesseract\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = r"E:\Download\Tesseract\tesseract.exe"



# translator = Translator()
# st.set_page_config(page_title="مساعد الدكتور")
# st.title("مساعد الدكتور الذكي")

# # نص الأعراض
# user_input = st.text_input("اكتب الأعراض التي تشعر بها:")

# # رفع صورة فحص
# uploaded_image = st.file_uploader("أرفق صورة فحص (تحليل دم، أشعة...)", type=["jpg", "png", "jpeg"])

# ocr_text = ""

# if uploaded_image:
#     image = Image.open(uploaded_image)
#     ocr_text = pytesseract.image_to_string(image)
#     st.markdown("**النص المستخرج من الصورة:**")
#     st.code(ocr_text)

# # عند توفر أعراض أو صورة
# if user_input or ocr_text:
#     with st.spinner("جاري التحليل..."):

#         input_text = ""

#         # ترجمة الأعراض
#         if user_input:
#             translated_input = translator.translate(user_input, src='ar', dest='en').text
#             input_text += f"Patient symptoms: {translated_input}\n"

#         # إضافة نص الصورة (الفحص)
#         if ocr_text:
#             input_text += f"Lab report or scan content: {ocr_text}\n"

#         # إرسال لـ GPT
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a medical assistant. Based on symptoms and lab report, provide suggestions. Always recommend a real doctor."},
#                 {"role": "user", "content": input_text}
#             ]
#         )

#         english_reply = response["choices"][0]["message"]["content"]
#         arabic_reply = translator.translate(english_reply, src='en', dest='ar').text

#         st.markdown("**مساعد الدكتور:**")
#         st.write(arabic_reply)

















# import streamlit as st
# import openai
# import pytesseract
# from PIL import Image
# from dotenv import load_dotenv
# from googletrans import Translator
# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime
# import requests
# import os

# # تحميل المفاتيح من env
# load_dotenv()
# openai.api_key = os.getenv("OPEN_API_KEY")
# INFER_APP_ID = os.getenv("INFERMEDICA_APP_ID")
# INFER_APP_KEY = os.getenv("INFERMEDICA_APP_KEY")

# headers_infer = {
#     # "App-Id": INFER_APP_ID,
#     "App-Key": INFER_APP_KEY,
#     "Content-Type": "application/json",
#     "Model": "infermedica-en"
# }

# pytesseract.pytesseract.tesseract_cmd = r"E:\Download\Tesseract\tesseract.exe"

# # مترجم
# translator = Translator()

# # قاعدة البيانات
# engine = create_engine("sqlite:///doctor_assistant.db")
# Base = declarative_base()

# class UserRecord(Base):
#     __tablename__ = "user_records"
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     symptoms = Column(Text)
#     diagnosis = Column(Text)
#     report_text = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# # واجهة Streamlit
# st.set_page_config(page_title="مساعد الدكتور")
# st.title("🤖 مساعد الدكتور الذكي")

# username = st.text_input("👤 أدخل اسمك")

# user_input = st.text_input("✍️ اكتب الأعراض التي تشعر بها (بالعربية):")
# uploaded_image = st.file_uploader("📎 أرفق صورة فحص (تحليل دم، أشعة...)", type=["jpg", "png", "jpeg"])

# ocr_text = ""

# if uploaded_image:
#     image = Image.open(uploaded_image)
#     ocr_text = pytesseract.image_to_string(image)
#     st.markdown("🧾 **النص المستخرج من الصورة:**")
#     st.code(ocr_text)

# if (user_input or ocr_text) and username:
#     with st.spinner("⏳ جاري التحليل..."):
#         input_text = ""

#         # ترجمة الأعراض
#         if user_input:
#             translated_input = translator.translate(user_input, src='ar', dest='en').text
#             input_text += f"Patient symptoms: {translated_input}\n"

#             # تشخيص باستخدام Infermedica
#             search_url = f"https://api.infermedica.com/v3/symptoms?phrase={translated_input}"
#             search_res = requests.get(search_url, headers=headers_infer).json()

#             evidence = []
#             if search_res:
#                 evidence = [{"id": search_res[0]["id"], "choice_id": "present"}]

#             diagnosis_payload = {
#                 "sex": "male",
#                 "age": 30,
#                 "evidence": evidence
#             }

#             diagnosis_response = requests.post(
#                 "https://api.infermedica.com/v3/diagnosis",
#                 headers=headers_infer,
#                 json=diagnosis_payload
#             ).json()

#             diagnosis_list = [
#                 f"{cond['name']} - احتمال: {round(cond['probability']*100)}%"
#                 for cond in diagnosis_response.get("conditions", [])
#             ]

#             st.markdown("🧠 **تشخيص مبدئي من Infermedica:**")
#             for d in diagnosis_list:
#                 st.write("🔹", d)

#             input_text += f"Possible conditions: {', '.join(diagnosis_list)}\n"

#         # نص الفحص
#         if ocr_text:
#             input_text += f"Lab report or scan content: {ocr_text}\n"

#         # تحليل GPT
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a medical assistant. Based on symptoms and lab report, provide suggestions. Always recommend a real doctor."},
#                 {"role": "user", "content": input_text}
#             ]
#         )

#         english_reply = response["choices"][0]["message"]["content"]
#         arabic_reply = translator.translate(english_reply, src='en', dest='ar').text

#         st.subheader("📋 مساعد الدكتور:")
#         st.write(arabic_reply)

#         # حفظ
#         if st.button("💾 حفظ البيانات"):
#             session = Session()
#             record = UserRecord(
#                 username=username,
#                 symptoms=user_input,
#                 diagnosis=arabic_reply,
#                 report_text=ocr_text
#             )
#             session.add(record)
#             session.commit()
#             st.success("✅ تم حفظ بيانات المستخدم بنجاح!")
# else:
#     st.info("يرجى إدخال اسمك وبعض الأعراض أو صورة فحص للمتابعة.")




















# import streamlit as st
# import openai
# import pytesseract
# from PIL import Image
# from dotenv import load_dotenv
# from googletrans import Translator
# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime
# import requests
# import os

# # تحميل المفاتيح من env
# load_dotenv()
# openai.api_key = os.getenv("OPEN_API_KEY")
# INFER_APP_ID = os.getenv("INFERMEDICA_APP_ID")
# INFER_APP_KEY = os.getenv("INFERMEDICA_APP_KEY")


# # رأس API الخاص بـ MedlinePlus (لا حاجة لمفاتيح API هنا)
# # medlineplus_url = "https://medlineplus.gov/download/genetics/condition/alzheimer-disease.json"
# disease = "Diabetes"  # ممكن تغيرها حسب الحالة
# wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{disease}"

# pytesseract.pytesseract.tesseract_cmd = r"E:\Download\Tesseract\tesseract.exe"

# # مترجم
# translator = Translator()

# # قاعدة البيانات
# engine = create_engine("sqlite:///doctor_assistant.db")
# Base = declarative_base()

# class UserRecord(Base):
#     __tablename__ = "user_records"
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     symptoms = Column(Text)
#     diagnosis = Column(Text)
#     report_text = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# # واجهة Streamlit
# st.set_page_config(page_title="مساعد الدكتور")
# st.title("🤖 مساعد الدكتور الذكي")

# username = st.text_input("👤 أدخل اسمك")

# user_input = st.text_input("✍️ اكتب الأعراض التي تشعر بها (بالعربية):")
# uploaded_image = st.file_uploader("📎 أرفق صورة فحص (تحليل دم، أشعة...)", type=["jpg", "png", "jpeg"])

# ocr_text = ""

# if uploaded_image:
#     image = Image.open(uploaded_image)
#     ocr_text = pytesseract.image_to_string(image)
#     st.markdown("🧾 **النص المستخرج من الصورة:**")
#     st.code(ocr_text)

# if (user_input or ocr_text) and username:
#     with st.spinner("⏳ جاري التحليل..."):
#         input_text = ""

#         # ترجمة الأعراض
#         if user_input:
#             translated_input = translator.translate(user_input, src='ar', dest='en').text
#             input_text += f"Patient symptoms: {translated_input}\n"

#             # استخدام MedlinePlus API للحصول على معلومات حول مرض الزهايمر
#             response = requests.get(wiki_url)
            
#             if response.status_code == 200:
#                 data = response.json()
#                 # الحصول على التفاصيل المتعلقة بالمرض من JSON
#                 disease_name = data.get('condition', {}).get('name', 'غير معروف')
#                 description = data.get('condition', {}).get('description', 'لا توجد معلومات متوفرة')
                
#                 # st.markdown("🧠 **معلومات عن مرض الزهايمر من MedlinePlus:**")
#                 st.write(f"**اسم المرض:** {disease_name}")
#                 st.write(f"**الوصف:** {description}")

#                 input_text += f"Disease Information: {disease_name} - {description}\n"
#             else:
#                 st.error("حدث خطأ أثناء الحصول على البيانات من MedlinePlus.")

#         # نص الفحص
#         if ocr_text:
#             input_text += f"Lab report or scan content: {ocr_text}\n"

#         # تحليل GPT
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a medical assistant. Based on symptoms and lab report, provide suggestions. Always recommend a real doctor."},
#                 {"role": "user", "content": input_text}
#             ]
#         )

#         english_reply = response["choices"][0]["message"]["content"]
#         arabic_reply = translator.translate(english_reply, src='en', dest='ar').text

#         st.subheader("📋 مساعد الدكتور:")
#         st.write(arabic_reply)

#         # حفظ
#         if st.button("💾 حفظ البيانات"):
#             session = Session()
#             record = UserRecord(
#                 username=username,
#                 symptoms=user_input,
#                 diagnosis=arabic_reply,
#                 report_text=ocr_text
#             )
#             session.add(record)
#             session.commit()
#             st.success("✅ تم حفظ بيانات المستخدم بنجاح!")
# else:
#     st.info("يرجى إدخال اسمك وبعض الأعراض أو صورة فحص للمتابعة.")





# import streamlit as st
# import pytesseract
# from PIL import Image
# from dotenv import load_dotenv
# from googletrans import Translator
# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime
# import json
# import pandas as pd

# import os


# # تحميل المفاتيح من env
# load_dotenv()

# # تحميل بيانات الأمراض من ملف JSON
# with open("SymptomsOutput.json", "r", encoding="utf-8") as f:
#     disease_data = json.load(f)

# # إعدادات OCR
# pytesseract.pytesseract.tesseract_cmd = r"E:\Download\Tesseract\tesseract.exe"

# # مترجم
# translator = Translator()

# # قاعدة البيانات
# engine = create_engine("sqlite:///doctor_assistant.db")
# Session = sessionmaker(bind=engine)
# session = Session()

# # استعلام كل السجلات
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Text, DateTime

# Base = declarative_base()

# class UserRecord(Base):
#     __tablename__ = "user_records"
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     symptoms = Column(Text)
#     diagnosis = Column(Text)
#     report_text = Column(Text)
#     created_at = Column(DateTime)

# st.set_page_config(page_title="سجلات المستخدمين")
# st.title("📋 عرض سجلات المستخدمين السابقة")

# # تحميل السجلات من قاعدة البيانات
# records = session.query(UserRecord).order_by(UserRecord.created_at.desc()).all()

# # تحويل السجلات إلى DataFrame لسهولة العرض
# data = [{
#     "الاسم": r.username,
#     "الأعراض": r.symptoms,
#     "التشخيص": r.diagnosis,
#     "نص الفحص": r.report_text,
#     "تاريخ الإدخال": r.created_at.strftime("%Y-%m-%d %H:%M")
# } for r in records]

# df = pd.DataFrame(data)

# if not df.empty:
#     st.dataframe(df)
# else:
#     st.info("لا توجد سجلات محفوظة حالياً.")
# # واجهة Streamlit
# st.set_page_config(page_title="مساعد الدكتور")
# st.title("🤖 مساعد الدكتور الذكي")

# username = st.text_input("👤 أدخل اسمك")

# user_input = st.text_input("✍️ اكتب الأعراض التي تشعر بها (بالعربية):")
# uploaded_image = st.file_uploader("📎 أرفق صورة فحص (تحليل دم، أشعة...)", type=["jpg", "png", "jpeg"])

# ocr_text = ""

# if uploaded_image:
#     image = Image.open(uploaded_image)
#     ocr_text = pytesseract.image_to_string(image)
#     st.markdown("🧾 **النص المستخرج من الصورة:**")
#     st.code(ocr_text)

# if (user_input or ocr_text) and username:
#     with st.spinner("⏳ جاري التحليل..."):
#         input_text = ""

#         # ترجمة الأعراض
#     if user_input:
#      translated_input = translator.translate(user_input, src='ar', dest='en').text.lower()
#      input_text += f"Patient symptoms: {translated_input}\n"

#     matched_diseases = []
#     for disease in disease_data:
#         # التأكد من أن الأعراض هي قائمة
#         symptoms = disease.get("symptoms", [])
        
#         # تحقق من أن symptoms هو قائمة
#         if isinstance(symptoms, list):
#             # تحقق من تطابق جزئي في الأعراض
#             if any(symptom.lower() in translated_input for symptom in symptoms):
#                 matched_diseases.append(disease)
#         else:
#             # إذا كانت الأعراض ليست قائمة، تجاهل هذا المرض أو معالجته بطريقة أخرى
#             st.warning(f"❗ الأعراض لـ {disease['name']} غير معرفة بشكل صحيح.")
    
#     if matched_diseases:
#         st.markdown("🧠 **تشخيص مبدئي بناءً على قاعدة البيانات:**")
#         diagnosis_list = []
#         for d in matched_diseases:
#             diagnosis_list.append(d["name"])
#             st.write(f"**Question:** {d['text']}")
#             st.write(f"**Category:** {d['category']}")
#             st.write(f"**Default Value:** {d['default']}")
#             # st.write("🔹", d["name"])
#             # st.write("• الأعراض:", ", ".join(d["symptoms"]))
#             # st.write("• الفحوصات:", ", ".join(d["tests"]))
#             # st.write("• العلاجات:", ", ".join(d["treatments"]))
#             st.markdown("---")
#         input_text += f"Possible conditions: {', '.join(diagnosis_list)}\n"
#     else:
#         st.warning("❗ لم يتم التعرف على المرض من الأعراض المدخلة.")
#         st.subheader("📝 الأعراض المتاحة في قاعدة البيانات:")
#         available_symptoms = set()
#         for disease in disease_data:
#             available_symptoms.update(disease.get("symptoms", []))
#         st.write(", ".join(available_symptoms))

#         # نص الفحص
#         if ocr_text:
#             input_text += f"Lab report or scan content: {ocr_text}\n"
            

#         # تحليل GPT
#         # (إذا أردت أن تضيف هذه الجزء مع GPT أو تدمجها بشكل آخر)
#         # response = openai.ChatCompletion.create(
#         #     model="gpt-3.5-turbo",
#         #     messages=[
#         #         {"role": "system", "content": "You are a medical assistant. Based on symptoms and lab report, provide suggestions. Always recommend a real doctor."},
#         #         {"role": "user", "content": input_text}
#         #     ]
#         # )

#         # حفظ البيانات
#         if st.button("💾 حفظ البيانات"):
#             session = Session()
#             record = UserRecord(
#                 username=username,
#                 symptoms=user_input,
#                 diagnosis=str(matched_diseases),
#                 report_text=ocr_text
#             )
#             session.add(record)
#             session.commit()
#             st.success("✅ تم حفظ بيانات المستخدم بنجاح!")
# else:
#     st.info("يرجى إدخال اسمك وبعض الأعراض أو صورة فحص للمتابعة.")








import streamlit as st
st.set_page_config(page_title="مساعد الدكتور", page_icon="🩺", layout="centered")

from main_page import main_app
# from view_records import view_records
from db import create_table


create_table()  # لإنشاء الجدول إذا مش موجود

st.sidebar.title("القائمة")
page = st.sidebar.radio("انتقل إلى:", ["الصفحة الرئيسية", "سجل المرضى"])

if page == "الصفحة الرئيسية":
    main_app()
elif page == "سجل المرضى":
    view_records()
