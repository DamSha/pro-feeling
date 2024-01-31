from flask import *
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['pro-feeling']
interviews_collection = db['interviews']
agents_collection = db['agents']
personnes_collection = db['personnes']
utilisateurs_collection = db['utilisateurs']

@app.route('/')
def index():
    interviews = interviews_collection.find()
    agents = agents_collection.find()
    personnes = personnes_collection.find()
    return render_template('index.html', interviews=interviews, agents=agents, personnes=personnes)

#Création d'interview
@app.route("/creationInterview/<agent_id>//<personne_id>", methods=['GET', 'POST'])
def creation(agent_id, personne_id):
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        id_agent = agent_id
        id_personne = personne_id

         # Récupération de l'agent et de la personne
        personne = personnes_collection.find_one({'_id': ObjectId(id_personne)})
        agent = agents_collection.find_one({'_id': ObjectId(id_agent)})

        if personne and agent:
            nouvel_interview = {'date': date, 'description': description, 'agent': agent, 'personne': personne}
            interviews_collection.insert_one(nouvel_interview)
            return redirect(url_for('index'))
        else:
            print("La personne ou l'agent n'existe pas.")
        return redirect(url_for('creationInterview', agent_id=agent_id, personne_id=personne_id))
    return render_template('creationInterview.html', agent_id=agent_id, personne_id=personne_id)

#Création des agentq
@app.route("/creationAgent", methods=['GET', 'POST'])
def creationAgent():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        genre = request.form['genre']
        specialite = request.form['specialite']
        
        nouvel_agent = {'nom': nom, 'prenom': prenom, 'genre': genre, 'specialite': specialite}
        agents_collection.insert_one(nouvel_agent)
        
        return redirect(url_for('index'))

    return render_template('creationAgent.html')

#Création des personnes
@app.route("/creationPersonne", methods=['GET', 'POST'])
def creationPersonne():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        genre = request.form['genre']
        casier = request.form['casier']
        antecedents = request.form['antecedents']
        description = request.form['description']
        consentement = request.form['consentement']

        nouvel_personne = {'nom': nom, 'prenom': prenom, 'genre': genre, 'casier': casier, 'antecedents': antecedents, 'description': description, 'consentement': consentement }
        agents_collection.insert_one(nouvel_personne)
        
        return redirect(url_for('index'))

    return render_template('creationPersonne.html')

#Connexion
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        utilisateur = next((user for user in utilisateurs_collection if user['username'] == username), None)

        if utilisateur and utilisateur['password'] == password:
            
            return redirect(url_for('index'))
        else:
            print("Nom d'utilisateur ou mot de passe incorrect")
            return redirect(url_for('connexion'))

    return render_template('connexion.html')


if __name__ == '__main__':
    app.run(debug=True)
