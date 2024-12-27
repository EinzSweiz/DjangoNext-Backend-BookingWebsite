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

    # Add the company logo
    try:
        pdf.drawImage("backend/media/uploads/avatars/images.jpeg", 0.5 * inch, height - 1.2 * inch, width=1.5 * inch, height=1 * inch, mask='auto')
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Header with invoice title and payment status
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(2.5 * inch, height - 1 * inch, "INVOICE")

    payment_status = "PAID"
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(colors.green if payment_status == "PAID" else colors.red)
    pdf.drawString(width - 2 * inch, height - 1 * inch, payment_status)

    # Draw a divider line
    pdf.setFillColor(colors.gray)
    pdf.line(0.5 * inch, height - 1.3 * inch, width - 0.5 * inch, height - 1.3 * inch)

    # Customer details
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    y_position = height - 1.6 * inch
    pdf.drawString(0.5 * inch, y_position, "Billed To:")
    pdf.setFont("Helvetica", 10)
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"Name: {response_data['customer']['name']}")
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"Email: {response_data['customer']['email']}")

    # Company details
    pdf.setFont("Helvetica-Bold", 12)
    y_position = height - 1.6 * inch
    pdf.drawString(width / 2, y_position, "Your Company Name")
    pdf.setFont("Helvetica", 10)
    y_position -= 0.2 * inch
    pdf.drawString(width / 2, y_position, "123 Main Street")
    y_position -= 0.2 * inch
    pdf.drawString(width / 2, y_position, "Anytown, US 12345")
    y_position -= 0.2 * inch
    pdf.drawString(width / 2, y_position, "info@company.com")

    # Reservation details
    pdf.setFont("Helvetica-Bold", 12)
    y_position -= 0.5 * inch
    pdf.drawString(0.5 * inch, y_position, "Reservation Details:")
    pdf.setFont("Helvetica", 10)
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"Property: {response_data['reservation']['property']['name']}")
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"Location: {response_data['reservation']['property']['address']}")
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"Start Date: {response_data['reservation']['start_date']}")
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"End Date: {response_data['reservation']['end_date']}")
    y_position -= 0.2 * inch
    pdf.drawString(0.5 * inch, y_position, f"Total Price: ${response_data['reservation']['total_price']}")

    # Add the property image
    y_position -= 0.5 * inch
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(0.5 * inch, y_position, "Property Image:")
    y_position -= 0.2 * inch

    try:
        image_url = response_data['reservation']['property']['image_url']
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_path = "/tmp/property_image.jpg"
            image.save(image_path)
            pdf.drawImage(image_path, 0.5 * inch, y_position - 2 * inch, width=2 * inch, height=1.5 * inch, preserveAspectRatio=True)
    except Exception as e:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(0.5 * inch, y_position, f"Error loading image: {e}")

    # Footer
    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(colors.gray)
    pdf.drawString(0.5 * inch, 0.5 * inch, "Thank you for choosing our service!")
    pdf.drawRightString(width - 0.5 * inch, 0.5 * inch, "Generated on: 2024-12-27")

    # Finalize the PDF
    pdf.save()
    buffer.seek(0)

    return buffer
