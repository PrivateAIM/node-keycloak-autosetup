# Keycloak development setup tool

This repository contains a tool for setting up Keycloak for FLAME node development purposes.

## Prerequisites

[Poetry](https://python-poetry.org/), [Docker](https://docs.docker.com/engine/install/)
and [Docker Compose](https://docs.docker.com/compose/install/) must be installed and working.

## Installation

Clone this repository.
In a terminal, navigate to the repository's root directory.
Run `poetry install`.

## Usage

In a terminal, navigate to the [docker subdirectory](./docker) and run `docker compose up -d`.
This will start a development instance of Keycloak on port 8080 of your machine.
Next, change to the root directory and run `poetry shell`.
You can then run `kcsetup --help` to view the tool's options.

```
$ kcsetup --help
Usage: kcsetup [OPTIONS] ADMIN_USERNAME ADMIN_PASSWORD

Options:
  --kc-server-url TEXT         URL to Keycloak instance.
  --kc-master-realm-name TEXT  Name of master realm within Keycloak.
  --verify / --no-verify       Enable certificate validation for encrypted
                               traffic.
  --help                       Show this message and exit.
```

The Keycloak server URL and master realm name are set to http://localhost:8080 and "master" by default.
If you use the Compose file in this repository to start Keycloak, these options do not need to be configured.

You can then invoke the setup tool with the admin username and password.
The tool will create a new realm with service accounts enabled, as well as a client within that realm with its own
unique secret.

```
$ kcsetup admin admin
INFO:kcsetup:Read realm `flame` (78af1a45-369d-4336-adc9-d2e85e6e64f0) payload
INFO:kcsetup:Realm successfully created
INFO:kcsetup:Read client `flame-client`
INFO:kcsetup:Client successfully created
INFO:kcsetup:Authentication successful

================================================================

Realm: flame
Client ID: flame-client
Client Secret: yxZpcsCNinhPqW_k9RZkxnfzuCXLzx9B

================================================================
```

You can use the client ID and secret with a regular OAuth client credentials grant to authenticate against Keycloak.
