import threading
import platform
import winsound

from core.logger import logger


class AlertService:

    def __init__(self):
        self.lock = threading.Lock()

    def _beep(self, frequency: int, duration: int):
        try:
            if platform.system() == "Windows":
                winsound.Beep(frequency, duration)
        except Exception as e:
            logger.error(f"Beep Error: {e}")

    def _run(self, frequency, duration):

        threading.Thread(
            target=self._beep,
            args=(frequency, duration),
            daemon=True
        ).start()

    def critical_alert(self):

        logger.warning("CRITICAL ALERT Triggered")

        print("🚨 SECURITY BREACH DETECTED")

        self._run(1200, 500)

    def warning_alert(self):

        logger.warning("Warning Alert")

        print("⚠ Warning")

        self._run(800, 250)

    def posture_alert(self):

        logger.info("Posture Alert")

        print("🪑 Incorrect Posture")

        self._run(600, 200)

    def attention_alert(self):

        logger.info("Attention Alert")

        print("👀 Eyes Closed / Attention Lost")

        self._run(700, 300)

    def success_alert(self):

        logger.info("System OK")

        print("✅ Monitoring Running")

        self._run(500, 150)