from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import func

app = Flask(__name__)

# ตั้งค่าฐานข้อมูล SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# สร้าง instance ของ SQLAlchemy
db = SQLAlchemy(app)

# สร้าง Model สำหรับการเก็บข้อมูล "วันที่" และ "ค่าที่ต้องการเก็บ"
class DataRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)

# สร้างตารางในฐานข้อมูล (ครั้งแรก)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    dater = date.today()
    records = DataRecord.query.all() # ดึงข้อมูลทั้งหมดจากฐานข้อมูล
    return render_template('index.html', records=records,dater =dater)

@app.route('/record')
def record():
    goal = 1000
    dater = date.today()
    records = DataRecord.query.all()  # ดึงข้อมูลทั้งหมดจากฐานข้อมูล
    total_value = db.session.query(func.sum(DataRecord.value)).scalar()
    left = goal-total_value
    return render_template('record.html',goal=goal, records=records,dater =dater,total_value=total_value,left=left)

@app.route('/add_record', methods=['POST'])
def add_record():
    value = float(request.form.get('value'))  # รับค่าจากฟอร์ม
    dater = date.today()  # รับวันที่จากฟอร์มและแปลงเป็น datetime object
    new_record = DataRecord(date=dater, value=value)
    db.session.add(new_record)  # เพิ่มข้อมูลใหม่เข้าไปในฐานข้อมูล
    db.session.commit()  # บันทึกการเปลี่ยนแปลงในฐานข้อมูล
    return redirect(url_for('index'))

# ฟังก์ชันลบ record
@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    record = DataRecord.query.get_or_404(record_id)  # ค้นหา record โดยใช้ id
    db.session.delete(record)  # ลบ record ออกจากฐานข้อมูล
    db.session.commit()  # บันทึกการเปลี่ยนแปลงลงฐานข้อมูล
    return redirect(url_for('record'))  # กลับไปยังหน้าแรกหรือหน้าอื่น

if __name__ == '__main__':
    app.run(debug=True)
