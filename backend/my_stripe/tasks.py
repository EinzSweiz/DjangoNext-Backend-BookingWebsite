from celery import shared_task
from io import BytesIO
from helpers.messaging import send_message
from helpers.create_pdf import generate_payment_pdf
import logging

logger = logging.getLogger(__name__)

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
                        body {{ 
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f4f7f9;
                        }}
                        .email-container {{
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #ffffff;
                            border-radius: 8px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        }}
                        h1, h2 {{
                            color: #1f2937;
                            text-align: center;
                        }}
                        p {{
                            color: #4b5563;
                            font-size: 16px;
                            line-height: 1.6;
                        }}
                        .info-box {{
                            margin-top: 20px;
                            padding: 15px;
                            background-color: #f9fafb;
                            border-radius: 8px;
                            border: 1px solid #e5e7eb;
                        }}
                        .info-box strong {{
                            color: #333;
                        }}
                        .button-wrapper {{
                            text-align: center;
                            margin-top: 20px;
                        }}
                        .button {{
                            display: inline-block;
                            padding: 12px 24px;
                            background-color: #4CAF50;
                            color: #fff;
                            font-size: 16px;
                            font-weight: bold;
                            text-decoration: none;
                            border-radius: 5px;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        }}
                        .button:hover {{
                            background-color: #45a049;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <h1>Dear {landlord_name},</h1>
                        <h2>Invoice for Reservation</h2>
                        <p>Thank you for your reservation! Below are the details of your booking:</p>
                        
                        <div class="info-box">
                            <strong>Invoice ID:</strong> {response_data['reservation']['id']}<br>
                            <strong>Start Date:</strong> {response_data['reservation']['start_date']}<br>
                            <strong>End Date:</strong> {response_data['reservation']['end_date']}<br>
                            <strong>Total Price:</strong> ${response_data['reservation']['total_price']}<br>
                            <strong>Number of Nights:</strong> {response_data['reservation']['number_of_nights']}<br>
                            <strong>Guests:</strong> {response_data['reservation']['guests']}
                        </div>
                        
                        <div class="info-box">
                            <strong>Property Name:</strong> {response_data['reservation']['property']['name']}<br>
                            <strong>Location:</strong> {response_data['reservation']['property']['address']}<br>
                            <strong>Property ID:</strong> {response_data['reservation']['property']['id']}
                        </div>
                        
                        <div class="button-wrapper">
                            <a href="https://www.diplomaroad.pro/myreservations/" class="button">View Invoice</a>
                        </div>
                        
                        <p>If you have any questions, feel free to contact us. Thank you for choosing our service!</p>
                    </div>
                </body>
            </html>
        """

        # Generate the PDF from response_data
        pdf_buffer = generate_payment_pdf(response_data)

        # Send the email with the PDF
        send_message(
            subject=subject,
            message='',
            html_message=html_message,
            from_email=from_email,
            to_email=to_email,
            attachment_name='reservation_invoice.pdf',
            attachment_content=pdf_buffer.getvalue(),
            attachment_mime_type='application/pdf'
        )

    except Exception as e:
        logger.error(f"Error sending invoice email: {e}")
