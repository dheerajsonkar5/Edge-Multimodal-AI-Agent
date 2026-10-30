import cv2
from core.logger import logger


class MonitorService:

    def __init__(
        self,
        camera_service,
        frame_processor,
        alert_service=None,
        report_service=None,
        database=None,
        reasoning_engine=None,
    ):
        self.camera = camera_service
        self.processor = frame_processor
        self.alert = alert_service
        self.report = report_service
        self.database = database
        self.reasoning = reasoning_engine
        self.running = False

    def start(self):
        """Start monitoring."""
        if self.running:
            logger.info("Monitoring already running.")
            return

        self.camera.open()
        self.running = True
        logger.info("Monitoring Started")

    def stop(self):
        """Stop monitoring."""
        self.running = False
        self.camera.release()
        cv2.destroyAllWindows()
        logger.info("Monitoring Stopped")

    def process_frame(self):
        """
        Read one frame, process it and display it.
        This should be called continuously from main.py.
        """

        if not self.running:
            return

        frame = self.camera.read_frame()

        if frame is None:
            logger.warning("Camera frame is None")
            return

        processed_frame, result = self.processor.process(frame)

        try:

            report = (
                self.reasoning.analyse(result)
                if self.reasoning
                else str(result)
            )

            if self.report:
                self.report.save(report)

            if self.database:
                try:
                    self.database.insert_event(report)
                except Exception:
                    pass

            if self.alert:
                if len(result.get("faces", [])) == 0:
                    self.alert.trigger_breach_alert()

        except Exception as e:
            logger.exception(e)

        cv2.imshow("Edge Multimodal AI Agent", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.stop()

    def status(self):
        return {
            "running": self.running
        }