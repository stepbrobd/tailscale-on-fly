# Tailscale on Fly.io

![GitHub Action Status](https://github.com/StepBroBD/Tailscale-on-Fly.io/actions/workflows/auto-update.yml/badge.svg)

Forked from <https://github.com/patte/fly-tailscale-exit>.

## Setup

You'll need to modify `Dockerfile`, `fly.toml` and `start.sh` before deploy to Fly.io.

### `Dockerfile`

Optional: Double check the version specified matches the latest version available at <https://pkgs.tailscale.com/stable/>.

GitHub Action will auto update Tailscale version on Sundays.

### `fly.toml`

Change `app = "com-stepbrobd-vpn"` to your preferred app name.

### `setup.sh`

Change `--hostname=com-stepbrobd-vpn-${FLY_REGION}` to your preferred hostname.

## Deployment

Make sure you have a Tailscale account, a Fly.io account, and a computer with `flyctl` installed.

1. Go to <https://login.tailscale.com/admin/settings/keys> to generate a new auth key.

2. Run `fly launch` to initialize the app (do NOT deploy at this step).

3. Run `fly secrets set TAILSCALE_AUTH_KEY=YOUR-KEY`, replace `YOUR_KEY` with the key generated in step 1.

4. Run `fly deploy`.

5. Scale the app if you want, see documentation <https://fly.io/docs/reference/regions/#fly-io-regions>.

## Redeployment

`redeploy.py` will delete exit node machines on your Tailnet matching criteria and redeploy based on your local `flyctl` configuration.
