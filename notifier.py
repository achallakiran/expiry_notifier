from datetime import datetime
from datetime import timedelta
import os, sys

def send_mail(notification_email,notification_text,diff_days):

    mail_cmd='echo "'+notification_text.replace('<days>',str(diff_days))+'"|mail -s '+'"'+notification_text.replace('<days>',str(diff_days))+'" '+ notification_email
    os.system(mail_cmd)

def get_diff_days(reference_date, days_expiry_frequency):

    current_date=datetime.today().date()
    next_expiry_date=reference_date

    while next_expiry_date<current_date:
        next_expiry_date=reference_date+timedelta(days=days_expiry_frequency)

    diff_days=int((next_expiry_date-current_date).days%days_expiry_frequency)
    return diff_days

if __name__=="__main__":

    try:
        conf_loc=sys.argv[1]
        conf_file=open(conf_loc,"r")

        #ignore header
        next(conf_file)

        for conf_line in conf_file:
            attribute_list=conf_line.split("|")
            reference_date=datetime.strptime(attribute_list[0].strip(),'%Y-%m-%d').date()
            buffer_days=int(attribute_list[1].strip())
            days_expiry_frequency=int(attribute_list[2].strip())
            notification_text=attribute_list[3].strip()
            notification_email=attribute_list[4].strip()

            diff_days=get_diff_days(reference_date, days_expiry_frequency)

            if diff_days<=buffer_days:
                send_mail(notification_email,notification_text,diff_days)

        conf_file.close()
    except:
        print "Issue in config file or line!!!"
