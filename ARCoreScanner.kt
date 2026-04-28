package com.omniscan.xr



import android.content.Context

import com.google.ar.core.Config

import com.google.ar.core.Session

import com.google.ar.core.Frame

import com.google.ar.core.TrackingState



class ARCoreScanner(context: Context) {

    private var arSession: Session? = null



    init {

        setupSession(context)

    }



    private fun setupSession(context: Context) {

        arSession = Session(context)

        val config = Config(arSession)

        

        // Enable Depth API for Pixel devices to simulate LiDAR-like meshing

        if (arSession?.isDepthModeSupported(Config.DepthMode.AUTOMATIC) == true) {

            config.depthMode = Config.DepthMode.AUTOMATIC

        }

        

        // Optimize for real-time spatial mapping

        config.updateMode = Config.UpdateMode.LATEST_CAMERA_IMAGE

        arSession?.configure(config)

    }



    fun extractPointCloud(frame: Frame): List<FloatArray> {

        val points = mutableListOf<FloatArray>()

        val pointCloud = frame.acquirePointCloud()

        

        if (frame.camera.trackingState == TrackingState.TRACKING) {

            val buffer = pointCloud.points

            // Extract X, Y, Z coordinates and confidence values

            for (i in 0 until buffer.limit() step 4) {

                points.add(floatArrayOf(buffer.get(i), buffer.get(i+1), buffer.get(i+2)))

            }

        }

        pointCloud.release()

        return points // Ready to route to TopoMapper.py

    }

}
