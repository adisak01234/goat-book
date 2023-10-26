import random
from fabric import task, Connection

REPO_URL = 'https://github.com/adisak01234/goat-book.git'


def exists(c, file_path):
    return c.run(f'test -e {file_path}', warn=True).exited == 0


@task
def deploy(c):
    site_folder = f'/home/{c.user}/sites/{c.host}'
    c.run(f'mkdir -p {site_folder}')
    current_commit = c.local('git log -n 1 --format=%H').stdout
    with c.cd(site_folder):
        _get_latest_source(c, current_commit)
        _update_virtualenv(c)
        _create_or_update_dotenv(c)
        _update_static_files(c)
        _update_database(c)


def _get_latest_source(c, current_commit):
    if exists(c, '.git'):
        c.run('git fetch')
    else:
        c.run(f'git clone {REPO_URL} .')
    c.run(f'git reset --hard {current_commit}')


def _update_virtualenv(c):
    if not exists(c, '.venv/bin/pip'):
        c.run(f'python3.11 -m venv .venv')
    c.run('./.venv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv(c):

    current_contents = c.run('cat .env').stdout if exists(c, '.env') else None

    for x in ['DJANGO_DEBUG=y', f'SITENAME={c.host}']:
        if current_contents is None or x not in current_contents:
            c.run(f"echo {x} >> .env")
    if current_contents is None or 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        c.run(f'echo DJANGO_SECRET_KEY={new_secret} >> .env')




def _update_static_files(c):
    c.run('./.venv/bin/python manage.py collectstatic --noinput')


def _update_database(c):
    c.run('./.venv/bin/python manage.py makemigrations --noinput')
    c.run('./.venv/bin/python manage.py migrate --noinput')
