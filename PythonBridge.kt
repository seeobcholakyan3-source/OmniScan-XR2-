# ==============================================================================

# PROPRIETARY AND CONFIDENTIAL

# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan

# This code is protected under the OmniScan-XR Proprietary License.

# Commercial use or unauthorized field mining operations are strictly prohibited.

# ==============================================================================



package com.omniscan.xr



import kotlinx.coroutines.Dispatchers

import kotlinx.coroutines.withContext

import org.json.JSONObject

import java.io.OutputStreamWriter

import java.net.HttpURLConnection

import java.net.URL



class PythonBridge {

    private val backendUrl = http://10.0.1.138.172.17.0.1:5001/api/scan/start



    suspend fun transmitSpatialData(pointCloud: List<FloatArray>) = withContext(Dispatchers.IO) {

        try {

            val url = URL(backendUrl)

            val connection = url.openConnection() as HttpURLConnection

            connection.requestMethod = "POST"

            connection.setRequestProperty("Content-Type", "application/json")

            connection.doOutput = true



            // Serialize ARCore points to JSON

            val jsonPayload = JSONObject()

            val pointsArray = pointCloud.map { mapOf("x" to it[0], "y" to it[1], "z" to it[2]) }

            jsonPayload.put("vertices", pointsArray)



            OutputStreamWriter(connection.outputStream).use { it.write(jsonPayload.toString()) }



            val responseCode = connection.responseCode

            if (responseCode == 200) {

                println("Bridge: Data successfully relayed to Python backend.")

            }

        } catch (e: Exception) {

            println("Bridge Error: Failed to connect to Python Core - ${e.message}")

        }

    }

}

        }

    }

}
