/* ============================================================================
 * PROPRIETARY AND CONFIDENTIAL
 * OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
 * This code is protected under the OmniScan-XR Proprietary License.
 * Commercial use or unauthorized field mining operations are strictly prohibited.
 * ============================================================================ */

package com.omniscan.xr



import retrofit2.Response

import retrofit2.http.Body

import retrofit2.http.POST



interface OmniScanApi {

    @POST("/relay/lidar")

    suspend fun uploadSpatialData(@Body data: SpatialPayload): Response<BackendResponse>

}



data class SpatialPayload(

    val vertices: List<Map<String, Float>>,

    val timestamp: Long = System.currentTimeMillis()

)



data class BackendResponse(

    val status: String,

    val detections: List<DetectionMarker>

)



data class DetectionMarker(

    val type: String, // "Gold" or "Diamond"

    val probability: Float,

    val coordinates: Map<String, Float>

)
