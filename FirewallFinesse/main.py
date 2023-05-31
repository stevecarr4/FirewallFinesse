import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')  # Load configuration from file

db = SQLAlchemy(app)

class AttackPattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attack_pattern = db.Column(db.String(100), unique=True, nullable=False)
    rule_template = db.Column(db.String(500), nullable=False)

initialized = False

@app.before_request
def initialize():
    global initialized
    if not initialized:
        db.create_all()
        initialized = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attack-patterns', methods=['GET', 'POST'])
def attack_patterns():
    if request.method == 'POST':
        attack_pattern = request.form.get('attack_pattern')
        rule_template = request.form.get('rule_template')
        try:
            new_attack_pattern = AttackPattern(attack_pattern=attack_pattern, rule_template=rule_template)
            db.session.add(new_attack_pattern)
            db.session.commit()
            flash('Attack pattern added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the attack pattern.', 'danger')
        return redirect(url_for('attack_patterns'))
    else:
        all_attack_patterns = AttackPattern.query.all()
        return render_template('attack_patterns.html', attack_patterns=all_attack_patterns)

# Add more routes...

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('firewall_finesse.log'),
            logging.StreamHandler()
        ]
    )
    app.run(debug=True)
