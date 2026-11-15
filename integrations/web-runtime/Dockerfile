ARG BASE=agentflow-community-runtime:e0cef9118f61
FROM ${BASE}
USER root
RUN mv /opt/kc-mcp/scripts/configure.py /opt/kc-mcp/scripts/upstream_configure.py
COPY root_config.py /opt/kc-mcp/scripts/configure.py
COPY patch_upstream.py /opt/agentflow/patch_upstream.py
RUN python3 /opt/agentflow/patch_upstream.py
LABEL org.agentflow.role="isolated-community-web-runtime" \
      org.agentflow.upstream="repairer5812/webjjonku@e0cef9118f612ed148c6db2806f1f8b6ea2661ad"
ENV AGENTFLOW_ROOT_LAYOUT=separate-roots-v1
USER node
