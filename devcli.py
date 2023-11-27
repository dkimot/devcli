import app.github as github
import app.fly as fly
import app.linear as linear
import click
import time
import os
import subprocess
import tomllib

with open(".devcli.toml", "rb") as f:
    config = tomllib.load(f)

@click.group()
@click.version_option()
def cli():
    pass

@cli.command()
def apm():
    app_signal_id = config['apm']['app_signal_id']
    app_signal_org = config['apm']['app_signal_org']
    app_signal_url = f'https://appsignal.com/{app_signal_org}/sites/{app_signal_id}/dashboard'
    open_url(app_signal_url)


@cli.command()
def bg():
    open_url(config['deployed_url'] + "/super_admin/sidekiq")


@cli.command()
def deploy():
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    revision = revision.decode().replace('\n', '')

    print(f'Deploying revision {revision}')
    command = f'fly deploy -e APP_REVISION={revision}'

    print('running ' + command)
    os.system(command)

@cli.command()
def logsnag():
    logsnag_project_id = config['logsnag']['project_id']
    logsnag_url = f'https://app.logsnag.com/dashboard/{logsnag_project_id}/feed'
    open_url(logsnag_url)

@cli.group()
def gh():
    pass

@gh.command('open', help='Open Github repo.')
def gh_open():
    gh_url = github.origin_remote_url()
    open_url(gh_url)

@gh.command('prs', help='Open Github pr\'s.')
def gh_prs():
    gh_prs_url = f'{github.origin_remote_url()}/pulls'
    open_url(gh_prs_url)

@cli.command()
def logs():
    mezmo_app_name = config['logs']['mezmo_app_name']
    mezmo_url = f'https://app.mezmo.com/bc866d7f52/logs/view?q=app%3A{mezmo_app_name}'

    open_url(mezmo_url)

@cli.command()
def metrics():
    open_url(fly.metrics_url())

@cli.command()
def open():
    deployed_url = config['deployed_url']
    open_url(deployed_url)

@cli.command()
def tasks():
    project_management = config['project_management']
    provider = project_management['provider']
    match provider:
        case 'linear':
            linear.open_linear_url(linear.team_url(project_management['linear_org'], project_management['linear_team']))

@cli.command()
def tunnel():
    port = config['tunnel']['port']

    ip_v4 = get_ip("4")
    ip_v6 = get_ip("6")

    print(f'ngrok http {port} --cidr-allow {ip_v4}/32 --cidr-allow {ip_v6}/32 --domain kimotodev.ngrok.io')
    os.system(f'ngrok http {port} --cidr-allow {ip_v4}/32 --cidr-allow {ip_v6}/32 --domain kimotodev.ngrok.io')

def open_url(url):
    print("Opening " + url)
    time.sleep(1)
    os.system(f'open "{url}"')

def get_ip(version):
    result = os.popen(f"curl -{version} https://icanhazip.com")
    raw = result.read()
    return raw.replace("\n", "")
