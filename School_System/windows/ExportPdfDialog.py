from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6 import uic
from PyQt6.QtGui import QTextDocument, QPainter
from PyQt6.QtPrintSupport import QPrinter
from fontTools.tfmLib import PASSTHROUGH
from fontTools.varLib.models import nonNone
from PyQt6.QtCore import pyqtSlot

import School_System.helpers.db_utils as database

from School_System.ui import EXPORT_PDF_DIALOG


class ExportPdfDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(EXPORT_PDF_DIALOG, self)

        self.setWindowTitle("Export pdf")
        self.classes = database.get_classes_ids_grades()


        ##self.index_instance.students_table
        self.close_button.clicked.connect(self.init_export)
        self.setup()


        default_fields = [
            "students.student_id",
            "students.full_name",
            "students.gender",
            "grades.grade_name",
            "class.class_name",
            "students.email"
        ]

        #ass = database.fetch_students(class_id= 20,fields=default_fields)
        #print(ass)
        #self.export_to_pdf_reportlab(ass)


    def setup(self):
        added_grades = set()
        self.comboBox_grades.addItem("--")  # added default value.
        for class_id, class_name, grade in self.classes:
            self.comboBox_class.addItem(class_name, class_id)
            if grade not in added_grades:
                self.comboBox_grades.addItem(grade)
                added_grades.add(grade)

        self.comboBox_grades.currentIndexChanged.connect(self.update_classes)


    @pyqtSlot(int)  # Signal index
    def update_classes(self, index):
        selected_grade = self.comboBox_grades.itemText(index)
        self.comboBox_class.clear()  # clear the class combo box

        if selected_grade == "--":
            for class_id, class_name, grade in self.classes:
                self.comboBox_class.addItem(class_name, class_id)
            return

        for class_id, class_name, grade in self.classes:
            if grade == selected_grade:
                self.comboBox_class.addItem(class_name, class_id)



    def init_export(self):
        fields = []
        class_id = None
        pass


























    def export_to_pdf_reportlab(self,data, column_names=None):
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from PyQt6.QtWidgets import QFileDialog, QApplication
        import datetime

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        options = QFileDialog.Option(0)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)",
                                                   options=options)

        if not file_path:
            return False

        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'

        if not data:
            print("No data to export.")
            return False

        try:
            if not column_names and data and isinstance(data[0], dict):
                column_names = list(data[0].keys())
            elif not column_names:
                if data and isinstance(data[0], (list, tuple)):
                    column_names = [f"Column {i + 1}" for i in range(len(data[0]))]
                else:
                    column_names = ["Data"]

            table_data = []
            styles = getSampleStyleSheet()

            table_cell_style = ParagraphStyle(
                'TableCell',
                parent=styles['Normal'],
                wordWrap='CJK',
                leading=12,
                fontSize=8,
            )

            header_row = [Paragraph(col.replace('_', ' ').title().split('.')[-1], styles['Normal']) for col in
                          column_names]
            table_data.append(header_row)

            for row in data:
                data_row = []
                if isinstance(row, dict):
                    for col in column_names:
                        value = str(row.get(col, ""))
                        data_row.append(Paragraph(value, table_cell_style))
                elif isinstance(row, (list, tuple)):
                    data_row = [Paragraph(str(val) if val is not None else "", table_cell_style) for val in row]
                else:
                    data_row = [Paragraph(str(row) if row is not None else "", table_cell_style)]
                table_data.append(data_row)

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []

            elements.append(Paragraph("Data Export", styles['Title']))
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elements.append(Paragraph(f"Generated on: {current_time}", styles['Normal']))
            elements.append(Paragraph("<br/><br/>", styles['Normal']))

            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),  # add padding to the left.
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # add padding to the right.
            ]))
            elements.append(table)

            elements.append(Paragraph("<br/><br/>", styles['Normal']))
            elements.append(Paragraph(f"Total records: {len(data)}", styles['Italic']))

            doc.build(elements)
            return True

        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            return False



