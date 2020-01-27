import smtplib, ssl, config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn
from filoModules.Tools import Tools

class Email:
    @staticmethod
    def get_admin_email(to_addr, voornaam, subject, content):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = config.get_email_config().sender_mail
        message["To"] = to_addr

        text = """\
        Hoi {voornaam},

        {content}

        (Bericht verstuurd via Admin Panel)

        Met vriendelijke groet,
        Het Findlock Team
        """.format(
            content=content,
            voornaam=voornaam
            )

        html = Tools.read_txt_to_str("filoModules/Emails/admin_mail.html").replace("<!voornaam!>", voornaam).replace("<!content!>", content)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        return message
    @staticmethod
    def get_register_email(to_addr, auth_code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Findlock - Verify"
        message["From"] = config.get_email_config().sender_mail
        message["To"] = to_addr
        hostname = config.get_hostname()

        text = """\
        Hoi,

        Welkom bij Findlock!

        Bedankt voor uw aanmelding bij Findlock.

        Om veiligheidsredenen vragen wij u uw aanmelding compleet te maken door op de onderstaande linkt te klikken. Uw account wordt dan geactiveerd en u kunt meteen gebruik gaan maken van Findlock.

        Aanmelding Bevestigen
        https://{hostname}/auth/verify/{auth_code}


        Met vriendelijke groet,
        Het Findlock Team
        """.format(auth_code=auth_code, hostname=hostname)

        html = Tools.read_txt_to_str("filoModules/Emails/register_mail.html").replace("<!hostname!>", hostname).replace("<!auth_code!>", auth_code)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        return message

    @staticmethod
    def send_email(to_addr, message):
        context = ssl.create_default_context()
        email_config = config.get_email_config()
        try:
            with smtplib.SMTP_SSL(email_config.server, email_config.port, context=context) as server:
                server.login(email_config.sender_mail, email_config.password)
                server.sendmail(email_config.sender_mail, to_addr, message.as_string())
            return m_LogicReturn.f_success_msg("Email sent!")
        except:
            return m_LogicReturn.f_error_msg("Can't send email")