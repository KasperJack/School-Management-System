class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Dictionary mapping QDate to a list of events
        self.events = {}

    def add_event(self, date: QDate, event: Event):
        """Add an event to a specific date."""
        if date not in self.events:
            self.events[date] = []
        self.events[date].append(event)
        self.update()  # Repaint the calendar

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        """
        Paint the cell using the default drawing,
        then paint a single event card if the date has events.
        """
        # First, let QCalendarWidget draw the cell (date number, etc.)
        super().paintCell(painter, rect, date)

        if date in self.events:
            painter.save()

            # Use the first event as the main event to display.
            events = self.events[date]
            main_event = events[0]
            extra_count = len(events) - 1

            # Create the text to display.
            event_text = main_event.title
            if extra_count > 0:
                event_text += f" +{extra_count}"

            # Define a rectangle at the bottom of the cell for the event card.
            card_height = 15
            card_rect = QRect(
                rect.left() + 2,
                rect.bottom() - card_height - 2,
                rect.width() - 4,
                card_height
            )

            # Draw the event card background.
            painter.setBrush(main_event.color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(card_rect, 3, 3)

            # Draw the event text.
            painter.setPen(QPen(Qt.GlobalColor.black))
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            text_rect = card_rect.adjusted(2, 0, -2, 0)
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                event_text
            )

            painter.restore()



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



