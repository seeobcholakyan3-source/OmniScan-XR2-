
/* ============================================================================
 * PROPRIETARY AND CONFIDENTIAL
 * OmniScan-XR2 System - Copyright (c) 2026 Serob Cholakyan
 * This code is protected under the OmniScan-XR Proprietary License.
 * Commercial use or unauthorized field mining operations are strictly prohibited.
 * ============================================================================ */

package com.omniscan.xr



import android.content.Context
import android.opengl.GLSurfaceView
import android.view.Surface
import com.google.ar.core.Config
import com.google.ar.core.Session
import com.google.ar.core.Frame
import com.google.ar.core.TrackingState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.math.abs



class ARCoreScanner(context: Context) {

    private var arSession: Session? = null
    private var isScanning = false
    private var frameProcessingJob: Job? = null
    private var onPointCloudExtracted: ((List<FloatArray>) -> Unit)? = null



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



    fun setPointCloudCallback(callback: (List<FloatArray>) -> Unit) {

        onPointCloudExtracted = callback

    }



    suspend fun startFrameCapture() = withContext(Dispatchers.Default) {

        if (arSession == null) {

            println("ERROR: ARCore Session not initialized!")

            return@withContext

        }

        isScanning = true

        frameProcessingJob = kotlinx.coroutines.GlobalScope.launch(Dispatchers.Default) {

            while (isActive && isScanning && arSession != null) {

                try {

                    val frame = arSession?.update()

                    if (frame != null) {

                        val pointCloud = extractPointCloud(frame)

                        if (pointCloud.isNotEmpty()) {

                            onPointCloudExtracted?.invoke(pointCloud)

                        }

                    }

                } catch (e: Exception) {

                    println("Frame Capture Error: ${e.message}")

                }

                // Small delay to avoid excessive processing

                kotlinx.coroutines.delay(100)

            }

        }

    }



    suspend fun stopFrameCapture() = withContext(Dispatchers.Default) {

        isScanning = false

        frameProcessingJob?.cancel()

        frameProcessingJob = null

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
