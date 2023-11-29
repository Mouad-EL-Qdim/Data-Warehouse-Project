import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('/home/moad/Downloads/Pdf/Source Database Sales History/Database/Product.csv')

# Supprimer les colonnes indésirables
columns_to_keep = ['id', 'categ_id', 'price', 'active', 'name', 'quantity_per_package', 'quantity_per_pallet']
df = df[columns_to_keep]

# Convertir les colonnes en float
df['price'] = df['price'].astype(float)
df['quantity_per_package'] = df['quantity_per_package'].astype(float)
df['quantity_per_pallet'] = df['quantity_per_pallet'].astype(float)

# Supprimer les lignes contenant des valeurs nulles
df = df.dropna()

# Enregistrer le nouveau fichier CSV
df.to_csv('Product_modified.csv', index=False)
