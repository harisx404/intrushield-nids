"""Unit tests for the GeoIP enricher's graceful-degradation behavior."""

from backend.detection.geoip_enricher import GeoIPEnricher, GeoLocation


def test_missing_database_degrades_to_empty(tmp_path):
    # No GeoLite2 DB on disk (the common dev/CI case) must not raise; every
    # lookup returns an empty location instead.
    enricher = GeoIPEnricher(str(tmp_path / "does-not-exist.mmdb"))

    assert enricher.lookup("8.8.8.8") == GeoLocation()
    assert enricher.lookup_country("8.8.8.8") is None


def test_empty_and_invalid_input_returns_empty(tmp_path):
    enricher = GeoIPEnricher(str(tmp_path / "does-not-exist.mmdb"))

    assert enricher.lookup("") == GeoLocation()
    assert enricher.lookup("not-an-ip") == GeoLocation()


def test_private_addresses_are_not_geolocated(tmp_path):
    # Even with a reader present these would short-circuit; with none present
    # the contract is simply "empty, never raise".
    enricher = GeoIPEnricher(str(tmp_path / "does-not-exist.mmdb"))

    for private_ip in ("192.168.1.10", "10.0.0.5", "127.0.0.1"):
        assert enricher.lookup(private_ip) == GeoLocation()
