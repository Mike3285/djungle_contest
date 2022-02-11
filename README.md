# Djungle Contest API V 2.0

## Prerequisites:
Project has been made and was tested with the following environment:
- Python 3.9+
- Linux 5.15+

### Instructions:

1. Clone the repo
2. `cd djungle_contest`
3. Install required packages with `pip install -r requirements.txt`
4. Install the required cronjob with `python3 manage.py make_cronjobs`
   - This will append a cronjob for the `root` user by default
   - You can change user by changing the value of `CRON_USER` string in `djungle_contest/settings.py:127`
5. Create you contest or contests in the admin
6. Add a prize for each contest you created in the admin
7. "Winning moments" table will be made when you create the prize
   - These tables will be refreshed by the cronjob every day at 0.00
8. Run the project locally with `python3 manage.py runserver`