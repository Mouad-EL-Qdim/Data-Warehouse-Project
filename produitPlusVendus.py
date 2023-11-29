import matplotlib.pyplot as plt
import mysql.connector

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

# Requête SQL pour récupérer les données sur les produits les plus vendus
query = '''
SELECT
    Product.name AS ProductName,
    COUNT(*) AS total_sales
FROM
    Invoice
    JOIN `Invoice Line` ON Invoice.id = `Invoice Line`.invoice_id
    JOIN Product ON `Invoice Line`.product_id = Product.id
GROUP BY
    Product.name
ORDER BY
    total_sales DESC
LIMIT 10
'''

# Exécution de la requête SQL
cur.execute(query)

# Récupération des résultats
results = cur.fetchall()

# Fermeture du curseur et de la connexion à la base de données
cur.close()
conn.close()

# Récupération des noms de produits et des quantités de ventes depuis les résultats de la requête
product_names = [result[0] for result in results]
total_sales = [result[1] for result in results]

# Création du graphique à barres horizontales
plt.barh(product_names, total_sales)
plt.xlabel('Total Sales')
plt.ylabel('Product Name')
plt.title('Top 10 Best Selling Products')

# Affichage du graphique
plt.show()

#Création du graphique à cercle (camembert) pour afficher le pourcentage des produits vendus
plt.pie(total_sales, labels=product_names, autopct='%1.1f%%')
plt.title('Percentage of Best Selling Products')

#Affichage du graphique à cercle
plt.show()