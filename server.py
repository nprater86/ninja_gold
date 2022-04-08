from flask import Flask, render_template, request, redirect, session
import random
import datetime

app = Flask(__name__)
app.secret_key = 'ninja_gold'

@app.route('/')
def index():
    today = datetime.datetime.now()
    date_time = today.strftime("%m/%d/%Y, %H:%M")

    if 'gold' not in session:
        session['gold'] = 0
    
    if 'message' not in session:
        session['message'] = [f'<p>Welcome to Ninja Gold! Click a location to start earning money! Collect 300 gold to win! ({date_time})</p>']

    if 'moves' not in session:
        session['moves'] = 15;
    
    print(session['moves'])
    return render_template("index.html")

@app.route('/process_money', methods=['POST'])
def process_money():
    today = datetime.datetime.now()
    date_time = today.strftime("%m/%d/%Y, %H:%M")
    session['moves'] -= 1

    if request.form['which_form'] != 'reset':
        form_string = request.form['which_form'].split(",")
        multiplier = random.randint(int(form_string[0]),int(form_string[1]))
        session['gold'] += multiplier

        if multiplier > 0:
            gain = 'earns'
            color = 'green'
        elif multiplier < 0:
            gain = 'loses'
            color = 'red'
        else:
            gain = 'breaks even with'
            color = 'black'

        session['message'].append(f'<p class="{color}">Ninja enters the {form_string[2]} and {gain} {multiplier} gold! ({date_time})</p>')

    if session['moves'] == 0:
        if session['gold'] >= 300:
            session['message'].append(f'<p>You win! Play again? ({date_time})</p>')
        else:
            session['message'].append(f'<p>You lose! Play again? ({date_time})</p>')

    if request.form['which_form'] == 'reset':
        session.pop('gold')
        session.pop('moves')
        session['message'].append(f'<p>Game has been reset! Collect 300 gold to win! ({date_time})</p>')

    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)