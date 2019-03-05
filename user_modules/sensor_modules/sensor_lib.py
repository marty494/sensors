import smtplib
import datetime
import sys
import socket

PI_SERVER = socket.gethostname()

# Email constants
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = 'martinjohndavey@gmail.com'
# PASSWORD = 'zelwduaehgrfwemt'
PASSWORD = 'bjofdzffmaaluvpw' # pi_watersoft App Password
RECIPIENT = 'martinjohndavey@gmail.com'

# Error handling constants
SEND_EMAIL = True
DO_NOT_SEND_EMAIL = False
FATAL_ERROR = True
NON_FATAL_ERROR = False

def send_email(subject, text):
    try:
	smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(USERNAME, PASSWORD)

	subject = '[' + PI_SERVER + '] ' + subject
	text = '[' + PI_SERVER + '] ' + text

	header = 'To:' + RECIPIENT + '\n' + 'From: ' + USERNAME
	header = header + '\n' + 'Subject:' + subject + '\n'
	msg = header + '\n' + text + ' \n\n'
	smtpserver.sendmail(USERNAME, RECIPIENT, msg)
	smtpserver.close()
    except:
	handle_error('send_email', 'subject="' + subject + '", text="' + text + '"')

def __error_handler(app_name, message, exit_required, email_required):
    try:
	now = datetime.datetime.now()
	error_type = 'FATAL ERROR' if exit_required else 'ERROR'

	write_to_file(app_name, message, 'err')

	if email_required:
		send_email(error_type + ' in ' + app_name, message)

	if exit_required:
		sys.exit()

    except Exception as e:
	print('DISASTER in __error_handler("' + app_name + '", "' + message + 
		'", [' + error_type + '], Email Required=' + str(email_required) +
		' : [' + str(e) + ']')
	sys.exit()


def handle_fatal_error(app_name, message):
	__error_handler(app_name, message, True, False);

def handle_fatal_error_and_email(app_name, message):
	__error_handler(app_name, message, True, True);

def handle_error(app_name, message):
	__error_handler(app_name, message, False, False);

def handle_error_and_email(app_name, message):
	__error_handler(app_name, message, False, True);


def write_to_file(app_name, data, file_ext):
    try:
	now = datetime.datetime.now()
	filename = now.strftime('%Y%m%d') + '-' + app_name + '.' + file_ext
	f = open(filename, 'a+')
	f.write(now.strftime('%Y-%m-%d,%H:%M,') + str(data) + "\n")
	f.close()
    except:
	if file_ext == 'err':
		raise ValueError('ERROR writing to error file')
	else:
		handle_fatal_error_and_email('write_to_file', 'data="' + str(data) + '", file_ext="' + file_ext + '"')
