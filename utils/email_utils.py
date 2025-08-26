from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(context, to_email):
    from_email = settings.DEFAULT_FROM_EMAIL

    # Render HTML content
    html_content = render_to_string("email.html", context)

    # Create plain text version by stripping HTML tags
    text_content = strip_tags(html_content)

    # Create email message
    email = EmailMultiAlternatives(
        subject="Reset Password - QrGen Pro",
        body=text_content,
        from_email=from_email,
        to=[to_email],
    )

    # Attach HTML content
    email.attach_alternative(html_content, "text/html")

    # Send email
    return email.send()
