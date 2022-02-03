from django.core import mail
from api_yamdb.settings import EMAIL_ADDRESS
from django.utils.crypto import get_random_string


def send_ccmail(recipient, code):
    mail.send_mail(
        subject='Get the confirmation code',
        message=f'Your confirmation code is {code}',
        from_email=EMAIL_ADDRESS,
        recipient_list=[recipient],
        fail_silently=False,
    )
    print(mail.outbox[0].body)


def generate_confirmation_code():
    return get_random_string(length=32)