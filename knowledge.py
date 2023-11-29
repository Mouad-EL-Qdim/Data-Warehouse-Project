import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn import tree


# Paramètres de connexion à la base de données
db_host = 'localhost'
db_port = 3306
db_name = 'DW_OutPut'
db_user = 'root'
db_password = ''

# Connexion à la base de données
conn = mysql.connector.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)

# Création du curseur pour exécuter les requêtes SQL
cur = conn.cursor()

# Requête SQL pour récupérer les données nécessaires pour le modèle
query = '''
SELECT
    Product.price,
    Product.active,
    Product.categ_id,
    Country._name AS country,
    CASE
        WHEN Invoice.amount_total > 1000 THEN 1
        ELSE 0
    END AS high_value
FROM
    Invoice
    JOIN `Invoice Line` ON Invoice.id = `Invoice Line`.invoice_id
    JOIN Product ON `Invoice Line`.product_id = Product.id
    JOIN Partner ON Invoice.partner_id = Partner.id
    JOIN Country ON Partner.country_id = Country._id
'''

# Exécution de la requête SQL
cur.execute(query)


# Récupération des résultats
results = cur.fetchall()

# Fermeture du curseur et de la connexion à la base de données
cur.close()
conn.close()

# Création d'un DataFrame à partir des résultats
columns = ['price', 'active', 'category', 'country', 'high_value']
data = pd.DataFrame(results, columns=columns)

# Conversion des variables catégoriques en variables indicatrices (one-hot encoding)
data = pd.get_dummies(data, columns=['category', 'country'])

# Séparation des données en variables indépendantes (X) et variable cible (y)
X = data.drop('high_value', axis=1)
y = data['high_value']

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création du modèle d'arbre de décision
model = DecisionTreeClassifier()

# Entraînement du modèle sur les données d'entraînement
model.fit(X_train, y_train)

# Prédiction sur les données de test
y_pred = model.predict(X_test)

# Création de la matrice de confusion
confusion = confusion_matrix(y_test, y_pred)

# Affichage de la matrice de confusion
print('Confusion Matrix:')
print(confusion)

# Générer l'arbre de décision
class_names = ['0', '1']  # Update with appropriate class labels
feature_names = X_train.columns.astype(str)
tree.export_graphviz(model, out_file='treeDT.dot', feature_names=feature_names, class_names=class_names)
