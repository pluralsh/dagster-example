# Dagster User Code Example

This repo covers how to set up continuous deployment to a dagster instance using Plural and github actions.  There are a few main portions here:

* dagster user code defined in `app/` and specified in `dagster.yaml`
* github actions automation in `.github/workflows`

The core CD is done off git tags, you can create a new tagged release using the make target `release-vsn` in `Makefile`.

## Github Actions Authentication

You'll need to set up your plural user with the permissions to authenticate from github to support this setup of the `setup-plural` action.  This can be done easily by just running:

```bash
plural auth trust --issuer https://token.actions.githubusercontent.com --trust "repo:<your-dagster-repo>:ref:refs/tags/v.*"
```

This will set our auth provider to trust jwts from github actions with the given `sub` field regex (in a format generated by github, eg any tag prefixed with `v`).

## Configuring Your Dagster deployment

You'll also need to set the `dagster/helm/dagster/values.yaml` file appropriately to wire in this user code.  Dagster provides decent docs and we have some as well, but for this specific module structure, yaml like this will work:

```yaml
dagster:
  dagster:
    dagster-user-deployments:
      deployments:
      - dagsterApiGrpcArgs:
        - -m
        - etl
        envSecrets:
        - name: dagster-user-secrets
        image:
          pullPolicy: Always
          repository: ghcr.io/pluralsh/dagster-example
          tag: v0.0.12
        name: etl
        port: 4000
        resources:
          requests:
            cpu: 20m
            memory: 100Mi
      imagePullSecrets:
      - name: gh-creds
```

(Note that the `gh-creds` secret was created already with ghcr pull credentials, using a cloud provider registry usually automatically has pull creds provisioned).

## The `plural upgrade` command

The CD portion is ultimately triggered by an invocation of `plural upgrade` in `.github/workflows/publish.yaml#48`.  You can see it pipes in the structure from the `upgrade.yaml` file at the root of the repo and substitutes some env vars.  

You can theoretically modify this if there are any other attributes you'd like to configure with the update to your dagster instance, but for the most part just modifying the image tag should be sufficient like we do.

To better understand this command, you can run `plural upgrade --help`, but the tldr is you'll want your command to look something like:

```
plural upgrade YOUR_CLUSTER_NAME dagster -f -
```

in our example code here: https://github.com/pluralsh/dagster-example/blob/main/.github/workflows/publish.yml#L52 the cluster name (and upgrade queue name, which is the same in our api), is `plural`.