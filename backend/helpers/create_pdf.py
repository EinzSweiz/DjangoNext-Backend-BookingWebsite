from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def generate_payment_pdf(response_data):
    buffer = BytesIO()

    # Create PDF with ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add some text to the PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 100, f"Payment Successful for Reservation ID: {response_data['reservation']['id']}")
    p.drawString(100, height - 120, f"Total Price: ${response_data['reservation']['total_price']}")
    p.drawString(100, height - 140, f"Guests: {response_data['reservation']['guests']}")
    
    # Add reservation dates
    p.drawString(100, height - 160, f"Start Date: {response_data['reservation']['start_date']}")
    p.drawString(100, height - 180, f"End Date: {response_data['reservation']['end_date']}")

    # Add property information
    p.drawString(100, height - 200, f"Property: {response_data['reservation']['property']['name']}")
    p.drawString(100, height - 220, f"Address: {response_data['reservation']['property']['address']}")
    
    # If there's an image URL, add it to the PDF (optional)
    img_path = response_data['reservation']['property']['image_url']
    try:
        img = Image.open(img_path)
        img_path_temp = "/tmp/temp_property_image.jpg"
        img.save(img_path_temp)
        p.drawImage(img_path_temp, 100, height - 300, width=200, height=200)  # Adjust coordinates as needed
    except Exception as e:
        print("Error adding image to PDF:", e)

    # Add customer information
    p.drawString(100, height - 320, f"Customer Name: {response_data['customer']['name']}")
    p.drawString(100, height - 340, f"Customer Email: {response_data['customer']['email']}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
