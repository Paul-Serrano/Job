import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QLabel, QPushButton, QVBoxLayout, QWidget, QListWidget, QDialog, QComboBox, QLineEdit, QDateEdit, QTextEdit, QFormLayout, QHBoxLayout
from PySide6.QtCore import Qt
# from ui_file import Ui_MainWindow
from PyQt6 import uic

# Ui_MainWindow, QtBaseClass = uic.loadUiType("ui_file.ui")

class Job(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)

        # Configuration de la fenêtre principale
        self.setWindowTitle("Mon Application")
        self.setGeometry(200, 100, 600, 500)

        # Création d'un layout pour organiser les widgets
        layout = QVBoxLayout()

        # Création d'un widget central pour la fenêtre principale
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Ajoutez un widget pour afficher la liste des offres d'emploi
        self.offresListWidget = QListWidget()
        layout.addWidget(self.offresListWidget)

        # Ajoutez des boutons pour ajouter et supprimer des offres
        self.addButton = QPushButton("Ajouter une offre")
        self.removeButton = QPushButton("Supprimer une offre")
        layout.addWidget(self.addButton)
        layout.addWidget(self.removeButton)

        # Connectez les signaux aux slots pour les boutons
        self.addButton.clicked.connect(self.ajouter_offre)
        self.removeButton.clicked.connect(self.supprimer_offre)

        # Déclarez les widgets pour le formulaire d'ajout
        self.comboBoxTypeAnnonce = QComboBox()
        self.comboBoxEtat = QComboBox()
        self.dateEditDate = QDateEdit()
        self.lineEditEntreprise = QLineEdit()
        self.lineEditPoste = QLineEdit()
        self.lineEditLienAnnonce = QLineEdit()
        self.textEditTexteAnnonce = QTextEdit()
        self.lineEditNomDestinataire = QLineEdit()
        self.lineEditEmailDestinataire = QLineEdit()
        self.lineEditTelephoneDestinataire = QLineEdit()
        self.lineEditLinkedInDestinataire = QLineEdit()
        self.textEditNotes = QTextEdit()
        self.dateEditDateRelance = QDateEdit()
        self.dateEditDateRendezVous = QDateEdit()

        # Connectez le signal du bouton au slot (la fonction) pour ouvrir le formulaire
        self.addButton.clicked.connect(self.ouvrir_formulaire_ajout)

        # Affichez initialement les offres d'emploi
        self.afficher_offres()

    def ajouter_offre(self):
        type_annonce = self.comboBoxTypeAnnonce.currentText()
        etat = self.comboBoxEtat.currentText()
        date = self.dateEditDate.date().toString("yyyy-MM-dd")
        entreprise = self.lineEditEntreprise.text()
        poste = self.lineEditPoste.text()
        lien_annonce = self.lineEditLienAnnonce.text()
        texte_annonce = self.textEditTexteAnnonce.toPlainText()
        nom_destinataire = self.lineEditNomDestinataire.text()
        email_destinataire = self.lineEditEmailDestinataire.text()
        telephone_destinataire = self.lineEditTelephoneDestinataire.text()
        linkedin_destinataire = self.lineEditLinkedInDestinataire.text()
        notes = self.textEditNotes.toPlainText()
        date_relance = self.dateEditDateRelance.date().toString("yyyy-MM-dd")
        date_rendez_vous = self.dateEditDateRendezVous.date().toString("yyyy-MM-dd")

        # Insérer les données dans la base de données
        conn = sqlite3.connect('job.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO offres_emploi (
                type_annonce, etat, date, entreprise, poste, lien_annonce, texte_annonce, nom_destinataire,
                email_destinataire, telephone_destinataire, linkedin_destinataire, notes, date_relance, date_rendez_vous
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (type_annonce, etat, date, entreprise, poste, lien_annonce, texte_annonce, nom_destinataire,
            email_destinataire, telephone_destinataire, linkedin_destinataire, notes, date_relance, date_rendez_vous))
        conn.commit()
        conn.close()

    def supprimer_offre(self):
        # Récupérez l'ID de l'offre d'emploi à supprimer
        offre_id = self.get_selected_offre_id()

        if offre_id is not None:
            # Supprimez l'offre d'emploi de la base de données
            conn = sqlite3.connect('job.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM offres_emploi WHERE id = ?', (offre_id,))
            conn.commit()
            conn.close()

    def afficher_offres(self):
        # Récupérez les offres d'emploi depuis la base de données
        conn = sqlite3.connect('job.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM offres_emploi')
        offres = cursor.fetchall()
        conn.close()

        # Créez un layout pour organiser les cartes d'offres
        offres_layout = QVBoxLayout()

        for offre in offres:
            # Créez une carte (QWidget) pour chaque offre
            offre_widget = QWidget()

            # Créez un layout pour la carte de l'offre
            carte_layout = QVBoxLayout()

            # Ajoutez des labels pour afficher toutes les informations de l'offre
            label_type_annonce = QLabel(f"Type d'annonce: {offre[1]}")
            label_etat = QLabel(f"État: {offre[2]}")
            label_date = QLabel(f"Date: {offre[3]}")
            label_entreprise = QLabel(f"Entreprise: {offre[4]}")
            label_poste = QLabel(f"Poste: {offre[5]}")
            label_lien_annonce = QLabel(f"Lien de l'annonce: {offre[6]}")
            label_texte_annonce = QLabel(f"Texte de l'annonce: {offre[7]}")
            label_nom_destinataire = QLabel(f"Nom du destinataire: {offre[8]}")
            label_email_destinataire = QLabel(f"Email du destinataire: {offre[9]}")
            label_telephone_destinataire = QLabel(f"Téléphone du destinataire: {offre[10]}")
            label_linkedin_destinataire = QLabel(f"LinkedIn du destinataire: {offre[11]}")
            label_notes = QLabel(f"Notes: {offre[12]}")
            label_date_relance = QLabel(f"Date de relance: {offre[13]}")
            label_date_rendez_vous = QLabel(f"Date de rendez-vous: {offre[14]}")

            # Ajoutez les labels à la carte de l'offre
            carte_layout.addWidget(label_type_annonce)
            carte_layout.addWidget(label_etat)
            carte_layout.addWidget(label_date)
            carte_layout.addWidget(label_entreprise)
            carte_layout.addWidget(label_poste)
            carte_layout.addWidget(label_lien_annonce)
            carte_layout.addWidget(label_texte_annonce)
            carte_layout.addWidget(label_nom_destinataire)
            carte_layout.addWidget(label_email_destinataire)
            carte_layout.addWidget(label_telephone_destinataire)
            carte_layout.addWidget(label_linkedin_destinataire)
            carte_layout.addWidget(label_notes)
            carte_layout.addWidget(label_date_relance)
            carte_layout.addWidget(label_date_rendez_vous)

            # Définissez le layout de la carte de l'offre
            offre_widget.setLayout(carte_layout)

            # Ajoutez la carte de l'offre au layout des offres
            offres_layout.addWidget(offre_widget)

        # Définissez le layout des offres comme le layout central de votre fenêtre
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(offres_layout)



    def get_selected_offre_id(self):
        # Récupérez l'ID de l'offre d'emploi sélectionnée dans l'interface utilisateur (par exemple, à partir d'une liste ou d'un tableau)
        # Cette fonction dépend de la façon dont vous gérez la sélection dans votre interface utilisateur.
        selected_item = self.offresListWidget.currentItem()  # Supposons que vous utilisez un QListWidget
        if selected_item is not None:
            # L'ID de l'offre d'emploi peut être stocké dans les données de l'élément sélectionné
            offre_id = selected_item.data(Qt.UserRole)  # Qt.UserRole doit être défini lors de l'ajout de l'élément
            return offre_id
        return None
    
    def display_offres_in_ui(self, offres):
        # Affichez les offres d'emploi dans l'interface utilisateur (par exemple, dans une liste ou un tableau)
        # Cette fonction dépend de la façon dont vous souhaitez afficher les offres dans votre interface utilisateur.
        self.offresListWidget.clear()  # Supprimez les éléments existants dans la liste
        for offre in offres:
            # Créez un élément pour chaque offre et ajoutez-le à la liste
            item = QListWidgetItem(f"{offre[4]} - {offre[3]}")  # Exemple : affiche le nom du poste et le nom de l'entreprise
            item.setData(Qt.UserRole, offre[0])  # Stockez l'ID de l'offre dans Qt.UserRole
            self.offresListWidget.addItem(item)  # Ajoutez l'élément à la liste

    def ouvrir_formulaire_ajout(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Ajouter une offre d'emploi")

        # Créez le formulaire avec un QFormLayout
        form_layout = QFormLayout()

        # Créez les champs déroulants (dropdown menus) pour "Type d'annonce" et "État"
        self.comboBoxTypeAnnonce = QComboBox()
        self.comboBoxTypeAnnonce.addItems(["Stage", "Alternance", "Emploi"])
        self.comboBoxEtat = QComboBox()
        self.comboBoxEtat.addItems(["Oui", "Non", "En attente"])

        # Ajoutez les champs du formulaire avec leur étiquette
        form_layout.addRow("Type d'annonce:", self.comboBoxTypeAnnonce)
        form_layout.addRow("État:", self.comboBoxEtat)
        form_layout.addRow("Date:", self.dateEditDate)
        form_layout.addRow("Entreprise:", self.lineEditEntreprise)
        form_layout.addRow("Poste:", self.lineEditPoste)
        form_layout.addRow("Lien de l'annonce:", self.lineEditLienAnnonce)
        form_layout.addRow("Texte de l'annonce:", self.textEditTexteAnnonce)
        form_layout.addRow("Nom du destinataire:", self.lineEditNomDestinataire)
        form_layout.addRow("Email du destinataire:", self.lineEditEmailDestinataire)
        form_layout.addRow("Téléphone du destinataire:", self.lineEditTelephoneDestinataire)
        form_layout.addRow("Lien LinkedIn du destinataire:", self.lineEditLinkedInDestinataire)
        form_layout.addRow("Notes:", self.textEditNotes)
        form_layout.addRow("Date de relance:", self.dateEditDateRelance)
        form_layout.addRow("Date de rendez-vous:", self.dateEditDateRendezVous)

        # Bouton pour enregistrer
        button_enregistrer = QPushButton("Enregistrer")

        # Connectez le bouton "Enregistrer" à la fonction d'enregistrement
        button_enregistrer.clicked.connect(self.enregistrer_offre)

        # Créez un layout pour organiser le bouton
        button_layout = QHBoxLayout()
        button_layout.addWidget(button_enregistrer)

        # Créez un layout principal pour organiser le formulaire et le bouton
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.dialog.setLayout(main_layout)

        button_enregistrer.clicked.connect(self.enregistrer_offre)

        self.dialog.exec()



    def enregistrer_offre(self):
        type_annonce = self.comboBoxTypeAnnonce.currentText()
        etat = self.comboBoxEtat.currentText()
        date = self.dateEditDate.date().toString("yyyy-MM-dd")
        entreprise = self.lineEditEntreprise.text()
        poste = self.lineEditPoste.text()
        lien_annonce = self.lineEditLienAnnonce.text()
        texte_annonce = self.textEditTexteAnnonce.toPlainText()
        nom_destinataire = self.lineEditNomDestinataire.text()
        email_destinataire = self.lineEditEmailDestinataire.text()
        telephone_destinataire = self.lineEditTelephoneDestinataire.text()
        linkedin_destinataire = self.lineEditLinkedInDestinataire.text()
        notes = self.textEditNotes.toPlainText()
        date_relance = self.dateEditDateRelance.date().toString("yyyy-MM-dd")
        date_rendez_vous = self.dateEditDateRendezVous.date().toString("yyyy-MM-dd")

        # Insérer les données dans la base de données
        conn = sqlite3.connect('job.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO offres_emploi (
                type_annonce, etat, date, entreprise, poste, lien_annonce, texte_annonce, nom_destinataire,
                email_destinataire, telephone_destinataire, linkedin_destinataire, notes, date_relance, date_rendez_vous
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (type_annonce, etat, date, entreprise, poste, lien_annonce, texte_annonce, nom_destinataire,
            email_destinataire, telephone_destinataire, linkedin_destinataire, notes, date_relance, date_rendez_vous))
        conn.commit()
        conn.close()
        self.dialog.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Job()
    window.show()
    sys.exit(app.exec_())
