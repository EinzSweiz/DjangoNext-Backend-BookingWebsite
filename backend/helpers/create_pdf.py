from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import requests
from PIL import Image

# Example custom font usage (commented out):
# pdfmetrics.registerFont(TTFont("CustomFont", "/path/to/custom_font.ttf"))

def generate_payment_pdf(response_data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --------------------------------------------------------
    # 1. HEADER SECTION
    # --------------------------------------------------------
    header_height = 1.7 * inch
    pdf.setFillColorRGB(0.07, 0.45, 0.55)  # Teal
    pdf.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(1 * inch, height - 1.2 * inch, "Reservation Invoice")

    # Payment Status Badge (rounded rectangle)
    payment_status = "PAID"  # Or "NOT PAID"
    status_color = colors.green if payment_status.upper() == "PAID" else colors.red
    badge_width = 1.5 * inch
    badge_height = 0.5 * inch
    badge_x = width - 1.8 * inch
    badge_y = height - 1.5 * inch

    pdf.setFillColor(status_color)
    pdf.roundRect(badge_x, badge_y, badge_width, badge_height, radius=0.1 * inch, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(badge_x + badge_width / 2, badge_y + 0.15 * inch, payment_status.upper())

    # --------------------------------------------------------
    # 2. CUSTOMER INFO BOX
    # --------------------------------------------------------
    box_margin = 1 * inch
    box_width = width - 2 * box_margin
    box_height = 1.2 * inch
    box_y = height - header_height - 0.5 * inch - box_height

    pdf.setFillColorRGB(0.93, 0.97, 0.98)  # Soft teal background
    pdf.roundRect(box_margin, box_y, box_width, box_height, 0.1 * inch, fill=1, stroke=0)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(box_margin + 0.3 * inch, box_y + box_height - 0.4 * inch, "Customer Information")

    pdf.setFont("Helvetica", 11)
    inner_y = box_y + box_height - 0.8 * inch
    pdf.drawString(box_margin + 0.3 * inch, inner_y, f"Name: {response_data['customer']['name']}")
    inner_y -= 0.25 * inch
    pdf.drawString(box_margin + 0.3 * inch, inner_y, f"Email: {response_data['customer']['email']}")

    # --------------------------------------------------------
    # 3. RESERVATION DETAILS & IMAGE SIDE-BY-SIDE
    # --------------------------------------------------------
    # We’ll create two “columns” within one larger box:
    #   - Left column for details
    #   - Right column for the property image

    # Outer box to visually group them
    big_box_height = 2.7 * inch
    big_box_y = box_y - 0.4 * inch - big_box_height
    pdf.setFillColorRGB(0.97, 0.97, 0.97)  # light gray
    pdf.roundRect(box_margin, big_box_y, box_width, big_box_height, 0.1 * inch, fill=1, stroke=0)

    # Left column for reservation details
    col_padding = 0.3 * inch
    col_width = (box_width / 2) - col_padding

    # Title
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(box_margin + col_padding, big_box_y + big_box_height - 0.4 * inch, "Reservation Details")

    # Details text
    pdf.setFont("Helvetica", 11)
    details_y = big_box_y + big_box_height - 0.8 * inch
    pdf.drawString(box_margin + col_padding, details_y, f"Property: {response_data['reservation']['property']['name']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + col_padding, details_y, f"Location: {response_data['reservation']['property']['address']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + col_padding, details_y, f"Start Date: {response_data['reservation']['start_date']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + col_padding, details_y, f"End Date: {response_data['reservation']['end_date']}")
    details_y -= 0.25 * inch
    pdf.drawString(box_margin + col_padding, details_y, f"Total Price: ${response_data['reservation']['total_price']}")

    # Right column for property image
    img_col_x = box_margin + col_width + (2 * col_padding)
    img_col_width = col_width - col_padding
    img_col_height = big_box_height - (2 * col_padding)
    img_y = big_box_y + big_box_height - img_col_height - col_padding

    # Label above the image
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(colors.black)
    pdf.drawString(img_col_x, big_box_y + big_box_height - 0.4 * inch, "Property Image")

    # Try loading the image
    try:
        image_url = response_data['reservation']['property']['image_url']
        resp = requests.get(image_url)
        if resp.status_code == 200:
            image = Image.open(BytesIO(resp.content))
            image_path = "/tmp/property_image.jpg"
            image.save(image_path)

            # Let's maintain the aspect ratio but fit within the column
            # We'll define a target width or height based on the box
            target_w = img_col_width
            target_h = img_col_height - 0.3 * inch  # some top/bottom padding

            # Draw a light border around the image area for a subtle frame
            pdf.setFillColorRGB(1, 1, 1)  # white background behind image
            pdf.roundRect(img_col_x, img_y, target_w, target_h, 0.1 * inch, fill=1, stroke=1)
            pdf.drawImage(
                image_path,
                img_col_x,
                img_y,
                width=target_w,
                height=target_h,
                preserveAspectRatio=True,
                anchor='c',
                mask='auto'
            )
    except Exception as e:
        pdf.setFont("Helvetica", 9)
        pdf.drawString(img_col_x, img_y + 0.2 * inch, f"Error loading image: {e}")

    # --------------------------------------------------------
    # 4. FOOTER
    # --------------------------------------------------------
    footer_height = 0.8 * inch
    pdf.setFillColorRGB(0.85, 0.85, 0.85)
    pdf.rect(0, 0, width, footer_height, fill=1, stroke=0)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(1 * inch, 0.3 * inch, "Thank you for choosing DiplomaRoad!")

    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawRightString(width - 1 * inch, 0.3 * inch, "Generated on: 2024-12-27")

    # --------------------------------------------------------
    # FINALIZE & RETURN
    # --------------------------------------------------------
    pdf.save()
    buffer.seek(0)
    return buffer
