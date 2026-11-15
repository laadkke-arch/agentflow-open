ARG BASE=agentflow-community-runtime:e0cef9118f61
FROM python:3.12-slim-bookworm AS python_runtime
FROM ${BASE}
USER root
COPY --from=python_runtime /usr/local /usr/local
RUN python3 -c "import sys, ssl, sqlite3, ctypes; assert sys.version_info[:2] == (3, 12)" && node --version
RUN mv /opt/kc-mcp/scripts/configure.py /opt/kc-mcp/scripts/upstream_configure.py
COPY root_config.py /opt/kc-mcp/scripts/configure.py
COPY patch_upstream.py /opt/agentflow/patch_upstream.py
RUN python3 /opt/agentflow/patch_upstream.py
LABEL org.agentflow.role="isolated-community-web-runtime" \
      org.agentflow.upstream="repairer5812/webjjonku@e0cef9118f612ed148c6db2806f1f8b6ea2661ad"
ENV AGENTFLOW_ROOT_LAYOUT=separate-roots-v1
USER node
