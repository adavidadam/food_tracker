from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import datetime

app = Flask(__name__)

# Path to your CSV file
CSV_FILE = 'daily_data.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        date = request.form['date']
        foods = request.form['foods']
        recovery_score = request.form['recovery_score']
        felt_tired = request.form['felt_tired']

        # Validate inputs
        if not date:
            date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if not recovery_score.isdigit():
            return "Recovery score must be a number.", 400

        # Load or create CSV
        file_exists = os.path.exists(CSV_FILE)
        df = pd.read_csv(CSV_FILE) if file_exists else pd.DataFrame(columns=['Date', 'Foods', 'RecoveryScore', 'FeltTired'])

        # Check if entry exists
        if date in df['Date'].values:
            df.loc[df['Date'] == date, ['Foods', 'RecoveryScore', 'FeltTired']] = [foods, recovery_score, felt_tired]
        else:
            df = pd.concat([df, pd.DataFrame([[date, foods, recovery_score, felt_tired]],
                                             columns=['Date', 'Foods', 'RecoveryScore', 'FeltTired'])], ignore_index=True)

        # Save back to CSV
        df.to_csv(CSV_FILE, index=False)
        return redirect('/')

    # Display the form
    return render_template('index.html')

@app.route('/data')
def view_data():
    if not os.path.exists(CSV_FILE):
        return "No data available."

    # Load and display data
    df = pd.read_csv(CSV_FILE)
    return df.to_html(index=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT variable or default to 5000
    app.run(host='0.0.0.0', port=port)  # Bind to 0.0.0.0 to be externally accessible

