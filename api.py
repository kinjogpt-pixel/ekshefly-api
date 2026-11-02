import os
import random
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'raw_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/evaluate', methods=['POST'])
def evaluate_building():
    print("\n--- 🌐 تم استلام طلب جديد من التطبيق ---") # رسالة مراقبة في التيرمنال
    
    if 'image' not in request.files:
        print("❌ خطأ: لم يتم إرسال أي صورة في الطلب.")
        return jsonify({"error": "لم يتم إرسال صورة"}), 400
    
    file = request.files['image']
    lat = request.form.get('latitude', 'غير محدد')
    lng = request.form.get('longitude', 'غير محدد')
    
    if file.filename == '':
        print("❌ خطأ: الملف المرفق فارغ.")
        return jsonify({"error": "لم يتم اختيار صورة"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"✅ تم حفظ الصورة بنجاح في: {filepath}")
    print(f"📍 الإحداثيات المستلمة: خط العرض {lat}، خط الطول {lng}")

    # ---------------------------------------------------------
    # لمحاكاة الرد الفعلي من الـ CNN والتأكد من تغير النتائج
    # (لاحقاً ستستبدل هذا باستدعاء دالة predict_damage)
    # ---------------------------------------------------------
    file_size_kb = os.path.getsize(filepath) / 1024
    if file_size_kb < 100:
        damage_level = "سليم (لا يوجد أضرار ظاهرة)"
    elif 100 <= file_size_kb < 500:
        damage_level = "متوسط (أضرار طفيفة، يتطلب مراجعة)"
    else:
        damage_level = "خطر (بحاجة لتدخل هندسي فوري)"
    
    print(f"🤖 نتيجة تقييم الذكاء الاصطناعي: {damage_level}")
    print("------------------------------------------\n")

    return jsonify({
        "damageLevel": damage_level,
        "message": "تم التقييم بنجاح"
    })

if __name__ == '__main__':
    # تأكد من أن الـ IP الخاص بك مطبوع هنا عند التشغيل
    app.run(host='0.0.0.0', port=5000, debug=True)
