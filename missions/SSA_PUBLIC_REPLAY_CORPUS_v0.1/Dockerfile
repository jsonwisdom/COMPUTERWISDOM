FROM ubuntu@sha256:678c6550cc43645e08669028bc177f50be4e7c5b8cca677067b1914d4afc7a03

WORKDIR /replay

COPY README.md Dockerfile ./
COPY contracts ./contracts
COPY receipts ./receipts
COPY tests ./tests

RUN chmod 0555 tests/verify-layout.sh

ENTRYPOINT ["/bin/bash", "tests/verify-layout.sh"]
