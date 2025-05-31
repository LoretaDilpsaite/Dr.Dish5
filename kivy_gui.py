import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

FHIR_URL = "https://hapi.fhir.org/baseR4/MedicationDispense/M14131413"

class InsulinCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        self.blutzucker_input = TextInput(hint_text="Blutzuckerwert eingeben", multiline=False)
        self.broteinheiten_input = TextInput(hint_text="Broteinheiten eingeben", multiline=False)
        self.result_label = Label(text="Insulinmenge: -- IE")

        self.add_widget(self.blutzucker_input)
        self.add_widget(self.broteinheiten_input)
        self.add_widget(Button(text="Berechnen", on_press=self.berechne_insulin))
        self.add_widget(self.result_label)

    def berechne_insulin(self, instance):
        try:
            blutzucker = int(self.blutzucker_input.text)
            broteinheiten = int(self.broteinheiten_input.text)

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

class InsulinApp(App):
    def build(self):
        return InsulinCalculator()

if __name__ == "__main__":
    InsulinApp().run()
