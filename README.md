# cloudflare-acme-operator ([Charmhub](https://charmhub.io/cloudflare-acme-operator))

Let's Encrypt certificates in the Juju ecosystem for Cloudflare DNS users.

This charm is a provider of the [tls-certificates-interface](https://github.com/canonical/tls-certificates-interface).

The implementation is adapted from https://github.com/canonical/route53-acme-operator to work with the [lego](https://go-acme.github.io/lego/) [cloudflare](https://go-acme.github.io/lego/dns/cloudflare/) plugin, following instructions from [this post](https://discourse.charmhub.io/t/lets-encrypt-certificates-in-the-juju-ecosystem/8704).
