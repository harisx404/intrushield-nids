import asyncio
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.detection.eve_parser import EveParser
from backend.detection.alert_manager import AlertManager

logger = logging.getLogger(__name__)

class EVELogHandler(FileSystemEventHandler):
    def __init__(self, file_path: str, alert_manager: AlertManager):
        self.file_path = file_path
        self.alert_manager = alert_manager
        self._file = None
        self._open_file()

    def _open_file(self):
        if os.path.exists(self.file_path):
            self._file = open(self.file_path, "r")
            self._file.seek(0, os.SEEK_END)

    def on_modified(self, event):
        if event.src_path == self.file_path:
            if not self._file:
                self._open_file()
            if self._file:
                for line in self._file:
                    parsed = EveParser.parse_line(line)
                    if parsed:
                        alert_data = EveParser.extract_alert_data(parsed)
                        if alert_data:
                            try:
                                loop = asyncio.get_event_loop()
                                loop.create_task(self.alert_manager.process_parsed_alert(alert_data))
                            except RuntimeError:
                                logger.error("No event loop available for EVE log processing")

class EVELogWatcher:
    def __init__(self, file_path: str, alert_manager: AlertManager):
        self.file_path = file_path
        self.alert_manager = alert_manager
        self.observer = Observer()

    def start(self):
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError:
                logger.warning(f"Could not create directory {directory}")
                return
            
        handler = EVELogHandler(self.file_path, self.alert_manager)
        self.observer.schedule(handler, path=directory, recursive=False)
        self.observer.start()

    def stop(self):
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
