from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6 import uic

from PyQt6.QtGui import QTextDocument, QPainter
from PyQt6.QtPrintSupport import QPrinter

import School_System.helpers.db_utils as database

from School_System.ui import EXPORT_PDF_DIALOG


class ExportPdfDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(EXPORT_PDF_DIALOG, self)

        self.setWindowTitle("Export pdf")


        ##self.index_instance.students_table
        self.close_button.clicked.connect(self.export_to_pdf)




    def export_to_pdf(self):
        """Exports table data to a PDF file."""
        options = QFileDialog.Option(0)

        file_path, _ = QFileDialog.getSaveFileName(
            None,  # Parent set to `None` to avoid inheriting app styles
            "Save PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options
        )

        if not file_path:
            return  # User canceled

        # Convert table to HTML
        html_content = "<table border='1' cellspacing='0' cellpadding='3'>"
        html_content += "<tr>"

        # Add table headers
        for col in range(self.index_instance.students_table.columnCount()):
            html_content += f"<th>{self.index_instance.students_table.horizontalHeaderItem(col).text()}</th>"
        html_content += "</tr>"

        # Add table data
        for row in range(self.index_instance.students_table.rowCount()):
            html_content += "<tr>"
            for col in range(self.index_instance.students_table.columnCount()):
                item = self.index_instance.students_table.item(row, col)
                html_content += f"<td>{item.text() if item else ''}</td>"
            html_content += "</tr>"

        html_content += "</table>"

        # Convert HTML to PDF
        document = QTextDocument()
        document.setHtml(html_content)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_path)

        document.print(printer)

        print(f"PDF saved to: {file_path}")

