DjangoNextAppBackend Documentation
Overview

DjangoNextAppBackend is a robust backend application built using Django, designed to support the Djanobnb platform. It manages user authentication, property listings, customer inquiries, payment processing, and other essential backend operations. This backend leverages modern tools and libraries, including Django REST Framework, Celery, and Stripe, to ensure scalability and reliability.
Key Features

The backend provides the following key features:

    User Management: Secure authentication with role-based permissions and profile management, including support for avatars.
    Property Management: Full CRUD functionality for managing property listings, along with a daily property report system.
    Customer Inquiries: Handles customer inquiries with features for creation, status updates, severity levels, and assignment to customer service agents.
    Payment Processing: Integration with Stripe for secure payment handling, including invoice generation and email notifications.
    Asynchronous Tasks: Uses Celery for background task management, such as sending emails and generating reports.
    Email Notifications: A custom email handler for dispatching messages with attachments and support for both text and HTML content.

Application Structure
User Accounts Module

The useraccounts module is responsible for user authentication, role-based permissions, and profile management. The User model extends Django's built-in AbstractBaseUser and PermissionsMixin, adding fields such as role, avatar, and Stripe customer ID. Roles like admin, customer_service, and user are used to determine permissions and capabilities. Users can upload avatars, which are accessible via a URL for frontend integration.
Property Management Module

The property module supports full CRUD functionality for property listings. Additionally, a daily HTML report of newly added properties is generated and emailed to administrators using Celery. This ensures that the system stays updated with the latest property data.
Inquiries Module

The inquiries module handles customer inquiries, allowing for creation, management, and assignment. Each inquiry includes fields such as subject, message, status, and severity. Serializers are used to validate and handle data, ensuring smooth operations. Status transitions and agent assignments are validated to maintain data integrity.
Stripe Integration

The my_stripe module manages payment-related functionality, including processing payments and generating invoices. A dedicated task generates PDF invoices and emails them to users, ensuring a seamless payment experience.
Email Handling

The backend includes a custom send_message function that handles email sending. This function supports plain text and HTML emails and allows attachments, providing flexibility for various email use cases.
Asynchronous Task Management

Celery is integrated for managing background tasks efficiently. The application uses Celery to run tasks such as email dispatch and report generation. Scheduled tasks, like the daily property report, are managed with Celery Beat to ensure timely execution.
Installation and Configuration

To set up the backend, follow these steps:

    Clone the repository and install dependencies.
    Configure environment variables, including DJANGO_SETTINGS_MODULE, ADMIN_USER_EMAIL, and Stripe API keys.
    Run database migrations to set up the schema.
    Start Celery workers and the beat scheduler to enable task execution.

The application uses Django’s ORM for database interactions, and email functionality can be configured via the settings file for production use.
Best Practices

    Use serializers for data validation and transformation to ensure consistency.
    Follow established patterns for creating tasks and sending emails.
    Regularly update and validate user roles and inquiry workflows to maintain system integrity.

Conclusion

This backend application serves as a scalable and feature-rich foundation for the Djanobnb platform. It efficiently handles complex operations such as user management, property handling, and payment processing while maintaining code quality and reliability. For further details, explore the specific modules and codebase. Contributions are welcome to enhance and extend its functionality.
