from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Bağlantısı (Şifreni güncellemeyi unutma!)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ahm@selen0601", 
        database="spor_takip_db"
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Antrenmanları çekelim
    cursor.execute("SELECT * FROM workouts ORDER BY workout_date ASC")
    workouts = cursor.fetchall()
    
    # HTML'deki grafik kodumuz bu isimleri bekliyor:
    workout_dates = [str(w['workout_date']) for w in workouts]
    workout_weights = [float(w['weight']) for w in workouts]
    
    cursor.close()
    db.close()
    
    # Buradaki isimleri HTML ile eşitledik:
    return render_template('index.html', 
                           workouts=workouts, 
                           workout_dates=workout_dates, 
                           workout_weights=workout_weights)

@app.route('/add', methods=['POST'])
def add_workout():
    # Formdan gelen verileri alalım
    exercise_name = request.form['exercise_name']
    weight = request.form['weight']
    sets = request.form['sets']
    reps = request.form['reps']
    workout_date = request.form['workout_date']

    # Veritabanına kaydedelim
    db = get_db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO workouts (exercise_name, weight, sets, reps, workout_date) VALUES (%s, %s, %s, %s, %s)"
    val = (exercise_name, weight, sets, reps, workout_date)
    cursor.execute(sql, val)
    db.commit() # Değişikliği kaydet
    
    cursor.close()
    db.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)