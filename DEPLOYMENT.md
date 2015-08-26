# Deployment

Currently 2 stages exist production and staging.
We use [capistrano](http://capistranorb.com/) to deploy servers.

## How to deploy a new version to staging

TODO: automatic pull from master on commit

## How to deploy a new version to production
1. Merge master into stable, run tests

```
$ cap production release:prepare
```

2. Push release and switch back to master

```
$ cap production release:push
```

3. Deploy new code from stable

```
$ cap production deploy
```
