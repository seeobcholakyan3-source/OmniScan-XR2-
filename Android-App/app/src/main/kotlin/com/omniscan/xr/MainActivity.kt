/* ============================================================================
 * PROPRIETARY AND CONFIDENTIAL
 * OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
 * This code is protected under the OmniScan-XR Proprietary License.
 * Commercial use or unauthorized field mining operations are strictly prohibited.
 * ============================================================================ */

package com.omniscan.xr



import android.os.Bundle

import androidx.activity.ComponentActivity

import androidx.activity.compose.setContent

import androidx.compose.foundation.background

import androidx.compose.foundation.layout.*

import androidx.compose.foundation.shape.RoundedCornerShape

import androidx.compose.material3.MaterialTheme

import androidx.compose.material3.Text

import androidx.compose.runtime.*

import androidx.compose.ui.Alignment

import androidx.compose.ui.Modifier

import androidx.compose.ui.graphics.Color

import androidx.compose.ui.text.font.FontWeight

import androidx.compose.ui.unit.dp

import androidx.compose.ui.unit.sp



class MainActivity : ComponentActivity() {

    // Initialize AR Scanner and Python Bridge

    private lateinit var arScanner: ARCoreScanner

    private val pythonBridge = PythonBridge()



    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)

        arScanner = ARCoreScanner(this)



        setContent {

            OmniScanTheme {

                DashboardHUD()

            }

        }

    }

}
