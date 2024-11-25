from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
db = SQLAlchemy(app)

# Define database models
class GPU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookings = db.relationship('Booking', backref='gpu', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    booker_name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(200), nullable=False)

# Initialize the database and GPUs
with app.app_context():
    db.create_all()
    if not GPU.query.first():
        for i in range(1, 9):
            gpu = GPU(id=i)
            db.session.add(gpu)
        db.session.commit()

@app.route('/')
def index():
    gpus = GPU.query.all()
    return render_template('index.html', gpus=gpus)

@app.route('/book', methods=['POST'])
def book():
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    booker_name = request.form['booker_name']
    purpose = request.form['purpose']
    selected_gpus = request.form.getlist('gpu_ids')
    from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
    
    for gpu_id in selected_gpus:
        current_date = from_date_obj
        while current_date <= to_date_obj:
            existing_booking = Booking.query.filter_by(gpu_id=gpu_id, date=current_date).first()
            if not existing_booking:
                booking = Booking(
                    gpu_id=gpu_id,
                    date=current_date,
                    booker_name=booker_name,
                    purpose=purpose
                )
                db.session.add(booking)
            current_date += timedelta(days=1)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/status')
def status():
    month_offset = int(request.args.get('month_offset', 0))
    current_date = datetime.utcnow().replace(day=1)
    target_month = current_date.month + month_offset
    target_year = current_date.year + (target_month - 1) // 12
    target_month = (target_month - 1) % 12 + 1
    start_date = datetime(target_year, target_month, 1)
    next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
    days_in_month = (next_month - start_date).days
    gpus = GPU.query.all()
    end_date = start_date + timedelta(days=days_in_month)
    bookings = Booking.query.filter(Booking.date >= start_date, Booking.date < end_date).all()
    # Organize bookings by date and GPU ID
    bookings_dict = {}
    for booking in bookings:
        bookings_dict.setdefault(booking.date, {})[booking.gpu_id] = booking
    return render_template(
        'status.html',
        gpus=gpus,
        bookings=bookings_dict,
        start_date=start_date,
        days_in_month=days_in_month,
        month_offset=month_offset,
        timedelta=timedelta  # Add this line
    )

@app.route('/manage_bookings')
def manage_bookings():
    month_offset = int(request.args.get('month_offset', 0))
    current_date = datetime.utcnow().replace(day=1)
    target_month = current_date.month + month_offset
    target_year = current_date.year + (target_month - 1) // 12
    target_month = (target_month - 1) % 12 + 1
    start_date = datetime(target_year, target_month, 1)
    next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
    days_in_month = (next_month - start_date).days
    gpus = GPU.query.all()
    end_date = start_date + timedelta(days=days_in_month)
    bookings = Booking.query.filter(Booking.date >= start_date, Booking.date < end_date).all()
    # Organize bookings by date and GPU ID
    bookings_dict = {}
    for booking in bookings:
        bookings_dict.setdefault(booking.date, {})[booking.gpu_id] = booking
    return render_template(
        'manage_bookings.html',
        gpus=gpus,
        bookings=bookings_dict,
        start_date=start_date,
        days_in_month=days_in_month,
        month_offset=month_offset,
        timedelta=timedelta
    )

@app.route('/free_booking', methods=['POST'])
def free_booking():
    booking_id = request.form['booking_id']
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
    return redirect(url_for('manage_bookings', month_offset=request.form.get('month_offset', 0)))

if __name__ == '__main__':
    app.run(debug=True)