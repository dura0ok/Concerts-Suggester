FROM alpine:latest
LABEL authors="durachok"

RUN apk add --no-cache bash curl python3
WORKDIR /app/indexer

COPY indexer.sh .
COPY . .
CMD ["/bin/bash", "./indexer.sh"]