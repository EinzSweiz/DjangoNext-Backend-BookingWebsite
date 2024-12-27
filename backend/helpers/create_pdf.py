from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
import requests
from PIL import Image

def generate_payment_pdf(response_data):
    # Create a BytesIO buffer to hold the PDF
    buffer = BytesIO()

    # Set up the PDF canvas
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header with gradient background
    pdf.setFillColorRGB(0.1, 0.4, 0.7)  # Blue
    pdf.rect(0, height - 1.5 * inch, width, 1.5 * inch, fill=1)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.setFillColor(colors.white)
    pdf.drawString(1 * inch, height - 1.2 * inch, "Reservation Invoice")

    # Add payment status (PAID or NOT PAID)
    payment_status = "PAID"
    pdf.setFont("Helvetica-Bold", 28)
    pdf.setFillColor(colors.green if payment_status == "PAID" else colors.red)
    pdf.drawRightString(width - 1 * inch, height - 1.2 * inch, payment_status)

    # Divider line
    pdf.setFillColor(colors.gray)
    pdf.line(0.5 * inch, height - 1.7 * inch, width - 0.5 * inch, height - 1.7 * inch)

    # Customer details
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    y_position = height - 2.2 * inch
    pdf.drawString(1 * inch, y_position, "Customer Information:")
    pdf.setFont("Helvetica", 12)
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Name: {response_data['customer']['name']}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Email: {response_data['customer']['email']}")

    # Reservation details
    pdf.setFont("Helvetica-Bold", 14)
    y_position -= 0.6 * inch
    pdf.drawString(1 * inch, y_position, "Reservation Details:")
    pdf.setFont("Helvetica", 12)
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Property: {response_data['reservation']['property']['name']}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Location: {response_data['reservation']['property']['address']}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Start Date: {response_data['reservation']['start_date']}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"End Date: {response_data['reservation']['end_date']}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Total Price: ${response_data['reservation']['total_price']}")

    # Property image
    y_position -= 0.6 * inch
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(1 * inch, y_position, "Property Image:")
    y_position -= 0.3 * inch

    try:
        image_url = response_data['reservation']['property']['image_url']
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_path = "/tmp/property_image.jpg"
            image.save(image_path)  # Save temporarily
            pdf.drawImage(image_path, 1 * inch, y_position - 2 * inch, width=3 * inch, height=2 * inch, preserveAspectRatio=True)
    except Exception as e:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(1 * inch, y_position, f"Error loading image: {e}")
    y_position -= 2.5 * inch

    # Footer with branding
    pdf.setFillColorRGB(0.95, 0.95, 0.95)  # Light gray
    pdf.rect(0, 0, width, 0.8 * inch, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(1 * inch, 0.4 * inch, "Thank you for choosing DiplomaRoad!")
    pdf.drawRightString(width - 1 * inch, 0.4 * inch, "Generated on: 2024-12-02")

    # Finalize the PDF
    pdf.save()
    buffer.seek(0)

    return buffer
