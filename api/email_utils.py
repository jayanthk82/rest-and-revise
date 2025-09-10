
import resend

resend.api_key = "re_aE59Yuhj_78eUxoXefPoQA6Kq9LjbUEW6"

params: resend.Emails.SendParams = {
  "from": "Acme <jayanthkonanki82@gmail.com>",
  "to": ["jkonanki@gitam.in"],
  "subject": "hello world",
  "html": "<p>it works!</p>"
}

email = resend.Emails.send(params)
print(email)