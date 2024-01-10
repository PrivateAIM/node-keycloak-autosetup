import json
import logging
import secrets
import time

import click
from jinja2 import Environment, PackageLoader, select_autoescape
from keycloak import KeycloakOpenIDConnection, KeycloakAdmin, KeycloakOpenID


@click.command()
@click.option(
    "--kc-server-url",
    default="http://localhost:8080/",
    help="URL to Keycloak instance.",
)
@click.option(
    "--kc-master-realm-name",
    default="master",
    help="Name of master realm within Keycloak.",
)
@click.option(
    "--verify/--no-verify",
    default=True,
    help="Enable certificate validation for encrypted traffic.",
)
@click.argument("kc_admin_username", metavar="ADMIN_USERNAME")
@click.argument("kc_admin_password", metavar="ADMIN_PASSWORD")
def setup_keycloak(
    kc_admin_username: str,
    kc_admin_password: str,
    kc_server_url: str,
    kc_master_realm_name: str,
    verify: bool,
) -> None:
    # set up jinja env
    env = Environment(
        loader=PackageLoader("project"),
        autoescape=select_autoescape(),
    )

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("kcsetup")

    kc_admin_oid = KeycloakOpenIDConnection(
        server_url=kc_server_url,
        username=kc_admin_username,
        password=kc_admin_password,
        realm_name=kc_master_realm_name,
        verify=verify,
    )

    kc_admin = KeycloakAdmin(connection=kc_admin_oid)

    # load realm payload
    realm_payload = json.loads(env.get_template("realm.json").render())

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
    client_payload = json.loads(
        env.get_template("client.json").render(
            client_secret=secrets.token_urlsafe(24),  # creates 32 char url-safe secret
            client_secret_creation_time=int(time.time()),
        )
    )

    kc_client_id = client_payload["clientId"]
    kc_client_secret = client_payload["secret"]
    logger.info("Read client `%s`", kc_client_id)

    # create client and perform sanity check
    kc_client_uuid = kc_admin.create_client(client_payload, skip_exists=True)
    kc_client = kc_admin.get_client(kc_client_uuid)

    assert kc_client["clientId"] == kc_client_id
    assert kc_client["secret"] == kc_client_secret

    logger.info("Client successfully created")

    # check whether authentication works
    kc_client_oid = KeycloakOpenID(
        server_url=kc_server_url,
        realm_name=realm_name,
        client_id=kc_client_id,
        client_secret_key=kc_client_secret,
        verify=verify,
    )

    auth_token = kc_client_oid.token(grant_type="client_credentials")
    assert auth_token is not None

    logger.info("Authentication successful")

    print("")
    print("=" * 64)
    print("")
    print(f"Realm: {realm_name}")
    print(f"Client ID: {kc_client_id}")
    print(f"Client Secret: {kc_client_secret}")
    print("")
    print("" * 64)
    print("")


if __name__ == "__main__":
    setup_keycloak()
