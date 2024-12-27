from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import requests
from PIL import Image

# If you have custom fonts (TTF), you can register them like so:
# pdfmetrics.registerFont(TTFont("CustomFont", "/path/to/custom_font.ttf"))

def generate_payment_pdf(response_data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --------------------------------------------------------
    # 1. HEADER SECTION
    # --------------------------------------------------------
    # Background rectangle for the header
    header_height = 1.7 * inch
    pdf.setFillColorRGB(0.07, 0.45, 0.55)  # A teal shade
    pdf.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

    # Invoice Title
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(1 * inch, height - 1.2 * inch, "Reservation Invoice")

    # Payment Status Badge (rounded rectangle)
    payment_status = "PAID"  # or "NOT PAID"
    status_color = colors.green if payment_status.upper() == "PAID" else colors.red
    badge_width = 1.5 * inch
    badge_height = 0.5 * inch
    badge_x = width - 1.8 * inch
    badge_y = height - 1.5 * inch

    pdf.setFillColor(status_color)
    pdf.roundRect(badge_x, badge_y, badge_width, badge_height, radius=0.1 * inch, fill=1, stroke=0)

    # Payment Status Text
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(badge_x + badge_width / 2, badge_y + 0.15 * inch, payment_status.upper())

    # --------------------------------------------------------
    # 2. CUSTOMER INFORMATION BOX
    # --------------------------------------------------------
    # Define a box for the details
    box_margin = 1 * inch
    box_width = width - 2 * box_margin
    box_height = 1.2 * inch
    box_y = height - header_height - 0.5 * inch - box_height

    # Draw a light background for the box
    pdf.setFillColorRGB(0.93, 0.97, 0.98)  # Soft teal background
    pdf.roundRect(box_margin, box_y, box_width, box_height, 0.1 * inch, fill=1, stroke=0)

    # Title inside the box
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(box_margin + 0.3 * inch, box_y + box_height - 0.4 * inch, "Customer Information")

    # Customer details
    pdf.setFont("Helvetica", 11)
    inner_y = box_y + box_height - 0.8 * inch
    pdf.drawString(box_margin + 0.3 * inch, inner_y, f"Name: {response_data['customer']['name']}")
    inner_y -= 0.25 * inch
    pdf.drawString(box_margin + 0.3 * inch, inner_y, f"Email: {response_data['customer']['email']}")

    # --------------------------------------------------------
    # 3. RESERVATION DETAILS BOX
    # --------------------------------------------------------
    res_box_height = 2 * inch
    res_box_y = box_y - 0.4 * inch - res_box_height

    pdf.setFillColorRGB(0.97, 0.97, 0.97)  # light gray
    pdf.roundRect(box_margin, res_box_y, box_width, res_box_height, 0.1 * inch, fill=1, stroke=0)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(box_margin + 0.3 * inch, res_box_y + res_box_height - 0.4 * inch, "Reservation Details")

    pdf.setFont("Helvetica", 11)
    details_y = res_box_y + res_box_height - 0.8 * inch
    pdf.drawString(box_margin + 0.3 * inch, details_y, f"Property: {response_data['reservation']['property']['name']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + 0.3 * inch, details_y, f"Location: {response_data['reservation']['property']['address']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + 0.3 * inch, details_y, f"Start Date: {response_data['reservation']['start_date']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + 0.3 * inch, details_y, f"End Date: {response_data['reservation']['end_date']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + 0.3 * inch, details_y, f"Total Price: ${response_data['reservation']['total_price']}")

    # --------------------------------------------------------
    # 4. PROPERTY IMAGE SECTION
    # --------------------------------------------------------
    image_title_y = res_box_y - 0.4 * inch
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(colors.black)
    pdf.drawString(box_margin, image_title_y, "Property Image:")

    # Attempt to load and draw the image
    img_box_width = 3 * inch
    img_box_height = 2 * inch
    img_y = image_title_y - img_box_height - 0.2 * inch
    try:
        image_url = response_data['reservation']['property']['image_url']
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # Optionally, you can save to a temporary file
            image_path = "/tmp/property_image.jpg"
            image.save(image_path)
            pdf.drawImage(
                image_path,
                box_margin,
                img_y,
                width=img_box_width,
                height=img_box_height,
                preserveAspectRatio=True,
                mask='auto'
            )
    except Exception as e:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(box_margin, img_y + 0.5 * inch, f"Error loading image: {e}")

    # --------------------------------------------------------
    # 5. FOOTER SECTION
    # --------------------------------------------------------
    footer_height = 0.8 * inch
    pdf.setFillColorRGB(0.85, 0.85, 0.85)
    pdf.rect(0, 0, width, footer_height, fill=1, stroke=0)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(1 * inch, 0.3 * inch, "Thank you for choosing DiplomaRoad!")

    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawRightString(width - 1 * inch, 0.3 * inch, "Generated on: 2024-12-02")

    # --------------------------------------------------------
    # FINALIZE
    # --------------------------------------------------------
    pdf.save()
    buffer.seek(0)
    return buffer
