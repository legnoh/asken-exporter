#!/bin/bash
set -e

# Execute Display settings
Xvfb :99 &

# Then exec the container's main process (what's set as CMD in the Dockerfile).
exec "$@"
