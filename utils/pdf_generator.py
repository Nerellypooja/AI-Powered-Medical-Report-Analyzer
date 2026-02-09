# utils/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO


def generate_pdf(results, ocr_confidence):
    """
    Generates a PDF summary of lab results
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 1 * inch

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, y, "Medical Report Summary")
    y -= 0.5 * inch

    # OCR confidence
    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, y, f"OCR Confidence: {round(ocr_confidence * 100, 1)}%")
    y -= 0.4 * inch

    # Results
    for r in results:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1 * inch, y, f"{r['test']}")
        y -= 0.2 * inch

        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, y, f"Value: {r['value']}")
        y -= 0.2 * inch

        c.drawString(1 * inch, y, f"Status: {r['status']}")
        y -= 0.2 * inch

        c.drawString(1 * inch, y, f"Normal Range: {r['normal_range']}")
        y -= 0.2 * inch

        y -= 0.2 * inch

        # New page if space runs out
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch

    # Disclaimer
    c.showPage()
    c.setFont("Helvetica", 9)
    c.drawString(
        1 * inch,
        height - 1 * inch,
        "Disclaimer: This report is for informational purposes only and does not replace medical advice."
    )

    c.save()
    buffer.seek(0)
    return buffer
