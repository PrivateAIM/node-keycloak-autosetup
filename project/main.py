import click
from keycloak import KeycloakOpenIDConnection, KeycloakAdmin


@click.command()
@click.option("--kc-server-url", default="http://localhost:8080/")
@click.option("--kc-master-realm-name", default="master")
@click.option("--verify/--no-verify", default=True)
@click.argument("kc_admin_username")
@click.argument("kc_admin_password")
def setup_keycloak(
    kc_admin_username: str,
    kc_admin_password: str,
    kc_server_url: str,
    kc_master_realm_name: str,
    verify: bool,
) -> None:
    kc_oid = KeycloakOpenIDConnection(
        server_url=kc_server_url,
        username=kc_admin_username,
        password=kc_admin_password,
        realm_name=kc_master_realm_name,
        verify=verify,
    )

    kc_admin = KeycloakAdmin(connection=kc_oid)
    print(kc_admin.get_realms())


if __name__ == "__main__":
    setup_keycloak()
