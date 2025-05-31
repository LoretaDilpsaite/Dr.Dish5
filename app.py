import toga
import requests

FHIR_URL = "https://hapi.fhir.org/baseR4/MedicationDispense/M14131413"

class InsulinApp(toga.App):
    def startup(self):
        main_box = toga.Box()

        self.blutzucker_input = toga.TextInput(placeholder="Blutzuckerwert")
        self.broteinheiten_input = toga.TextInput(placeholder="Broteinheiten")
        button = toga.Button("Berechnen", on_press=self.berechne_insulin)
        self.result_label = toga.Label("Insulinmenge: -- IE")

        main_box.add(self.blutzucker_input)
        main_box.add(self.broteinheiten_input)
        main_box.add(button)
        main_box.add(self.result_label)

        self.main_window = toga.MainWindow(title="InsulinCalc")
        self.main_window.content = main_box
        self.main_window.show()

    def berechne_insulin(self, widget):
        try:
            blutzucker = int(self.blutzucker_input.value)
            broteinheiten = int(self.broteinheiten_input.value)

            response = requests.get(FHIR_URL)
            data = response.json()

            insulin_dose = 0
            for entry in data["extension"][0]["extension"]:
                low = entry["extension"][0]["valueInteger"]
                high = entry["extension"][1]["valueInteger"]
                dose = int(entry["extension"][3]["valueString"].split()[0])

                if low <= blutzucker <= high:
                    insulin_dose = dose
                    break

            gesamt_insulin = insulin_dose + broteinheiten
            self.result_label.text = f"Benötigte Insulinmenge: {gesamt_insulin} IE"

        except Exception as e:
            self.result_label.text = f"Fehler: {str(e)}"

def main():
    return InsulinApp("insulin_calc", app_id="com.deinname.insulincalc")

if __name__ == "__main__":
    main().main_loop()
