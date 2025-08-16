# ------------------
# Create a campaign\
# ------------------
# Include the Brevo library\
from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.conf import settings
import brevo_python 
import os 
from django.conf import settings
from celery import shared_task
from .models import Summary

def send_mail(subject, message, recipient):
    # Configure API key authorization: api-key
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = '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'
    # create an instance of the API class
    api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
    send_smtp_email = brevo_python.SendSmtpEmail(
        to=[{"email": recipient['email'], "name": recipient['name']}],
        template_id=4,
        params={"name": "John", "surname": "Doe"},
        headers={
            "X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
            "charset": "iso-8859-1"
        }
    )  # SendSmtpEmail | Values to send a transactional email

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}") 


@shared_task
def send_summary_email(summary_id):
    """
    A background task to send a summary email using Brevo.
    """
    try:
        summary = Summary.objects.get(id=summary_id)
        user = summary.user
        subject = f"Your Daily Summary: {summary.summary_text[:30]}..."
        message = f"""
        Hi {user.username},

        Here is a summary you saved:
        {summary.summary_text}
        ---
        Original Text:
        {summary.original_text}
        """
        # The from_email must be your Brevo login email
        recipient = {'name':user.username,'email':user.email}
        send_mail(subject, message,recipient)

        return f"Email sent successfully to {user.email} for summary ID {summary_id}"
    except Summary.DoesNotExist:
        return f"Could not find summary with ID {summary_id}"
    

