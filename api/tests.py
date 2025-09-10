from django.core.mail import send_mail

send_mail(
    subject="Hello from Django 🎉",
    message="This is a test email",
    from_email="jayanthkonanki82@gmail.com",
    recipient_list=["jkonanki@gitam.in"],
)
