from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Memastikan path absolut untuk loading model Hugging Face
base_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(base_dir, 'models')

load_error_str = ""
try:
    svm_depresi = joblib.load(os.path.join(models_dir, 'svm_model_depresi.pkl'))
    svm_kecemasan = joblib.load(os.path.join(models_dir, 'svm_model_kecemasan.pkl'))
    svm_stres = joblib.load(os.path.join(models_dir, 'svm_model_stres.pkl'))
    scaler = joblib.load(os.path.join(models_dir, 'svm_scaler.pkl'))
    models_loaded = True
except Exception as e:
    import traceback
    load_error_str = traceback.format_exc()
    print(f"Error loading models:\n{load_error_str}")
    models_loaded = False

# Roasting Dictionary Mapping (Gen-Z Style based on Severity 0-4)
ROAST_DEPRESI = {
    0: "Hidup kamu terlihat cukup tenang. Bersyukur ya, sepertinya tidak ada beban yang terlalu berat saat ini.",
    1: "Sepertinya kamu lagi agak overthinking sedikit. Kurang-kurangi melamun yang tidak perlu, ya.",
    2: "Wah, sepertinya kamu lagi sering dengar playlist galau nih. Jangan lupa luangkan waktu untuk istirahat sejenak.",
    3: "Halo, kalau kamu merasa pikiran sedang berat, jangan dipendam sendiri. Yuk, coba cerita ke orang terdekat!",
    4: "Perhatian sebentar! Pikiran kamu sepertinya butuh pertolongan. Jangan ragu buat ngobrol sama psikolog, kamu nggak sendirian kok."
}

ROAST_KECEMASAN = {
    0: "Santai banget nih. Sepertinya kamu bisa menghadapi hari-hari dengan sangat tenang.",
    1: "Ada sedikit rasa gugup saat menghadapi momen penting. Tenang saja, itu hal yang sangat wajar kok.",
    2: "Sepertinya kamu mulai sering merasa khawatir soal masa depan. Coba tarik napas dalam-dalam dan fokus pada hari ini ya.",
    3: "Kamu sepertinya terlalu sering memikirkan hal-hal yang belum terjadi. Coba tenangkan diri, jangan buat dirimu capek karena pikiran sendiri.",
    4: "Kondisi kamu sepertinya sedang sangat waspada terus-menerus. Coba istirahat, jauhkan gadget sebentar, dan cari ketenangan yang kamu butuhkan."
}

ROAST_STRES = {
    0: "Bebas stres! Kamu sepertinya pintar mengelola tekanan dan tidak terlalu memusingkan omongan orang.",
    1: "Beban tugas atau kerjaan sepertinya mulai mengganggu waktu tidur kamu. Kurangi konsumsi kafein malam-malam ya.",
    2: "Kamu sepertinya sudah mulai sering lelah. Mungkin ini saatnya ambil waktu luang untuk liburan singkat.",
    3: "Tingkat stres kamu agak tinggi nih, sedikit masalah saja sepertinya bisa memancing emosimu. Yuk, tenangkan pikiran dulu.",
    4: "Pikiran kamu sepertinya sudah sangat kelelahan. Kamu butuh waktu luang sejenak untuk memulihkan energi dari hiruk pikuk rutinitas."
}

def generate_pixel_character(dep_score, anx_score, str_score):
    avg_score = (dep_score + anx_score + str_score) / 3
    
    # Karakter Minuman dengan Tema Warna Spesifik
    if avg_score < 1:
        return {
            "name": "Air Mineral", 
            "tags": ["#StayHydrated", "#ZenMode"],
            "quote": '"Jernih, tenang, dan selalu menyegarkan."',
            "bg_color": "#D3E9F8",      # Diubah agar match background gambar AI
            "theme_color": "#5B96B7",
            "img": "air_mineral.jpeg"
        }
    elif avg_score < 2:
        return {
            "name": "Matcha Latte", 
            "tags": ["#Overthinker", "#Aesthetic"],
            "quote": '"Kelihatan tenang di luar, tapi lumayan rumit di dalam."',
            "bg_color": "#BAD3BA",      # Diubah agar match background gambar AI
            "theme_color": "#769A63",
            "img": "matcha_latte.jpeg"
        }
    elif avg_score < 3:
        return {
            "name": "Kopi Hitam", 
            "tags": ["#NeedCoffee", "#DeadlineHustle"],
            "quote": '"Pahitnya pas, sekeras realita hari ini."',
            "bg_color": "#E9D2C0",      # Diubah agar match background gambar AI
            "theme_color": "#B57A59",
            "img": "kopi_hitam.jpeg"
        }
    else:
        return {
            "name": "Energy Drink", 
            "tags": ["#LowBattery", "#SurvivalMode"],
            "quote": '"Lagi push limit banget nih, awas meledak!"',
            "bg_color": "#E1CAEE",      # Diubah agar match background gambar AI
            "theme_color": "#8B70A6",
            "img": "energy_drink.jpeg"
        }

