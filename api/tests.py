
# ------------------
# brevo transactional emailing\
# ------------------
# Include the Brevo library\
from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.conf import settings
import brevo_python 
code = '''
# Configure API key authorization: api-key
configuration = brevo_python.Configuration()
configuration.api_key['api-key'] =   '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'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api-key'] = 'Bearer'
# Configure API key authorization: partner-key
#configuration = brevo_python.Configuration()
#configuration.api_key['partner-key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['partner-key'] = 'Bearer'

# create an instance of the API class
api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
send_smtp_email = brevo_python.SendSmtpEmail(to=[{"email":"jkonanki@gitam.in","name":"jayanth"}], template_id=4, params={"name": "John", "surname": "Doe"}, headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", "charset": "iso-8859-1"}) # SendSmtpEmail | Values to send a transactional email

try:
    # Send a transactional email
    api_response = api_instance.send_transac_email(send_smtp_email)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")'''

def send_mail():
    exec(code,globals())
send_mail()




