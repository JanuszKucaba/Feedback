import smtplib
from email.mime.text import MIMEText
from data import port, smtp_server, login, password, sender_email, receiver_mail


def send_mail(customer, dealer, rating, comments):
    message = f'<h3>Nowe zgłoszenie opinii</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>'

    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Opel Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_mail

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_mail, msg.as_string())

    return 'Wysłałem maila'