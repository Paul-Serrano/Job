import sqlite3

conn = sqlite3.connect('job.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE offres_emploi (
        id INTEGER PRIMARY KEY,
        type_annonce TEXT,
        etat TEXT,
        date TEXT,
        entreprise TEXT,
        poste TEXT,
        lien_annonce TEXT,
        texte_annonce TEXT,
        nom_destinataire TEXT,
        email_destinataire TEXT,
        telephone_destinataire TEXT,
        linkedin_destinataire TEXT,
        notes TEXT,
        date_relance TEXT,
        date_rendez_vous TEXT
    )
''')

conn.commit()

conn.close()
