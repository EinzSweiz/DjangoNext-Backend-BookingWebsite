from celery import shared_task
from io import BytesIO
from helpers.messaging import send_message
from helpers.create_pdf import generate_payment_pdf

@shared_task
def send_property_creation_message(response_data):
    try:
        # Extract the necessary information from response_data
        landlord_email = response_data['customer']['email']
        landlord_name = response_data['customer']['name']
        property_data = response_data['reservation']
        
        subject = 'New Property Created'
        from_email = 'riad.sultanov.1999@gmail.com'
        to_email = landlord_email

        # Prepare the HTML message body
        html_message = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    h1 {{ color: #1f2937; }}
                    h2 {{ color: #1f2937; }}
                    p {{ color: #4b5563; }}
                    .property-info {{ margin-bottom: 10px; }}
                </style>
            </head>
            <body>
                <h1>Dear {landlord_name},</h1><br>
                <h2>New Property Created</h2>
                <p>A new property has been added:</p>
                <div class="property-info">
                    <strong>Name:</strong> {property_data['property']['name']}<br>
                    <strong>Location:</strong> {property_data['property']['address']}<br>
                    <strong>Price per Night:</strong> ${property_data['total_price']}<br>
                    <strong>Bedrooms:</strong> {property_data['number_of_nights']}<br>
                    <strong>Bathrooms:</strong> {property_data['guests']}
                </div>
                <p>Thank you for using our service!</p>
            </body>
        </html>
        """

        # Generate the PDF from response_data
        pdf_buffer = generate_payment_pdf(response_data)

        # Attach the PDF and send the email with the PDF
        send_message(
            subject=subject,
            message=html_message,
            from_email=from_email,
            to_email=to_email,
            attachment_name='property_creation_details.pdf',
            attachment_content=pdf_buffer.getvalue(),
            attachment_mime_type='application/pdf'
        )

    except Exception as e:
        print(f"Error sending confirmation email: {e}")
