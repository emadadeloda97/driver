import time
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'sandra'   
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        a = request.form.get('username')
        b = request.form.get('password')
        if a and b:
            flash(f'Welcome {a}!', 'success')
        return redirect(url_for('home'))
    return render_template('flash.html')




if __name__ == '__main__':
    app.run(debug=True)