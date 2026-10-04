"""
SwasthyaSetu AI - Application Entry Point
Run with: python run.py  (from any directory)
"""

import os
import sys

# Ensure the swasthyasetu/ directory is on sys.path regardless of
# where the user calls python from.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Ensure UTF-8 output on Windows so startup message prints cleanly
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print("=" * 55)
    print("  SwasthyaSetu AI - Rural Preventive Healthcare")
    print("  Powered by IBM Granite / Watsonx.ai")
    print(f"  Running on : http://localhost:{port}")
    print(f"  Health check: http://localhost:{port}/api/health")
    print("=" * 55)
    app.run(host="0.0.0.0", port=port, debug=debug)
