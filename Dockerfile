FROM alpine:3.16

# Install dependencies
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Download the latest PocketBase binary
RUN curl -L -o pocketbase.zip https://github.com/pocketbase/pocketbase/releases/download/v0.22.4/pocketbase_0.22.4_linux_amd64.zip && \
    unzip pocketbase.zip && \
    rm pocketbase.zip

# Make port 8090 available to the world outside this container
EXPOSE 8090

# Run PocketBase
CMD ["./pocketbase", "serve", "--http=0.0.0.0:8090", "--dir=/app/data"]
