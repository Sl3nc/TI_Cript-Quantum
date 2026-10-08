ARG LIBOQS_VERSION=0.14.0

FROM --platform=linux/amd64 debian:bookworm-slim AS builder

ARG LIBOQS_VERSION

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ninja-build \
        git \
        ca-certificates \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch "${LIBOQS_VERSION}" https://github.com/open-quantum-safe/liboqs.git /tmp/liboqs \
    && cmake -S /tmp/liboqs -B /tmp/liboqs/build -GNinja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DBUILD_SHARED_LIBS=OFF \
        -DOQS_BUILD_ONLY_LIB=ON \
    && cmake --build /tmp/liboqs/build \
    && cmake --install /tmp/liboqs/build \
    && rm -rf /tmp/liboqs

WORKDIR /build
COPY CMakeLists.txt ./
COPY src ./src
COPY tests ./tests
COPY profiling ./profiling

RUN cmake -S . -B build -GNinja -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build \
    && cmake -S . -B build-profile -GNinja -DCMAKE_BUILD_TYPE=Release -DBENCH_PROFILE=ON \
    && cmake --build build-profile --target benchmark

FROM --platform=linux/amd64 debian:bookworm-slim AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends libssl3 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

COPY --from=builder /build/build/benchmark /app/benchmark
COPY scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["--algorithm", "KEM", "--volume", "10000"]

FROM runtime AS profiling

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/build-profile/benchmark /app/benchmark
COPY scripts/entrypoint-profile.sh /app/entrypoint-profile.sh
RUN chmod +x /app/entrypoint-profile.sh

USER appuser

ENTRYPOINT ["/app/entrypoint-profile.sh"]
CMD ["--algorithm", "KEM", "--volume", "10000"]
