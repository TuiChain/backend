from django.core.mail import send_mail
from django.template import loader

def send_email(subject="Tuichain", message="Hi there!", from_email=None, to_email="tuichain2020@gmail.com", html_file=None):
    html_message = None
    if html_file is not None:
        html_message = loader.render_to_string(html_file)

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to_email],
        html_message=html_message,
        fail_silently=False,
    )
