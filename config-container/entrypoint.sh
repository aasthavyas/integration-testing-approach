#!/bin/sh

# Copy config.json to a shared volume
cp /config.json /shared-volume/

# Keep the container running
tail -f /dev/null
