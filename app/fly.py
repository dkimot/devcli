import tomllib

with open(".devcli.toml", "rb") as f:
    config = tomllib.load(f)

def metrics_url():
    with open("fly.toml", "rb") as f:
        fly_config = tomllib.load(f)

    app_name = fly_config["app"]
    org_id = config["fly"]["org_id"]

    return f'https://fly-metrics.net/d/fly-app/fly-app?orgId={org_id}&var-app={app_name}'
