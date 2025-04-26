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
# import openai

# import pandas as pd

# import os

# # تحميل المفاتيح من env
# load_dotenv()
# openai.api_key = os.getenv("OPEN_API_KEY")
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

# # st.set_page_config(page_title="سجلات المستخدمين")
# st.title("📋 عرض سجلات المستخدمين السابقة")

# # تحميل السجلات من قاعدة البيانات

# records = session.query(UserRecord).order_by(UserRecord.created_at.desc()).all()

# # تحويل السجلات إلى DataFrame لسهولة العرض
# data = [{
#     "الاسم": r.username,
#     "الأعراض": r.symptoms,
#     "التشخيص": r.diagnosis,
#     "نص الفحص": r.report_text,
#     "تاريخ الإدخال": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "غير محدد"
# } for r in records]

# df = pd.DataFrame(data)

# if not df.empty:
#     st.dataframe(df)
# else:
#     st.info("لا توجد سجلات محفوظة حالياً.")
# # واجهة Streamlit
# # st.set_page_config(page_title="مساعد الدكتور")
# def main_app():

#  st.title("🤖 مساعد الدكتور الذكي")

#  username = st.text_input("👤 أدخل اسمك")

#  user_input = st.text_input("✍️ اكتب الأعراض التي تشعر بها (بالعربية):")
#  uploaded_image = st.file_uploader("📎 أرفق صورة فحص (تحليل دم، أشعة...)", type=["jpg", "png", "jpeg"])

#  ocr_text = ""

#  if uploaded_image:
#     image = Image.open(uploaded_image)
#     ocr_text = pytesseract.image_to_string(image)
#     st.markdown("🧾 **النص المستخرج من الصورة:**")
#     st.code(ocr_text)

#  if (user_input or ocr_text) and username:
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
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a medical assistant. Based on symptoms and lab report, provide suggestions. Always recommend a real doctor."},
#                 {"role": "user", "content": input_text}
#             ]
#         )

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
#  else:
#     st.info("يرجى إدخال اسمك وبعض الأعراض أو صورة فحص للمتابعة.")
                 


import streamlit as st
import pytesseract
from PIL import Image
from dotenv import load_dotenv
from googletrans import Translator
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json
import openai
import os
import pandas as pd
# from view_records import view_records

# import os

translator = Translator()
json_path = "SymptomsOutput.json"  # الملف الذي نحفظ فيه الردود
pytesseract.pytesseract.tesseract_cmd = r"E:\Download\Tesseract\tesseract.exe"

# مترجم

# قاعدة البيانات
engine = create_engine("sqlite:///doctor_assistant.db")
Session = sessionmaker(bind=engine)
session = Session()

# استعلام كل السجلات
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()

class UserRecord(Base):
    __tablename__ = "user_records"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    symptoms = Column(Text)
    diagnosis = Column(Text)
    report_text = Column(Text)
    created_at = Column(DateTime)

# st.set_page_config(page_title="سجلات المستخدمين")
st.title("📋 عرض سجلات المستخدمين السابقة")

# تحميل السجلات من قاعدة البيانات


# تحميل الرد المخزن من الكاش
def load_cached_response(key, json_path="SymptomsOutput.json"):
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # إذا كانت البيانات قائمة، نحاول البحث عن المفتاح داخل العناصر
            if isinstance(data, list):
                # البحث في القائمة عن العنصر الذي يحتوي على المفتاح المطلوب
                for item in data:
                    if item.get('key') == key:  # تعديل هنا ليشمل المفتاح المناسب
                        return item.get('value', None)
            else:
                # إذا كانت البيانات قاموسًا، نستخدم get مباشرة
                return data.get(key, None)
        except json.JSONDecodeError:
            # إذا كان هناك خطأ في تنسيق JSON
            return None
    return None

# حفظ الرد إلى الكاش
def save_response_to_cache(key, response, json_path="SymptomsOutput.json"):
    # محاولة قراءة البيانات الحالية من الملف
    data = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # إذا كان الملف فارغًا أو يحتوي على تنسيق خاطئ، يمكن إعادة تعيين البيانات
                data = []
    
    # إضافة الرد الجديد إلى البيانات
    data.append({'key': key, 'value': response})
    
    # حفظ البيانات مرة أخرى في الملف
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




