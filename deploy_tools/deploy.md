## Staging Deploy
on local:
```sh
git push
cd deploy_tools
fab -H adisak01234@adisak-superlists-staging.xyz deploy
```
on server as root:
```sh
sudo systemctl restart gunicorn-adisak-superlists-staging.xyz
```
on local:
```sh
STAGING_SERVER=adisak-superlists-staging.xyz python manage.py test functional_tests
```

## Live Deploy
on local:
```sh
fab -H adisak01234@adisak-superlists.xyz deploy
```
on server as root:
```sh
sudo service gunicorn-adisak-superlists.xyz restart
```