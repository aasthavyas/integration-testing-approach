# Use a lightweight base image
FROM alpine:3.14

# Copy the configuration file into the container
COPY ./config/config.json /config.json

# Entrypoint script
COPY ./config-container/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
