from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize GPU availability
gpus = [{'id': i, 'availability': {}} for i in range(1, 9)]

@app.route('/')
def index():
    return render_template('index.html', gpus=gpus)

@app.route('/book', methods=['POST'])
def book():
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    booker_name = request.form['booker_name']
    purpose = request.form['purpose']
    selected_gpus = request.form.getlist('gpu_ids')
    from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
    to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
    
    for gpu_id in selected_gpus:
        gpu_id = int(gpu_id)
        for gpu in gpus:
            if gpu['id'] == gpu_id:
                current_date = from_date_obj
                while current_date <= to_date_obj:
                    date_str = current_date.strftime('%Y-%m-%d')
                    if date_str not in gpu['availability']:
                        gpu['availability'][date_str] = {'available': True, 'booker': None, 'purpose': None}
                    if gpu['availability'][date_str]['available']:
                        gpu['availability'][date_str] = {'available': False, 'booker': booker_name, 'purpose': purpose}
                    current_date += timedelta(days=1)
                break
    return redirect(url_for('index'))

@app.route('/status')
def status():
    return render_template('status.html', gpus=gpus)

if __name__ == '__main__':
    app.run(debug=True)