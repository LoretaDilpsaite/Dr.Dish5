from flask import Flask, jsonify
import requests

app = Flask(__name__)
FHIR_URL = "https://hapi.fhir.org/baseR4/MedicationDispense/M14131413"

def berechne_insulinmenge(be: float, faktor: float = 1.0) -> float:
    return be * faktor

def hole_medikation_daten():
    try:
        response = requests.get(FHIR_URL)
        response.raise_for_status()
        data = response.json()

        dosage_instruction = data.get("dosageInstruction", [{}])[0]
        dose_quantity = dosage_instruction.get("doseAndRate", [{}])[0].get("doseQuantity", {})

        be_menge = float(dose_quantity.get("value", 0))
        einheit = dose_quantity.get("unit", "unbekannt")

        return be_menge, einheit
    except Exception as e:
        return None, str(e)

@app.route("/insulin", methods=["GET"])
def insulin_route():
    be, einheit = hole_medikation_daten()
    if be is None:
        return jsonify({"error": einheit}), 500

    insulin = berechne_insulinmenge(be)
    return jsonify({
        "brot_einheiten": be,
        "einheit": einheit,
        "insulinmenge": insulin
    })

if __name__ == "__main__":
    app.run(debug=True)