def calculate_digital_activity(X_input):
    score = 0
    # 1. Durasi Smartphone
    if X_input[2] > 7: score += 2
    elif X_input[2] >= 4: score += 1
    
    # 2. Durasi Medsos
    if X_input[3] > 6: score += 2
    elif X_input[3] >= 3: score += 1
        
    # 3. Durasi Game
    if X_input[4] > 4: score += 2
    elif X_input[4] >= 2: score += 1
        
    # 4. Durasi Streaming
    if X_input[5] > 4: score += 2
    elif X_input[5] >= 2: score += 1
    
    # 5. Gadget sblm tidur
    if X_input[6] == 1: score += 1
        
    # 6. Terganggu Notif
    score += X_input[7]
        
    # 7. Cemas Tanpa Internet
    if X_input[8] == 1: score += 1
        
    # 8. Menunda Tugas
    if X_input[9] == 1: score += 1
    
    # 9. Waktu Tidur (Kurang tidur)
    if X_input[10] <= 4: score += 2
    elif X_input[10] <= 6: score += 1
        
    # 10. Doom Scrolling
    score += X_input[12]
        
    # 11. Cek HP
    if X_input[11] > 6: score += 2
    elif X_input[11] >= 3: score += 1
        
    # Platform Medsos adalah pertanyaan aktivitas digital ke-12 (Teks), tidak masuk ke skor kuantitatif
        
    if score <= 7: return "Sehat"
    elif score <= 13: return "Sedang"
    else: return "Tinggi"

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/form')
def form():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not models_loaded:
        return f"Models not loaded on server. Please check backend. Load Error:<br><pre>{load_error_str}</pre>", 500

    try:
        # Extract features from form
        frm = request.form
        
        # A. Fitur Aktivitas Digital (13 fitur)
        X_input = [
            float(frm.get('Usia', 20)),
            int(frm.get('Jenis_Kelamin', 0)), # 0 Laki, 1 Perempuan
            float(frm.get('Durasi_Smartphone', 5)),
            float(frm.get('Durasi_Medsos', 3)),
            float(frm.get('Durasi_Game', 0)),
            float(frm.get('Durasi_Streaming', 1)),
            int(frm.get('Gadget_Sblm_Tidur', 0)),
            int(frm.get('Terganggu_Notif', 1)),
            int(frm.get('Cemas_Tanpa_Internet', 0)),
            int(frm.get('Menunda_Tugas', 0)),
            float(frm.get('Waktu_Tidur', 7.0)),
            int(frm.get('Cek_HP_Tanpa_Notif', 2)),
            int(frm.get('Doom_Scrolling', 2))
        ]
        
        # B. Fitur DASS-21 (21 fitur dari kuesioner psikologis)
        dass_input = [int(frm.get(f'DASS_{i}', 0)) for i in range(1, 22)]
        
        # Gabungkan semua input
        all_input = X_input + dass_input
        
        feature_names = [
            "Usia", "Jenis_Kelamin", "Durasi_Smartphone", "Durasi_Medsos", 
            "Durasi_Game", "Durasi_Streaming", "Gadget_Sblm_Tidur",
            "Terganggu_Notif", "Cemas_Tanpa_Internet", "Menunda_Tugas",
            "Waktu_Tidur", "Cek_HP_Tanpa_Notif", "Doom_Scrolling"
        ] + [f"DASS_{i}" for i in range(1, 22)]
        
        import pandas as pd
        X_df = pd.DataFrame([all_input], columns=feature_names)
        
        # Feature Engineering (harus sama persis dengan pipeline training)
        X_df['Total_Screen_Time'] = X_df['Durasi_Smartphone'] + X_df['Durasi_Medsos'] + X_df['Durasi_Game'] + X_df['Durasi_Streaming']
        X_df['Digital_Dependency'] = X_df['Gadget_Sblm_Tidur'] + X_df['Cemas_Tanpa_Internet'] + X_df['Menunda_Tugas'] + X_df['Terganggu_Notif']
        
        # Scale Input
        X_scaled = scaler.transform(X_df)
        
        # Predict 0-4
        dep_pred = int(svm_depresi.predict(X_scaled)[0])
        anx_pred = int(svm_kecemasan.predict(X_scaled)[0])
        str_pred = int(svm_stres.predict(X_scaled)[0])
        
        # Gen-Z Roasting Profile Generation
        bento_character_profile = generate_pixel_character(dep_pred, anx_pred, str_pred)
        
        # Labels for 0-4
        severity_labels = {
            0: "Normal",
            1: "Ringan",
            2: "Sedang",
            3: "Parah",
            4: "Sangat Parah"
        }
        dep_label = severity_labels.get(dep_pred, "Normal")
        anx_label = severity_labels.get(anx_pred, "Normal")
        str_label = severity_labels.get(str_pred, "Normal")
        
        digital_activity_label = calculate_digital_activity(X_input)
        
        roast_texts = {
            'depresi': ROAST_DEPRESI.get(dep_pred, ""),
            'kecemasan': ROAST_KECEMASAN.get(anx_pred, ""),
            'stres': ROAST_STRES.get(str_pred, "")
        }
        
        # Additional single roast box for extreme behavior
        bad_habits_roast = "Screen time kamu tergolong wajar kok. Lanjutkan aktivitas harian normalmu ya."
        if X_input[3] > 6:
            bad_habits_roast = "Waktu medsos kamu tembus " + str(int(X_input[3])) + " jam sehari... pantas jadi capek mikir, yuk kurangi sedikit kebiasaan scroll-nya."
        elif X_input[8] == 1 and X_input[9] == 1:
            bad_habits_roast = "Sering takut tertinggal tren (FOMO) dan menunda pekerjaan. Coba perlahan atur prioritas ya biar hidup lebih tertata."
            
        return render_template('result.html', 
                               dep=dep_pred, anx=anx_pred, strs=str_pred,
                               dep_label=dep_label, anx_label=anx_label, str_label=str_label,
                               roast=roast_texts,
                               character=bento_character_profile,
                               bad_habits=bad_habits_roast,
                               digital_activity=digital_activity_label)

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Prediction Error: {error_msg}")
        return f"Error Occured: {e}<br><pre>{error_msg}</pre>", 500

if __name__ == '__main__':
    # Server configuration for Hugging Face Docker Space
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
