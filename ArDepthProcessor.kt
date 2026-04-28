# ==============================================================================

# PROPRIETARY AND CONFIDENTIAL

# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan

# This code is protected under the OmniScan-XR Proprietary License.

# Commercial use or unauthorized field mining operations are strictly prohibited.

# ==============================================================================



package com.omniscan.xr



import com.google.ar.core.Frame

import com.google.ar.core.PointCloud



class ArDepthProcessor {

    fun processFrame(frame: Frame): List<Map<String, Float>> {

        val pointCloud: PointCloud = frame.acquirePointCloud()

        val points = mutableListOf<Map<String, Float>>()

        

        val buffer = pointCloud.points

        // ARCore provides points in (X, Y, Z, Confidence) format

        for (i in 0 until buffer.limit() step 4) {

            if (buffer.get(i + 3) > 0.5) { // Only use high-confidence points

                points.add(mapOf(

                    "x" to buffer.get(i),

                    "y" to buffer.get(i + 1),

                    "z" to buffer.get(i + 2)

                ))

            }

        }

        

        pointCloud.release()

        return points

    }

}
