from modules.request_ip import IpGetter
from configparser import ConfigParser
from modules.mail_sender import MailSender, NotificationSendingFailed
import logging
import os


def main():
    config = ConfigParser()
    ip_getter = IpGetter()
    logging.basicConfig(filename='logs/requester.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if os.path.exists('params.conf'):
        config.read('params.conf')
    else:
        try:
            config['Params'] = {}
            config_sect = config['Params']
            default_text = 'Write down the'
            config_sect['sender'] = input(f'{default_text} sender: ')
            config_sect['receiver'] = input(f'{default_text} receiver: ')
            config_sect['password'] = input(f'{default_text} password: ')
            config_sect['last_ip'] = ip_getter.get_ip()['ip']
        except KeyError as ex:
            text = 'A non-existent param used. Check the correctness.'
            logging.error(f'{ex} {text}')
            raise KeyError(f'KeyError: {text}')
        with open('params.conf', 'w') as f:
            config.write(f)
        return
    config_sect = config['Params']
    current_ip = ip_getter.get_ip()['ip']
    if config_sect['last_ip'] != current_ip:
        mail = MailSender()
        try:
            mail.send_email(config_sect['sender'], config_sect['receiver'], config_sect['password'],
                            u'My IP has changed', f'Hi!\nMy new IP is {current_ip}')
        except NotificationSendingFailed as ex:
            logging.error(ex)
            raise NotificationSendingFailed(ex)
        else:
            text = f'Email with a new IP is sent: {current_ip}'
            logging.info(text)
            print(text)
        config_sect['last_ip'] = current_ip
        with open('params.conf', 'w') as f:
            config.write(f)
    else:
        text = 'Same IP detected. No email is gonna be sent'
        logging.info(text)
        print(text)
    return


if __name__ == "__main__":
    main()
