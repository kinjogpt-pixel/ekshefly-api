import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
# استيراد الدالة التي تقيم الصورة من ملف زميلتك
from predict_utils import predict_damage 

app = Flask(__name__)
UPLOAD_FOLDER = 'raw_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/evaluate', methods=['POST'])
def evaluate_building():
    if 'image' not in request.files:
        return jsonify({"error": "لم يتم إرسال صورة"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "لم يتم اختيار صورة"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # ---------------------------------------------------------
    # استدعاء الموديل الفعلي لتقييم الصورة
    try:
        # نفترض أن الدالة تعيد النص مباشرة (مثلاً: "خطر")
        damage_level = predict_damage(filepath) 
    except Exception as e:
        print(f"Error during prediction: {e}")
        damage_level = "حدث خطأ أثناء التقييم"
    # ---------------------------------------------------------

    return jsonify({
        "damageLevel": damage_level,
        "message": "تم التقييم بنجاح عبر CNN على Render"
    })

if __name__ == '__main__':
    # لا يهم هنا المنفذ أو الهوست، لأن Gunicorn سيتولى التشغيل في Render
    app.run(debug=False)
