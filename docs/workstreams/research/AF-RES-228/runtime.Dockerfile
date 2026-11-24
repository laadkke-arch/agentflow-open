FROM debian:trixie-slim@sha256:8aa5a7bf5a1955bddbe7d74fcdd0b91ab30e74362a8b73af672b0481b35b44a0
RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates php-cli php-curl php-gmp php-intl php-mbstring php-sqlite3 php-xml php-zip python3 strace && rm -rf /var/lib/apt/lists/*
