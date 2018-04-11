#!/usr/bin/env python

import optparse
import sys
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE
from email.Utils import formatdate
from email import Encoders


def main():
    ''' Email client - can send through specific mail server, add attachment, TLS etc. '''
    # All the options accepted by the script
    usage_line='%prog -f env_from -t env_to -s subject -H smtp-host -F from -T to -r reply -R return-address, -d debug_level -p port_number, -D date, -e helo, -S tls, -a attach, -b body -c certificate -k privatekey'
    p = optparse.OptionParser(description='email client', prog='emailer',
                              version='0.1a', usage=usage_line)
    p.add_option("-f", "--env_from", dest="env_from", action="store", help="envelop from address for MTA")
    p.add_option("-t", "--env_to", dest="env_to", action="store", help="envelop to address for MTA")
    p.add_option("-s", "--subject", dest="subject", action="store", type="string", help="subject")
    p.add_option("-D", "--date", dest="date", action="store", help="date for MUA")
    p.add_option("-H", "--host", dest="host", action="store", help="smtp server hostname")
    p.add_option("-e", "--ehlo", dest="ehlo", action="store", help="helo or helo")
    p.add_option("-p", "--port", dest="port", type="int", action="store", help="smtp port number")
    p.add_option("-F", "--From", dest="From", action="store", help="from address for MUA")
    p.add_option("-T", "--to", dest="to", action="store", help="to address for MUA")
    p.add_option("-r", "--reply", dest="reply", action="store", help="reply address")
    p.add_option("-R", "--Return", dest="Return", action="store", help="Return-to address")
    p.add_option("-S", "--tls", dest="tls", action="store", help="tls - enables TLS")
    p.add_option("-d", "--debug", dest="debug", type="int", action="store", help="debug level")
    p.add_option("-a", "--attach", dest="attach", action="store", help="path to attachment file")
    p.add_option("-b", "--body", dest="body", action="store", help="Text or body of message")
    p.add_option("-C", "--cc", dest="cc", action="store", help="cc")
    p.add_option("-B", "--bcc", dest="bcc", action="store", help="bcc")
    p.add_option("-c", "--cert", dest="cert", action="store", help="cert")
    p.add_option("-k", "--key", dest="key", action="store", help="key")
    p.set_defaults(host="localhost", subject="No subject", debug=0)
    options, arguments = p.parse_args()
    # To do: add validator for all options; feature - secure smtp : user authentication.
    # To do: use idioms - less if..else, make it readable; exception handling; class
    # multithreading (send single email through multiple smtp servers at the same time).
    # To do: bind IP address (source ip); use function generator
    if len(arguments) != 0:
        p.print_help()
        sys.exit(1)
    if not options.env_from and not options.From:
        p.error("From address not given")
        sys.exit(1)
    if not options.env_to and not options.to:
        p.error("To address not given")
        sys.exit(1)
    if not options.body:
        p.error("Email body not given")
        sys.exit(1)
    if options.attach:
        if os.path.isfile(options.attach):
            textfile = options.attach
            fp = open(textfile, 'rb')
            msg = MIMEText(fp.read())
            fp.close()
        else:
            print "Attachment file " + options.attach + " does not exist "
            sys.exit(1)
    if options.env_from:
        fromaddr = options.env_from
    else:
        if options.From:
            fromaddr = options.From
    if options.env_to:
        toaddrs = [options.env_to]
    else:
        if options.to:
            toaddrs = [options.to]
    if options.subject:
        subject = options.subject
    if options.host:
        smtpserver = options.host
    debuglevel = options.debug
    if options.body:
        body = options.body
    if options.date:
        mydate = options.date
    if options.port:
        port = options.port
    if options.From:
        From = options.From
    else:
        if options.env_from:
            From = options.env_from

    if options.to:
        to = [options.to]
    else:
        if options.env_to:
            to = [options.env_to]
    if options.reply:
        reply = options.reply
    if options.Return:
        Return = options.Return
    if options.tls:
        tls = options.tls
    if options.attach:
        attach = options.attach
    if options.ehlo:
        ehlo = options.ehlo
    if options.cc:
        cc = options.cc
    if options.bcc:
        bcc = options.bcc
    if options.cert:
        certfile = options.bcc
    if options.key:
        keyfile = options.bcc
    if not options.attach:
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n" % (fromaddr, ", ".join(toaddrs), subject, body))
        print "Message length is " + repr(len(msg))
        server = smtplib.SMTP(smtpserver)
        server.ehlo()
        if debuglevel:
            server.set_debuglevel(debuglevel)
        if options.tls and options.cert and options.key:
            server.starttls(keyfile, certfile)
        elif options.tls:
            server.starttls()
        server.sendmail(fromaddr, toaddrs, msg)
    else:
        msg = MIMEMultipart()
        msg['From'] = From
        msg['To'] = COMMASPACE.join(to)
        if options.cc:
            msg['Cc'] = options.cc
        if options.bcc:
            msg['BCc'] = options.bcc
        if options.reply:
            msg['Reply-to'] = options.reply
        if options.Return:
            msg['Return-path'] = options.Return
        if options.date:
            msg['Date'] = options.date
        else:
            msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(body))
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attach, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename = "%s"' % os.path.basename(attach))
        msg.attach(part)
        server = smtplib.SMTP(smtpserver)
        server.ehlo()
        if options.tls:
            server.starttls()
        if debuglevel:
            server.set_debuglevel(debuglevel)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


if __name__ == '__main__':
    sys.exit(main())
