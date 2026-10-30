from pathlib import Path
from datetime import datetime


class ReportGenerator:

    def __init__(self):

        self.report_dir = Path("reports")

        self.report_dir.mkdir(exist_ok=True)

    def save(self, report):

        filename = self.report_dir / (

            datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

        )

        with open(filename, "w", encoding="utf8") as f:

            f.write(report)

        return filename