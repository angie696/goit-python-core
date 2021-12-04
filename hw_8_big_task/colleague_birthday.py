from datetime import datetime, timedelta

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekdays_massive = [[], [], [], [], [], [], []]


def find_birthday_boy(text_file):
    today = datetime.today()
    start_date = today - timedelta(days=today.weekday())
    all_weekdays = [(start_date + timedelta(days=idx)).strftime("%d.%m") for idx in range(-2, 7)]
    days_important = [all_weekdays[:3]] + all_weekdays[3:]
    with open(text_file, 'r') as all_users:
        for user in all_users:
            name_and_birth = user.split(":")
            name = name_and_birth[0]
            birth = name_and_birth[1].split('.')
            birthday = datetime(year=today.year, month=int(birth[1]), day=int(birth[0]))
            birthday = birthday.strftime("%d.%m")
            for day in range(len(days_important)):
                if birthday in days_important[day]:
                    weekdays_massive[day].append(name)
    return weekdays_massive


def get_birthdays_per_week():
    birthday_boy = find_birthday_boy('scientist_birthday')
    for idx in range(len(birthday_boy)):
        print(f"{WEEKDAYS[idx]:<9}: {', '.join(birthday_boy[idx])}")


if __name__ == "__main__":
    get_birthdays_per_week()
