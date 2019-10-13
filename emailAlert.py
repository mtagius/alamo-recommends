import smtplib
import configs

 
def send(from_addr, to_addr_list, subject, message,
login, password=configs.emailPassword, smtpserver='smtp.gmail.com:587'):
        header  = 'From: %s' % from_addr
        header += '\nTo: %s' % ','.join(to_addr_list)
        header += '\nSubject: %s' % subject
        message = header + "\n" + message
    
        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()

def htmlSend(from_addr, to_addr, subject, message,
login, password=configs.emailPassword, smtpserver='smtp.gmail.com:587'):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login, password)
        problems = server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()