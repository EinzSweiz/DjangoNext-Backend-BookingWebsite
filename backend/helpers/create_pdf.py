from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import requests
from PIL import Image

# If you have custom fonts (TTF), you can register them like so:
# pdfmetrics.registerFont(TTFont("CustomFont", "/path/to/custom_font.ttf"))

def generate_payment_pdf(response_data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    current_date = datetime.now().strftime("%Y-%m-%d")
    # --------------------------------------------------------
    # 1. HEADER
    # --------------------------------------------------------
    header_height = 1.7 * inch
    pdf.setFillColorRGB(0.07, 0.45, 0.55)  # Teal
    pdf.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

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
    # Outer box to group reservation details and image
    big_box_height = 2.7 * inch
    big_box_y = box_y - 0.4 * inch - big_box_height

    pdf.setFillColorRGB(0.97, 0.97, 0.97)  # light gray
    pdf.roundRect(box_margin, big_box_y, box_width, big_box_height, 0.1 * inch, fill=1, stroke=0)

    # --- Left Column for Reservation Details ---
    col_padding = 0.3 * inch
    col_width = (box_width / 2) - col_padding
    left_col_x = box_margin + col_padding
    left_col_y_top = big_box_y + big_box_height - 0.4 * inch

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(left_col_x, left_col_y_top, "Reservation Details")

    # Let's define the data in a 2-column format
    # (label, value) pairs
    reservation_table_data = [
        ("Property:",  response_data['reservation']['property']['name']),
        ("Location:",  response_data['reservation']['property']['address']),
        ("Start Date:", response_data['reservation']['start_date']),
        ("End Date:",   response_data['reservation']['end_date']),
        ("Total Price:", f"${response_data['reservation']['total_price']}"),
    ]

    # Move down a bit for the actual table
    pdf.setFont("Helvetica", 11)
    row_height = 0.25 * inch
    current_y = left_col_y_top - 0.5 * inch

    for label, value in reservation_table_data:
        # Label in bold
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(left_col_x, current_y, label)
        # Value in regular font, slightly shifted right
        pdf.setFont("Helvetica", 11)
        pdf.drawString(left_col_x + 1.2 * inch, current_y, str(value))
        current_y -= row_height

    # --- Right Column for Property Image ---
    right_col_x = box_margin + col_width + (2 * col_padding)
    img_col_width = col_width - col_padding
    img_col_height = big_box_height - (2 * col_padding)
    img_y = big_box_y + big_box_height - img_col_height - col_padding

    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(colors.black)
    pdf.drawString(right_col_x, left_col_y_top, "Property Image")

    # Attempt to load and draw the image with a subtle border
    try:
        image_url = response_data['reservation']['property']['image_url']
        resp = requests.get(image_url)
        if resp.status_code == 200:
            image = Image.open(BytesIO(resp.content))
            image_path = "/tmp/property_image.jpg"
            image.save(image_path)

            target_w = img_col_width
            target_h = img_col_height - 0.4 * inch  # some padding

            # Border behind image
            pdf.setFillColorRGB(1, 1, 1)  # white background
            pdf.roundRect(right_col_x, img_y, target_w, target_h, 0.1 * inch, fill=1, stroke=1)

            pdf.drawImage(
                image_path,
                right_col_x,
                img_y,
                width=target_w,
                height=target_h,
                preserveAspectRatio=True,
                anchor='c',
                mask='auto'
            )
    except Exception as e:
        pdf.setFont("Helvetica", 9)
        pdf.drawString(right_col_x, img_y + 0.2 * inch, f"Error loading image: {e}")

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
    pdf.drawRightString(width - 1 * inch, 0.3 * inch, f"Generated on: {current_date}")

    # --------------------------------------------------------
    # FINALIZE & RETURN
    # --------------------------------------------------------
    pdf.save()
    buffer.seek(0)
    return buffer
