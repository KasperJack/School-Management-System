from PyQt6.QtWidgets import QTableWidgetItem




def load_students_to_table(self):


    # Récupère les informations des étudiants
    students = get_students_info()
    #Exemple de sortie de `students` :
    #(1, "Alice Johnson", "Femme", "Grade 10", "Classe A", "2006-05-14", "123 Main St", "1234567890","alice@example.com"),
    #(2, "Bob Smith", "Homme", "Grade 11", "Classe B", "2005-03-22", "456 Elm St", "0987654321", "bob@example.com")




    # Configurer la table pour afficher les données
    self.students_table.setRowCount(len(students))  # Définit le nombre de lignes en fonction des données récupérées

    # Optionnel : cette étape peut être configurée dans l'interface utilisateur (fichier .ui)
    self.students_table.setColumnCount(9)  # Définit 9 colonnes pour les différentes informations
    self.students_table.setHorizontalHeaderLabels([     # Définit les noms des colonnes
        "ID Étudiant", "Nom Complet", "Genre", "Niveau",
        "Nom de la Classe", "Date de Naissance", "Adresse", "Téléphone", "Email"
    ])


    # Remplir la table avec les données des étudiants
    for row_idx, student in enumerate(students):
        for col_idx, data in enumerate(student):
            # Vérifie si la donnée est `None`, remplace par une chaîne vide dans ce cas
            item = QTableWidgetItem(str(data) if data is not None else "")
            # Ajoute la donnée au bon emplacement dans la table
            self.students_table.setItem(row_idx, col_idx, item)



