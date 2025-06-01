from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///insulin_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class InsulinData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    patient_id = db.Column(db.String(20), nullable=False)
    blutzucker = db.Column(db.Float, nullable=False)
    broteinheiten = db.Column(db.Float, nullable=False)
    insulinmenge = db.Column(db.Float, nullable=False)


def berechne_insulinmenge(blutzucker, broteinheiten):
    korrekturfaktor = 1.5
    ziel_blutzucker = 100
    insulin_pro_mg = 0.1
    korrektur_insulin = (blutzucker - ziel_blutzucker) * insulin_pro_mg
    mahlzeiten_insulin = broteinheiten * korrekturfaktor
    gesamt_insulin = max(0, korrektur_insulin + mahlzeiten_insulin)
    return round(gesamt_insulin, 2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/berechne_insulin", methods=["POST"])
def berechne_insulin():
    try:
        patient_id = request.form["patient_id"]
        blutzucker = float(request.form["blutzucker"])
        broteinheiten = float(request.form["broteinheiten"])

        insulinmenge = berechne_insulinmenge(blutzucker, broteinheiten)

        # Daten in DB speichern
        eintrag = InsulinData(
            patient_id=patient_id,
            blutzucker=blutzucker,
            broteinheiten=broteinheiten,
            insulinmenge=insulinmenge
        )
        db.session.add(eintrag)
        db.session.commit()

        return jsonify({
            "patient_id": patient_id,
            "blutzucker": blutzucker,
            "broteinheiten": broteinheiten,
            "berechnete_insulinmenge": insulinmenge,
            "timestamp": eintrag.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
