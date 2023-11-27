import tomllib

def metrics_url(org_id):
    with open("fly.toml", "rb") as f:
        fly_config = tomllib.load(f)

    app_name = fly_config["app"]

    return f'https://fly-metrics.net/d/fly-app/fly-app?orgId={org_id}&var-app={app_name}'
