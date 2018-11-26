import smtplib
from email.mime.text import MIMEText


def send_email(to_addr, subject, body):
    """
    使用公共邮箱发送邮件
    :param to_addr: 收件地址
    :param subject: 主题
    :param body: 邮件内容
    :return: 返回邮件主题名称（尾部自动附加用作防垃圾邮件拦截的UUID值）
    """
    import settings
    import uuid
    sender_name = settings.EMAIL.get('USERNAME')
    receivers = to_addr if isinstance(to_addr, list) else [to_addr]
    # 在主题后面加UUID，防止邮件被判定为垃圾邮件
    uid = uuid.uuid4().__str__()
    subject = '{} - {}'.format(subject, uid)
    body = '{} - {}'.format(body, uid)
    message = _build_email_header(sender_name, receivers, subject, body)

    with _get_email_server() as server:
        server.login(settings.EMAIL.get('USERNAME'), settings.EMAIL.get('SMTP_PASSWORD'))
        server.sendmail(settings.EMAIL.get('USERNAME'), receivers, message)
        print('邮件已发送到：{}'.format(to_addr))
        return subject, body


def _get_email_server():
    import settings
    server = smtplib.SMTP_SSL(settings.EMAIL.get('SMTP_SERVER'), settings.EMAIL.get('SSL_PORT'))
    return server


def _build_email_header(sender, receivers, subject, body):
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ','.join(receivers)
    message['Subject'] = subject
    message['X-Coremail-Locale'] = 'zh_CN'
    message['X-Mailer'] = 'Coremail Webmail Server Version SP_ntes V3.5 build'
    return message.as_string()
