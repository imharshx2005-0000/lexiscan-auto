#!/usr/bin/env bash
set -e

# Start the Flask backend in the background on a fixed internal port.
# It's only reachable from inside this container (bound to 127.0.0.1),
# so it never needs to be exposed publicly.
export FLASK_INTERNAL_PORT=5000
python app.py &

# Give Flask a moment to come up before Streamlit starts sending it requests.
sleep 3

# Streamlit is the public-facing process. Render injects $PORT — we must
# bind to it (and to 0.0.0.0) or Render's health check will never pass.
export BACKEND_URL="http://127.0.0.1:${FLASK_INTERNAL_PORT}"
streamlit run streamlit_app.py \
  --server.port="${PORT:-8501}" \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --browser.gatherUsageStats=false