def main_app():
    st.title("📋 عرض سجلات المستخدمين السابقة")
    #    List to save the conversation
    # if "messages" not in st.session_state:
    #  st.session_state.messages = []

    #  # Display the previous conversation
    # for msg in st.session_state.messages:
    #  with st.chat_message(msg["role"]):
    #     st.markdown(msg["content"])
   
    records = session.query(UserRecord).order_by(UserRecord.created_at.desc()).all()
    data = [{
        "الاسم": r.username,
        "الأعراض": r.symptoms,
        "التشخيص": r.diagnosis,
        "نص الفحص": r.report_text,
        "تاريخ الإدخال": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "غير محدد"
    } for r in records]

    df = pd.DataFrame(data)

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("لا توجد سجلات محفوظة حالياً.")

    username = st.text_input("👤 أدخل اسمك")
    user_input = st.text_input("✍️ اكتب الأعراض التي تشعر بها (بالعربية):")
    # user_input2 = st.text_input("➕ أضف أعراض أخرى أو تفاصيل إضافية (اختياري):")
    uploaded_image = st.file_uploader("📎 أرفق صورة فحص", type=["jpg", "png", "jpeg"])
    user_input2 = st.chat_input("type your message here: ")

    ocr_text = ""
    if uploaded_image:
        image = Image.open(uploaded_image)
        ocr_text = pytesseract.image_to_string(image)
        st.markdown("🧾 **النص المستخرج من الصورة:**")
        st.code(ocr_text)

    # if user_input2:
    # # إظهار الرسالة اللي كتبها المستخدم
    #  with st.chat_message("user"):
    #      st.markdown(user_input2)

    if (user_input and user_input2 or ocr_text) and username:
        
        with st.spinner("⏳ جاري التحليل..."):
            input_text = ""
            if user_input:
                translated_input = translator.translate(user_input, src='ar', dest='en').text.lower()
                input_text += f"Patient symptoms: {translated_input}\n"
            # if user_input2:   
            #     translated_input2 = translator.translate(user_input2, src='ar', dest='en').text.lower()
            #     input_text += f"chatbot: {translated_input2}\n"
            if ocr_text:
                translated_input = translator.translate(user_input, src='ar', dest='en').text.lower()
                input_text += f"Lab report or scan content: {ocr_text}\n"

            # st.chat_message("user").markdown(f"👤🧾 {ocr_text}")

            # 🔍 تحقق من الرد في JSON
            cached = load_cached_response(input_text)
            reply = ""
            if cached:
                st.markdown("🧠 **رد محفوظ مسبقاً:**")
                st.success(cached)
                reply = cached
            else:
                # ⏳ إرسال الطلب إلى OpenAI
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "أنت مساعد طبي تحلل الأعراض وتعطي تشخيصاً أولياً."},
                            {"role": "user", "content": input_text}
                        ]
                    )
                    
                    
                    if response["choices"]:
                        reply = response["choices"][0]["message"]["content"]
                        save_response_to_cache(input_text, reply, )
                        st.markdown("🧠 **تشخيص مقترح من الذكاء الاصطناعي:**")
                        st.success(reply)
                    else:
                        st.warning("❗ لم يتم العثور على رد من الذكاء الاصطناعي.")    

                    
                except Exception as e:
                    st.error(f"❌ خطأ أثناء التواصل مع OpenAI: {e}")

            
            # 💾 حفظ البيانات
            if st.button("💾 حفظ البيانات"):
                record = UserRecord(
                    username=username,
                    symptoms=user_input,
                    diagnosis=reply if not cached else cached,
                    report_text=ocr_text
                )
                session.add(record)
                session.commit()
                st.success("✅ تم حفظ بيانات المستخدم بنجاح!")
     
    else:
        st.info("يرجى إدخال اسمك وبعض الأعراض أو صورة فحص للمتابعة.")
    # elif not user_input2:
    #  st.info("يرجى إدخال اسمك وبعض الأعراض أو صورة فحص للمتابعة.")
        
            
            


















