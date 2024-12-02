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

    # Draw header with background color
    pdf.setFillColorRGB(0.1, 0.4, 0.7)  # Blue
    pdf.rect(0, height - 1.2 * inch, width, 1.2 * inch, fill=1)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(colors.white)
    pdf.drawString(1 * inch, height - 0.9 * inch, "Reservation Invoice")

    # Add a status (PAID or NOT PAID)
    payment_status = "PAID"
    pdf.setFont("Helvetica-Bold", 30)
    pdf.setFillColor(colors.red if payment_status == "NOT PAID" else colors.green)
    pdf.drawString(width - 3 * inch, height - 0.9 * inch, payment_status)

    # Draw customer and reservation details
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 12)
    y_position = height - 1.6 * inch

    # Customer details
    pdf.drawString(1 * inch, y_position, f"Customer: {response_data['customer']['name']}")
    y_position -= 0.3 * inch
    pdf.drawString(1 * inch, y_position, f"Email: {response_data['customer']['email']}")
    y_position -= 0.5 * inch

    # Reservation details
    pdf.setFont("Helvetica-Bold", 14)
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
    y_position -= 0.5 * inch

    # Attempt to fetch and add the property image
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(1 * inch, y_position, "Property Image:")
    y_position -= 0.3 * inch

    try:
        image_url = response_data['reservation']['property']['image_url']
        response = requests.get(image_url)
        if response.status_code == 200:
            # Load the image into PIL and draw it onto the PDF
            image = Image.open(BytesIO(response.content))
            image_path = "/tmp/property_image.jpg"
            image.save(image_path)  # Save temporarily
            pdf.drawImage(image_path, 1 * inch, y_position - 3 * inch, width=3 * inch, height=2 * inch)
    except Exception as e:
        pdf.drawString(1 * inch, y_position, f"Error adding image: {e}")
    y_position -= 2.5 * inch

    # Footer
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.gray)
    pdf.drawString(1 * inch, 0.5 * inch, "Thank you for choosing our service!")
    pdf.drawString(width - 3 * inch, 0.5 * inch, "Generated on: 2024-12-02")

    # Finalize the PDF
    pdf.save()
    buffer.seek(0)

    return buffer
