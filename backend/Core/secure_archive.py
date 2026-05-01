# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026
# This code is protected under the OmniScan-XR Proprietary License.
# Commercial use or unauthorized field mining operations are strictly prohibited.
# ==============================================================================

import sqlite3
from fastapi import FastAPI, HTTPException
from SecureArchive import SecureArchive

app = FastAPI(
    title="OmniScan-XR Backend API",
    description="API for retrieving encrypted and decrypted mineral detection hits.",
    version="1.0.0"
)

archive = SecureArchive()


def fetch_hits():
    """Fetches all stored hits from the SQLite database."""
    try:
        conn = sqlite3.connect(archive.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, encrypted_coords, mineral, timestamp FROM hits ORDER BY timestamp DESC"
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/hits", summary="Get encrypted scan results")
def get_hits():
    """
    Returns all stored hits with encrypted coordinates.
    """
    rows = fetch_hits()
    return [
        {
            "id": r[0],
            "encrypted_coords": r[1],
            "mineral": r[2],
            "timestamp": r[3]
        }
        for r in rows
    ]


@app.get("/hits/decrypted", summary="Get decrypted scan results")
def get_hits_decrypted():
    """
    Returns all stored hits with decrypted latitude/longitude coordinates.
    """
    rows = fetch_hits()

    decrypted_results = []
    for r in rows:
        try:
            decrypted_coords = archive.cipher.decrypt(r[1].encode()).decode()
        except Exception:
            decrypted_coords = "DECRYPTION_FAILED"

        decrypted_results.append(
            {
                "id": r[0],
                "coords": decrypted_coords,
                "mineral": r[2],
                "timestamp": r[3]
            }
        )

    return decrypted_results


@app.get("/", summary="Health check")
def root():
    return {"status": "OK", "message": "OmniScan-XR backend is running"}
