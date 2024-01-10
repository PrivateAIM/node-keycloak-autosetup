import json
import logging

import click
from keycloak import KeycloakOpenIDConnection, KeycloakAdmin


@click.command()
@click.option("--kc-server-url", default="http://localhost:8080/")
@click.option("--kc-master-realm-name", default="master")
@click.option("--verify/--no-verify", default=True)
@click.argument("kc_admin_username")
@click.argument("kc_admin_password")
@click.argument("kc_realm_file")
@click.argument("kc_client_file")
def setup_keycloak(
    kc_admin_username: str,
    kc_admin_password: str,
    kc_realm_file: str,
    kc_client_file: str,
    kc_server_url: str,
    kc_master_realm_name: str,
    verify: bool,
) -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("kcsetup")

    kc_oid = KeycloakOpenIDConnection(
        server_url=kc_server_url,
        username=kc_admin_username,
        password=kc_admin_password,
        realm_name=kc_master_realm_name,
        verify=verify,
    )

    kc_admin = KeycloakAdmin(connection=kc_oid)

    # load realm payload
    with open(kc_realm_file, mode="r", encoding="utf-8") as f:
        realm_payload = json.load(f)

    realm_id = realm_payload["id"]
    realm_name = realm_payload["realm"]
    logger.info("Read realm `%s` (%s) payload", realm_name, realm_id)

    # create realm and perform sanity check
    kc_admin.create_realm(realm_payload, skip_exists=True)
    kc_realm = kc_admin.get_realm(realm_name)

    assert kc_realm["id"] == realm_id
    assert kc_realm["realm"] == realm_name

    logger.info("Realm successfully created")

    # switch realms
    kc_admin.change_current_realm(realm_name)

    # load client payload
    with open(kc_client_file, mode="r", encoding="utf-8") as f:
        client_payload = json.load(f)

    kc_client_id = client_payload["clientId"]
    kc_client_secret = client_payload["secret"]
    logger.info("Read client `%s`", kc_client_id)

    # create client and perform sanity check
    kc_client_uuid = kc_admin.create_client(client_payload, skip_exists=True)
    kc_client = kc_admin.get_client(kc_client_uuid)

    assert kc_client["clientId"] == kc_client_id
    assert kc_client["secret"] == kc_client_secret

    logger.info("Client successfully created")


if __name__ == "__main__":
    setup_keycloak()
