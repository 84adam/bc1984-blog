#!/bin/sh
# Preview the published site on this machine. Drafts are not included.
set -eu
cd "$(dirname "$0")"

port="${PORT:-1984}"
bind="${BIND:-127.0.0.1}"

if command -v hugo >/dev/null 2>&1; then
  hugo_bin=$(command -v hugo)
elif [ -n "${HUGO:-}" ] && [ -x "${HUGO}" ]; then
  hugo_bin=${HUGO}
elif [ -x /tmp/hugo ]; then
  hugo_bin=/tmp/hugo
else
  echo "Hugo is not installed." >&2
  echo "Download the Linux amd64 tarball from https://github.com/gohugoio/hugo/releases/latest and put the hugo binary on your PATH." >&2
  exit 1
fi

python3 scripts/stage.py

echo "Preview: http://${bind}:${port}/"
echo "About:   http://${bind}:${port}/donate/"
echo "Press Ctrl-C to stop. Run this again after editing an article."

# Serve from memory so this preview does not rewrite public/.
exec "$hugo_bin" server \
  --bind "$bind" \
  --port "$port" \
  --baseURL "http://${bind}:${port}/" \
  --appendPort=false \
  --renderToMemory
