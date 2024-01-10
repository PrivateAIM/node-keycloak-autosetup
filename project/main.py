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
def setup_keycloak(
    kc_admin_username: str,
    kc_admin_password: str,
    kc_realm_file: str,
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
    logger.info('Read realm "%s" (%s) payload', realm_name, realm_id)

    # create realm and perform sanity check
    kc_admin.create_realm(realm_payload, skip_exists=True)
    kc_realm = kc_admin.get_realm(realm_name)

    assert kc_realm["id"] == realm_id
    assert kc_realm["realm"] == realm_name

    logger.info("Realm successfully created")


if __name__ == "__main__":
    setup_keycloak()
