# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
# ==============================================================================

import json
import os

class SpectralAnalyzer:
def __init__(self):
lib_path = os.path.join(os.path.dirname(__file__), '../Data/spectral_lib.json')
with open(lib_path, 'r') as f:
self.library = json.load(f)

def calculate_absorption_depth(self, reflectance_center, reflectance_continuum):
"""Calculates absorption depth D = 1 - (R_center / R_continuum)"""
if reflectance_continuum == 0:
return 0
return 1 - (reflectance_center / reflectance_continuum)

def analyze_signature(self, swir1, swir2):
"""Evaluates mineral presence based on SWIR bands."""
results = []
for mineral in self.library['minerals']:
ratio = swir1 / swir2 if swir2 != 0 else 0
if ratio > mineral['probability_weight']:
results.append({
"mineral": mineral['name'],
"confidence": min(ratio, 0.99)
})
return results
