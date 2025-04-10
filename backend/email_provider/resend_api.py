# resend_api.py

import resend

def send_email(email, template, link):
    custom_email_html = fill_info(template, link)
    email_data = {
        "to": email,
        "subject": template['subject'],
        "html": custom_email_html,
        "from": template['from']
    }
    email_id = resend.Emails.send(email_data)
    print(email, email_id)


def fill_info(template, link):
    custom_email = template['html'].replace("{{ link }}", link)
    return custom_email
