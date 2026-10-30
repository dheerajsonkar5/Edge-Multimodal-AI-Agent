import random
import datetime


class DashboardWidgets:

    def __init__(self):

        self.people_count = 0
        self.face_count = 0
        self.alerts = 0

    def update(self):

        self.people_count = random.randint(0, 8)

        self.face_count = random.randint(0, 8)

        self.alerts += random.randint(0, 1)

    def summary(self):

        self.update()

        return {

            "People": self.people_count,

            "Faces": self.face_count,

            "Alerts": self.alerts,

            "Time": str(datetime.datetime.now())
        }

    def today_alerts(self):

        return {

            "date": str(datetime.date.today()),

            "alerts": self.alerts
        }