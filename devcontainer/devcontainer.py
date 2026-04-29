# ==============================================================================

# PROPRIETARY AND CONFIDENTIAL

# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan

# This code is protected under the OmniScan-XR Proprietary License.

# Commercial use or unauthorized field mining operations are strictly prohibited.

# ==============================================================================

{

    "name": "OmniScan-XR Cloud Core",

    "image": "mcr.microsoft.com/devcontainers/python:3.10",

    "customizations": {

        "vscode": {

            "extensions": [

                "ms-python.python",

                "ms-azuretools.vscode-docker"

            ]

        }

    },

    "postCreateCommand": "pip install -r requirements.txt",

    "remoteEnv": {

        "LOCAL_BACKEND_URL": "http://localhost:5001"

    }

}
