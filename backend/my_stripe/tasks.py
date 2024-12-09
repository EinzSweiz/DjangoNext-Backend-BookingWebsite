from celery import shared_task
from io import BytesIO
from helpers.messaging import send_message
from helpers.create_pdf import generate_payment_pdf

@shared_task
def send_invoice_creation_message(response_data):
    try:
        # Extract the necessary information from response_data
        landlord_email = response_data['customer']['email']
        landlord_name = response_data['customer']['name']
        property_data = response_data['reservation']
        
        subject = 'Invoice for Your Reservation'
        from_email = 'riad.sultanov.1999@gmail.com'
        to_email = landlord_email

        # Updated HTML message for the invoice email
        html_message = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    h1 {{ color: #1f2937; }}
                    h2 {{ color: #1f2937; }}
                    p {{ color: #4b5563; }}
                    .invoice-info, .property-info {{ margin-bottom: 10px; }}
                </style>
            </head>
            <body>
                <h1>Dear {landlord_name},</h1><br>
                <h2>Invoice for Reservation</h2>
                <p>Thank you for your reservation! Below are the details of your booking:</p>
                <div class="invoice-info">
                    <strong>Invoice ID:</strong> {response_data['reservation']['id']}<br>
                    <strong>Start Date:</strong> {response_data['reservation']['start_date']}<br>
                    <strong>End Date:</strong> {response_data['reservation']['end_date']}<br>
                    <strong>Total Price:</strong> ${response_data['reservation']['total_price']}<br>
                    <strong>Number of Nights:</strong> {response_data['reservation']['number_of_nights']}<br>
                    <strong>Guests:</strong> {response_data['reservation']['guests']}
                </div>
                <div class="property-info">
                    <strong>Property Name:</strong> {response_data['reservation']['property']['name']}<br>
                    <strong>Location:</strong> {response_data['reservation']['property']['address']}<br>
                    <strong>Property ID:</strong> {response_data['reservation']['property']['id']}
                </div>
                <p>If you have any questions, feel free to contact us. Thank you for choosing our service!</p>
            </body>
        </html>
        """

        # Generate the PDF from response_data
        pdf_buffer = generate_payment_pdf(response_data)

        # Send the email with the PDF
        send_message(
            subject=subject,
            message=html_message,
            from_email=from_email,
            to_email=to_email,
            attachment_name='reservation_invoice.pdf',
            attachment_content=pdf_buffer.getvalue(),
            attachment_mime_type='application/pdf'
        )

    except Exception as e:
        print(f"Error sending invoice email: {e}")
