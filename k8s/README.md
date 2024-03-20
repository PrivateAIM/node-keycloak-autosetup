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

The [Keycloak deployment file](keycloak-deployment.yaml) contains a config map which sets up
initial access credentials, the default realm and clients.
Applying the deployment will spawn two pods: one running Keycloak and one using the Keycloak Admin
CLI to configure Keycloak before sleeping indefinitely.

To change the admin credentials, modify `kc_admin_username` and `kc_admin_username`.
To change the default realm name, modify `kc_init_realm_name`.
To add or remove clients, modify `kc_init_clients`.
Entries of this key must be formatted as `<client_id>:<client_secret>`.
