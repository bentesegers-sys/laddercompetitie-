from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Een geheime sleutel is nodig om gegevens tijdelijk op te slaan in de browser (sessies)
app.secret_key = 'supergeheim_sparkx_sleutel'

class LadderCompetitie:
    def __init__(self, spelers_lijst):
        self.spelers = spelers_lijst

    def speler_toevoegen(self, naam):
        if naam and naam not in self.spelers:
            self.spelers.append(naam)
            return f"Speler {naam} is toegevoegd."
        return "Naam is leeg of bestaat al."

    def wissel_spelers(self, naam1, naam2):
        if naam1 not in self.spelers or naam2 not in self.spelers:
            return "Een of beide namen bestaan niet."
        
        i1 = self.spelers.index(naam1)
        i2 = self.spelers.index(naam2)
        self.spelers[i1], self.spelers[i2] = self.spelers[i2], self.spelers[i1]
        return f"{naam1} en {naam2} zijn succesvol gewisseld."

@app.route('/', methods=['GET', 'POST'])
def home():
    # Zorg dat er altijd een lijst met spelers in de sessie staat
    if 'spelers' not in session:
        session['spelers'] = []
    
    # Laad de huidige laddercompetitie in met de opgeslagen spelers
    ladder = LadderCompetitie(session['spelers'])
    melding = None

    if request.method == 'POST':
        actie = request.form.get('actie')

        if actie == 'toevoegen':
            naam = request.form.get('naam')
            melding = ladder.speler_toevoegen(naam)
            session.modified = True  # Vertel Flask dat de lijst is aangepast

        elif actie == 'wisselen':
            naam1 = request.form.get('naam1')
            naam2 = request.form.get('naam2')
            melding = ladder.wissel_spelers(naam1, naam2)
            session.modified = True

        elif actie == 'wissen':
            session['spelers'] = []
            return redirect(url_for('home'))

    return render_template('index.html', spelers=ladder.spelers, melding=melding)

if __name__ == '__main__':
    app.run(debug=True)
