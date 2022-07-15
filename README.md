# Tailscale on Fly.io

Forked from <https://github.com/patte/fly-tailscale-exit>.

## Setup

You'll need to modify `Dockerfile`, `fly.toml` and `start.sh` before you deploy to Fly.io.

### `Dockerfile`

Change `ARG TSFILE=tailscale_1.26.2_amd64.tgz` to whatever the latest on <https://pkgs.tailscale.com/stable/>.

### `fly.toml`

Change `app = "com-stepbrobd-vpn"` to you own app name.

### `setup.sh`

Chage `--hostname=com-stepbrobd-vpn-${FLY_REGION}` to your preferred hostname.

## Deploy

Make sure you have a Tailscale account, a Fly.io account, and a computer with `flyctl` installed.

1. Go to <https://login.tailscale.com/admin/settings/keys> to generate a new key.

2. Run `fly launch` to initiallize the app, do not deploy at this step.

3. Run `fly secrets set TAILSCALE_AUTH_KEY=YOUR-KEY`, replace `YOUR_KEY` with the key generated in step 1.

4. Run `fly deploy`.

5. Scale the app if you want, see documentation <https://fly.io/docs/reference/regions/#fly-io-regions>.
