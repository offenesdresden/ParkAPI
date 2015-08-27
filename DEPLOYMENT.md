# Deployment

Currently 2 stages exist production and staging.
We use [capistrano](http://capistranorb.com/) to deploy servers.

## How to deploy a new version to staging

TODO: automatic pull from master on commit

## How to deploy a new version to production
* Merge master into stable, run tests

```
$ cap production release:prepare
```

* Push release and switch back to master

```
$ cap production release:push
```

* Deploy new code from stable

```
$ cap production deploy
```

* To reset stable branch to offenesdresden/stable (abort release)

```
$ cap production release:reset
```

* Nothing works after deploy? Don't freak out use to step back

```
$ cap production deploy:rollback
```

* Download/upload configuration

```
$ cap production config:download
$ cap production config:upload
```
