import subprocess
import logging

logger = logging.getLogger(__name__)

class SuricataManager:
    @staticmethod
    def reload_rules() -> bool:
        """Send SIGHUP or use suricatasc to reload rules."""
        try:
            result = subprocess.run(
                ["suricatasc", "-c", "reload-rules"], 
                capture_output=True, text=True, check=True
            )
            logger.info("Suricata rules reloaded successfully.")
            return True
        except FileNotFoundError:
            logger.warning("suricatasc not found. Are you in a container?")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to reload rules: {e.stderr}")
            return False
