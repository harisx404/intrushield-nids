"""GeoIP enrichment backed by a MaxMind GeoLite2 database.

The enricher opens the GeoLite2-City database at startup when it is available
and looks up geographic metadata for source IPs. The database file is not
redistributable, so in development (and in CI) it is usually absent — in that
case the enricher degrades gracefully to empty results rather than failing.
"""

from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass

import structlog

try:  # geoip2 is a runtime dependency; guard the import so tests can run without it.
    import geoip2.database
    import geoip2.errors

    _GEOIP2_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only when the dep is missing
    _GEOIP2_AVAILABLE = False

log = structlog.get_logger(__name__)


@dataclass(frozen=True)
class GeoLocation:
    """Geographic metadata resolved for an IP address."""

    country: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None


_EMPTY = GeoLocation()


class GeoIPEnricher:
    """Resolve IP addresses to geographic metadata via GeoLite2.

    A single :class:`geoip2.database.Reader` is opened once and reused; the
    reader is thread-safe for concurrent reads. When the database is missing or
    unreadable the enricher stays operational and returns empty locations.
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._reader: geoip2.database.Reader | None = None

        if not _GEOIP2_AVAILABLE:
            log.warning("geoip_disabled", reason="geoip2 not installed")
            return
        if not os.path.exists(db_path):
            log.warning("geoip_disabled", reason="database not found", path=db_path)
            return
        try:
            self._reader = geoip2.database.Reader(db_path)
            log.info("geoip_ready", path=db_path)
        except (OSError, ValueError) as exc:
            log.warning("geoip_disabled", reason="database unreadable", error=str(exc))

    def lookup(self, ip_address: str) -> GeoLocation:
        """Return geographic metadata for ``ip_address``.

        Private, loopback, and reserved addresses never hit the database — they
        have no meaningful public geolocation. Unknown or unresolvable
        addresses return an empty :class:`GeoLocation`.
        """
        if not self._reader or not ip_address:
            return _EMPTY

        try:
            if ipaddress.ip_address(ip_address).is_global is False:
                return _EMPTY
        except ValueError:
            # Not a parseable IP (e.g. "Unknown") — nothing to look up.
            return _EMPTY

        try:
            response = self._reader.city(ip_address)
        except geoip2.errors.AddressNotFoundError:
            return _EMPTY
        except (ValueError, geoip2.errors.GeoIP2Error) as exc:
            log.debug("geoip_lookup_failed", ip=ip_address, error=str(exc))
            return _EMPTY

        return GeoLocation(
            country=response.country.iso_code,
            city=response.city.name,
            latitude=response.location.latitude,
            longitude=response.location.longitude,
        )

    def lookup_country(self, ip_address: str) -> str | None:
        """Convenience wrapper returning just the ISO country code."""
        return self.lookup(ip_address).country

    def close(self) -> None:
        """Close the underlying database reader, if open."""
        if self._reader:
            self._reader.close()
            self._reader = None
