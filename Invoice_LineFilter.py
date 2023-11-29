import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('/home/moad/Downloads/Pdf/Source Database Sales History/Database/Invoice Line.csv')

# Supprimer les colonnes indésirables
columns_to_keep = ['id', 'origin', 'invoice_id', 'price_unit', 'product_id', 'quantity', 'price_total']
df = df[columns_to_keep]

# Convertir les colonnes en float
columns_to_convert = ['price_unit', 'price_total']
df[columns_to_convert] = df[columns_to_convert].astype(float)

# Supprimer les lignes contenant des valeurs nulles
df = df.dropna()

# Enregistrer le nouveau fichier CSV
df.to_csv('Invoice Line.csv', index=False)
