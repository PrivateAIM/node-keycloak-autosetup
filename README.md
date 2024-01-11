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
You can then run `kcsetup -h` to view the tool's options.

```
$ kcsetup -h
Usage: kcsetup [OPTIONS] ADMIN_USERNAME ADMIN_PASSWORD

Options:
  --kc-server-url TEXT         URL to Keycloak instance.  [default:
                               http://localhost:8080/]
  --kc-master-realm-name TEXT  Name of master realm within Keycloak.
                               [default: master]
  --verify / --no-verify       Enable certificate validation for encrypted
                               traffic.  [default: verify]
  -r, --kc-realm-name TEXT     Name of realm within Keycloak to create.
                               [default: flame]
  -c, --kc-client-name TEXT    Name of client within Keycloak realm to create.
                               [default: flame-client]
  -h, --help                   Show this message and exit.
```

The Keycloak server URL and master realm name are set to http://localhost:8080 and "master" by default.
If you use the Compose file in this repository to start Keycloak, these options do not need to be configured.

You can then invoke the setup tool with the admin username and password.
If nothing else is specified, the tool will create a new realm called "flame" with service accounts enabled, as well as
a client within that realm called "flame-client" with its own unique secret.

```
$ kcsetup admin admin
INFO:kcsetup:Read realm payload, creating new realm `flame` (7e19937d-1bda-4560-ab5d-367547facddd)
INFO:kcsetup:Realm successfully created
INFO:kcsetup:Read client payload, creating new client `flame-client`
INFO:kcsetup:Client successfully created
INFO:kcsetup:Authentication successful

================================================================

Realm: flame

Client #1 ID: flame-client
Client #1 Secret: YGYzFdEIbXkAo1ZWsMQyCcaRVi0Ii2iR

================================================================
```

You can use the client ID and secret with a regular OAuth client credentials grant to authenticate against Keycloak.

To generate arbitrary realms and clients, use the `-r` and `-c` flags respectively.
You can use `-c` multiple times to generate multiple clients.
The following example creates a realm called "foo" with two clients called "bar" and "baz".

```
$ kcsetup -r foo -c bar -c baz admin admin
INFO:kcsetup:Read realm payload, creating new realm `foo` (ec953286-5139-4b47-8a5b-306ddef41cd8)
INFO:kcsetup:Realm successfully created
INFO:kcsetup:Read client payload, creating new client `bar`
INFO:kcsetup:Client successfully created
INFO:kcsetup:Authentication successful
INFO:kcsetup:Read client payload, creating new client `baz`
INFO:kcsetup:Client successfully created
INFO:kcsetup:Authentication successful

================================================================

Realm: foo

Client #1 ID: bar
Client #1 Secret: T7hWlbqdKXN12-nAe3WnghLc4xQihIcS

Client #2 ID: baz
Client #2 Secret: OjQi3Z7WNVLpYprHG7Stog3eQ_gilZdb

================================================================
```
