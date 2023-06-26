import subprocess


def origin_remote_url():
    raw_remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'])
    raw_remote = raw_remote.decode().replace('\n', '')

    if raw_remote.startswith('https://'):
        return raw_remote

    stripped_remote = raw_remote.replace('git@github.com:', '').replace('.git', '')
    org = stripped_remote.split('/')[0]
    repo_name = stripped_remote.split('/')[1]

    return f'https://github.com/{org}/{repo_name}'

