#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import logging
from typing import Dict

import ops

from charms.acme_client_operator.v0.acme_client import AcmeClient
from ops.model import ActiveStatus, BlockedStatus

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)


class CloudflareAcmeOperatorCharm(AcmeClient):
    """Charm the service."""

    REQUIRED_CONFIG = ["CLOUDFLARE_EMAIL"]

    def __init__(self, *args):
        """Use the acme_client library to manage events."""
        super().__init__(*args, plugin="cloudflare")
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    @property
    def _cloudflare_email(self) -> str:
        return self.model.config.get("cloudflare_email")

    @property
    def _cloudflare_api_key(self) -> str | None:
        return self.model.config.get("cloudflare_api_key")

    @property
    def _cloudflare_dns_api_token(self) -> str | None:
        return self.model.config.get("cloudflare_dns_api_token")

    @property
    def _cloudflare_zone_read_api_token(self) -> str | None:
        return self.model.config.get("cloudflare_zone_read_api_token")

    @property
    def _cloudflare_http_timeout(self) -> str | None:
        return self.model.config.get("cloudflare_http_timeout")

    @property
    def _cloudflare_polling_interval(self) -> str | None:
        return self.model.config.get("cloudflare_polling_interval")

    @property
    def _cloudflare_propagation_timeout(self) -> str | None:
        return self.model.config.get("cloudflare_propagation_timeout")

    @property
    def _cloudflare_ttl(self) -> str | None:
        return self.model.config.get("cloudflare_ttl")

    @property
    def _plugin_config(self) -> Dict[str, str]:
        additional_config = {
            # email required also as CLOUDFLARE_EMAIL or CF_API_EMAIL for whatever reason in case of the Cloudflare plugin,
            # see https://go-acme.github.io/lego/dns/cloudflare/
            "CLOUDFLARE_EMAIL": self._email
        }
        if self._cloudflare_api_key:
            additional_config["CLOUDFLARE_API_KEY"] = self._cloudflare_api_key
        if self._cloudflare_dns_api_token:
            additional_config["CLOUDFLARE_DNS_API_TOKEN"] = self._cloudflare_dns_api_token
        if self._cloudflare_zone_read_api_token:
            additional_config["CLOUDFLARE_ZONE_API_TOKEN"] = self._cloudflare_zone_read_api_token
        if self._cloudflare_http_timeout:
            additional_config["CLOUDFLARE_HTTP_TIMEOUT"] = self._cloudflare_http_timeout
        if self._cloudflare_polling_interval:
            additional_config["CLOUDFLARE_POLLING_INTERVAL"] = self._cloudflare_polling_interval
        if self._cloudflare_zone_read_api_token:
            additional_config["CLOUDFLARE_ZONE_API_TOKEN"] = self._cloudflare_zone_read_api_token
        if self._cloudflare_propagation_timeout:
            additional_config[
                "CLOUDFLARE_PROPAGATION_TIMEOUT"
            ] = self._cloudflare_propagation_timeout
        if self._cloudflare_ttl:
            additional_config["CLOUDFLARE_TTL"] = self._cloudflare_ttl
        return additional_config

    def _validate_cloudflare_livedns_config(self) -> bool:
        if missing_config := [
            option for option in self.REQUIRED_CONFIG if not self._plugin_config[option]
        ]:
            msg = f"The following config options must be set: {', '.join(missing_config)}"
            self.unit.status = BlockedStatus(msg)
            return False

        if self._cloudflare_api_key is None and self._cloudflare_dns_api_token is None:
            self.unit.status = BlockedStatus(
                "Either cloudflare_api_key or cloudflare_dns_api_token config values must be set"
            )
            return False

        return True

    def _on_config_changed(self, _) -> None:
        if not self._validate_cloudflare_livedns_config():
            return
        if not self.validate_generic_acme_config():
            return
        self.unit.status = ActiveStatus()


if __name__ == "__main__":  # pragma: nocover
    ops.main(CloudflareAcmeOperatorCharm)
