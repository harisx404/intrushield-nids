"""System-wide constants."""

from enum import Enum


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Ordered from least to most severe; used for threshold comparisons.
SEVERITY_ORDER = [
    Severity.INFO,
    Severity.LOW,
    Severity.MEDIUM,
    Severity.HIGH,
    Severity.CRITICAL,
]


def severity_at_least(severity: str, threshold: str) -> bool:
    """Return True if `severity` ranks at or above `threshold`.

    Unknown severities are treated as the lowest rank so they never satisfy a
    threshold accidentally.
    """
    order = [s.value for s in SEVERITY_ORDER]
    try:
        return order.index(severity) >= order.index(threshold)
    except ValueError:
        return False


class AlertStatus(str, Enum):
    NEW = "NEW"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class EventType(str, Enum):
    ALERT = "alert"
    DNS = "dns"
    HTTP = "http"
    TLS = "tls"
    FLOW = "flow"
    STATS = "stats"


# Map Suricata priority to our Severity enum
PRIORITY_MAP = {
    1: Severity.CRITICAL,
    2: Severity.HIGH,
    3: Severity.MEDIUM,
    4: Severity.LOW,
}

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20
