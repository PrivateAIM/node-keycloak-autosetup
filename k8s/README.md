# Keycloak deployment

This directory contains files for setting up a development (and therefore **non-persistent**)
instance Keycloak in a k8s cluster.
Make sure you have a k8s cluster running and accessible, e.g. by
installing [minikube](https://minikube.sigs.k8s.io/docs/) on your local machine.

## Deploy to k8s

To deploy, simply run the following commands.

```
$ kubectl apply -f ./keycloak-deployment.yaml
$ kubectl apply -f ./keycloak-service.yaml
```

## Configure realm and clients

The [Keycloak deployment file](keycloak-deployment.yaml) contains secrets which set up
initial access credentials, the default realm and clients.
Applying the deployment will spawn an init container which generates a realm file and
puts it in the main container's import directory.

To change the admin credentials, modify `kc-admin-username` and `kc-admin-password`.
To change the default realm name, modify `kc-init-realm`.
To add or remove clients, modify `kc-init-clients`.
Entries of this key must be formatted as `<client_id>:<client_secret>`.

## Fetching access tokens

Once deployed, you can retrieve access tokens for each specified client using the
OAuth client credentials grant.
You can easily expose Keycloak with minikube using `minikube service keycloak-service`.

```
$ curl -q -X POST -d "grant_type=client_credentials&client_id=service1&client_secret=9dd01665c2f3f02f93c32d03bd854569f03cd62f439ccf9f0861c141b9d6330e" http://192.168.49.2:30842/realms/flame/protocol/openid-connect/token
{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQTWM1QmZQVFVaM0NsVVhta3JzMXV3U0wyWHFvUThOSV9fZ1lMTVEzcjQ4In0.eyJleHAiOjE3MTA5Mzc2NjIsImlhdCI6MTcxMDkzNzM2MiwianRpIjoiYzBjZmU1NTYtZjMyNC00MzdlLWJjYTEtYzZmYjVlYzJlNjU2IiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguNDkuMjozMDg0Mi9yZWFsbXMvZmxhbWUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYjkxYzFlZDgtYzNiMS00ZGNkLTkyNDQtOGU2YjkzZWZmNWQ3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2VydmljZTEiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1mbGFtZSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRIb3N0IjoiMTAuMjQ0LjAuMSIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1zZXJ2aWNlMSIsImNsaWVudEFkZHJlc3MiOiIxMC4yNDQuMC4xIiwiY2xpZW50X2lkIjoic2VydmljZTEifQ.tQOKV4nGFHXFB-PHm3YKq4KspMGDlRW4Q9RHr3lTPoC1O-i3bDFgfOBxJUBd7jn__1fdZrWAdfVbMVajE_m-B2nQO1VepJvpNmDuPHubDxosiz0XFuiqhJxxCl8h-gNfb3cIPa-XjhQmbXf-7QGFCZ2vxqDnoulwacQv8Hmcnd_HNOsXi7SC5O-cXPh2OcIRR7zJV9c3hceTqbgOZb6ty_3OwvVCIE9fNhKYyV8YDw-i8zK0LLRox4rkRBiaqPbPEkBbzk-9d8YTBgzDm4D3uW-kj2I1Rd7y15J5oChGpkylTzfH0T_y-h-UiaO8LvNqV7_EEYInwDxG8Ib7AkIlBQ","expires_in":300,"refresh_expires_in":0,"token_type":"Bearer","not-before-policy":0,"scope":"profile email"}
```

If you have [jq](https://github.com/jqlang/jq) installed, you can filter out the access token directly.

```
$ curl -X POST -d "grant_type=client_credentials&client_id=service1&client_secret=9dd01665c2f3f02f93c32d03bd854569f03cd62f439ccf9f0861c141b9d6330e" http://192.168.49.2:30842/realms/flame/protocol/openid-connect/token 2>/dev/null | jq -r '.access_token'
eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQTWM1QmZQVFVaM0NsVVhta3JzMXV3U0wyWHFvUThOSV9fZ1lMTVEzcjQ4In0.eyJleHAiOjE3MTA5Mzc3MDIsImlhdCI6MTcxMDkzNzQwMiwianRpIjoiMTZkNTI3MzItNjE0Ni00YjQ5LWI4MjMtYTBjNmEzYTQ1ZGI4IiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguNDkuMjozMDg0Mi9yZWFsbXMvZmxhbWUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYjkxYzFlZDgtYzNiMS00ZGNkLTkyNDQtOGU2YjkzZWZmNWQ3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2VydmljZTEiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1mbGFtZSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRIb3N0IjoiMTAuMjQ0LjAuMSIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1zZXJ2aWNlMSIsImNsaWVudEFkZHJlc3MiOiIxMC4yNDQuMC4xIiwiY2xpZW50X2lkIjoic2VydmljZTEifQ.Je6KelV_WLBO5w0KbD9BZS1dx3NUkqVqh9OHp-hVjb0SjzraCTTB2WOV8gc9-AqCV_z4tt1hBS2MQoIGLBUwiNPh1gAeJ9GzRcpMdWvBaXjCU3JOCjJ3_JwwR4cqBqH0PedqkTKcvnTTqIObWqOx0wR4HYeTHnKlCS1bdzuJdGv4qntGOnJh8WKK4E7sB34awHETeuCDRa_PFV-Ri5TWDBTnbZVlEbsl_QN_n0DfUd5srERRIxR-i-uM4vOpWuxqC_TJgbRoFlk3J_RWIsw6UVT9-dNEFBqgC_xxdjor92orK77U8LrZE4jWbKLLLMDg9ZMkR5m37IDwprufKX1kmA
```
