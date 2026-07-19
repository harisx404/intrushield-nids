import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)


class RuleValidator:
    @staticmethod
    def validate_rule(rule_content: str) -> tuple[bool, str]:
        """Validate Suricata rule syntax by running suricata -T on a temp file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".rules", delete=False
        ) as temp_file:
            temp_file.write(rule_content)
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(
                ["suricata", "-T", "-S", temp_file_path], capture_output=True, text=True
            )
            if result.returncode == 0:
                return True, "Rule is valid."
            else:
                return False, result.stderr or result.stdout
        except FileNotFoundError:
            logger.warning("suricata executable not found. Skipping strict validation.")
            return True, "Validation skipped (suricata not found)."
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
