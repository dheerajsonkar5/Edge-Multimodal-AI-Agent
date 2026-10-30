import random


class DashboardCharts:

    def __init__(self):

        self.cpu = []
        self.people = []
        self.alerts = []

    def update(self):

        self.cpu.append(random.randint(10, 90))
        self.people.append(random.randint(0, 8))
        self.alerts.append(random.randint(0, 5))

        if len(self.cpu) > 30:
            self.cpu.pop(0)

        if len(self.people) > 30:
            self.people.pop(0)

        if len(self.alerts) > 30:
            self.alerts.pop(0)

    def cpu_chart(self):

        self.update()

        return self.cpu

    def people_chart(self):

        return self.people

    def alert_chart(self):

        return self.alerts

    def summary(self):

        self.update()

        return {

            "cpu": self.cpu,

            "people": self.people,

            "alerts": self.alerts
        }