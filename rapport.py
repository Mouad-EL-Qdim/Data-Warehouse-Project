from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import mysql.connector
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Utilisez un backend GUI approprié, comme TkAgg


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

# Requête SQL pour récupérer le pourcentage de produits achetés par année
query = '''
SELECT
    month,
    COUNT(*) AS total_products,
    (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()) AS percentage
FROM
    Invoice
    JOIN `Invoice Line` ON Invoice.id = `Invoice Line`.invoice_id
    JOIN Product ON `Invoice Line`.product_id = Product.id
GROUP BY
    month
ORDER BY
    month
'''

# Exécution de la requête SQL
cur.execute(query)

# Récupération des résultats
results = cur.fetchall()

# Fermeture du curseur et de la connexion à la base de données
cur.close()
conn.close()

# Chemin vers le fichier de rapport (.html)
report_path = 'rapport.html'

# Création de l'environnement Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('report_template.html')

# Génération du rapport HTML en utilisant le template Jinja2 et les résultats de la requête
html = template.render(results=results)

# Enregistrement du rapport HTML
with open(report_path, 'w') as file:
    file.write(html)

# Conversion du rapport HTML en PDF en utilisant WeasyPrint
output_path = 'rapport.pdf'
HTML(report_path).write_pdf(output_path)

# Récupération des années et des pourcentages depuis les résultats de la requête
years = [result[0] for result in results]
percentages = [result[2] for result in results]

# Création du graphique à barres
plt.bar(years, percentages)
plt.xlabel('month')
plt.ylabel('Percentage')
plt.title('Percentage of Products Purchased by month')

# Affichage du graphique
plt.show()
