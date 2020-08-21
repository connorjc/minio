# minio

Create a simple docker-compose.yml that instantiates a minio service, and a
python container that connects to minio to upload an object (maybe a small
sample image you bind mount into the container) into minio and then print to
standard out a "share url" that includes an expiration that is moderately
small -- shoot for 24 hours.
