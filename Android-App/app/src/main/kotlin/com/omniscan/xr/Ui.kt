/* ============================================================================
 * PROPRIETARY AND CONFIDENTIAL
 * OmniScan-XR2 System - Copyright (c) 2026 Serob Cholakyan
 * This code is protected under the OmniScan-XR Proprietary License.
 * Commercial use or unauthorized field mining operations are strictly prohibited.
 * ============================================================================ */


package com.omniscan.xr

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

private val OmniScanColorScheme = lightColorScheme(
    primary = Color(0xFF1E88E5),
    onPrimary = Color.White,
    secondary = Color(0xFF26A69A),
    onSecondary = Color.White,
    background = Color(0xFF101010),
    onBackground = Color.White,
    surface = Color(0xFF121212),
    onSurface = Color.White,
)

@Composable
fun OmniScanTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = OmniScanColorScheme,
        typography = MaterialTheme.typography,
        content = content
    )
}

@Composable
fun DashboardHUD(arScanner: ARCoreScanner, pythonBridge: PythonBridge) {
    val coroutineScope = rememberCoroutineScope()
    var isScanning by remember { mutableStateOf(false) }
    
    // Set up point cloud callback when composable is created
    LaunchedEffect(Unit) {
        arScanner.setPointCloudCallback { pointCloud ->
            coroutineScope.launch {
                pythonBridge.transmitSpatialData(pointCloud.toList())
            }
        }
    }
    
    Surface(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(16.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(18.dp, Alignment.Top),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "OmniScan-XR2",
                fontSize = 32.sp,
                fontWeight = FontWeight.ExtraBold,
                color = MaterialTheme.colorScheme.primary
            )

            Card(
                modifier = Modifier.fillMaxSize(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Text(
                        text = "AR scanning active",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = "Point cloud relay online.",
                        fontSize = 16.sp,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Button(
                        onClick = {
                            isScanning = !isScanning
                            if (isScanning) {
                                coroutineScope.launch {
                                    arScanner.startFrameCapture()
                                    println("AR Frame Capture Started!")
                                }
                            } else {
                                coroutineScope.launch {
                                    arScanner.stopFrameCapture()
                                    println("AR Frame Capture Stopped!")
                                }
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Text(
                            text = if (isScanning) "Stop Scan" else "Start Scan",
                            color = MaterialTheme.colorScheme.onPrimary
                        )
                    }
                }
            }
        }
    }
}
