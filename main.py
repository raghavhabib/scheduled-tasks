import smtplib
import random
import datetime as dt
import pandas
import os

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

# ---------------------------- FIND TODAY'S BIRTHDAYS ------------------------------- #
birthdays = pandas.read_csv("birthdays.csv")

today = dt.datetime.now()
# Keep only the rows whose month AND day match today (works for any number of people)
todays_birthdays = birthdays[(birthdays["month"] == today.month) & (birthdays["day"] == today.day)]
print(todays_birthdays)

# ---------------------------- SEND THE EMAILS ------------------------------- #
# Only connect to Gmail if someone actually has a birthday today
if not todays_birthdays.empty:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # encrypt the connection
        connection.login(user=my_email, password=password)

        #to loop / iterate over the selected rows
        for (index, birthday_person) in todays_birthdays.iterrows():
            birthday_persons_name = birthday_person["name"]
            birthday_persons_email = birthday_person["email"]

            # Pick a random letter template and put the person's name in it
            letter_number = random.randint(1, 3)
            with open(f"letter_templates/letter_{letter_number}.txt", "r") as letter_file:
                body_of_email = letter_file.read().replace("[NAME]", birthday_persons_name)

            connection.sendmail(
                from_addr=my_email,
                to_addrs=birthday_persons_email,
                msg=f"Subject:Happy Birthday {birthday_persons_name}!\n\n{body_of_email}".encode("utf-8")
            )
