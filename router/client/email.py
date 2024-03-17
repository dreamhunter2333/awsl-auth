from smtplib import SMTP

with SMTP("domain.org") as smtp:
    smtp.noop()
