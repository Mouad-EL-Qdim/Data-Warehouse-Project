import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('/home/moad/Downloads/Pdf/Source Database Sales History/Database/Invoice.csv')

# Supprimer les colonnes indésirables
columns_to_keep = ['id', 'origin', 'number', 'total_packages', 'amount_untaxed', 'amount_tax', 'state', 'amount_total', 'date_invoice', 'discount_amount', 'partner_id']
df = df[columns_to_keep]

# Convertir les colonnes en float
columns_to_convert = ['total_packages', 'amount_untaxed', 'amount_tax', 'amount_total', 'discount_amount']
df[columns_to_convert] = df[columns_to_convert].astype(float)

# Supprimer les lignes contenant des valeurs nulles
df = df.dropna()

# Enregistrer le nouveau fichier CSV
df.to_csv('Invoice_modified.csv', index=False)
