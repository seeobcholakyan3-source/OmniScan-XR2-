# ==============================================================================

# PROPRIETARY AND CONFIDENTIAL

# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan

# This code is protected under the OmniScan-XR Proprietary License.

# Commercial use or unauthorized field mining operations are strictly prohibited.

# ==============================================================================

import numpy as np

class TopoMapper:
    def __init__(self):
        # Set resolution to 0.5 meters per block for optimal performance
        self.voxel_size = 0.5 

    def voxelize_mesh(self, vertices):
        """Converts raw ARKit point clouds into a manageable 3D grid."""
        points = np.array(vertices)
        
        # Divide coordinates by voxel size and round to create a 3D grid index
        voxels = np.round(points / self.voxel_size).astype(int)
        
        # Remove duplicate points falling in the same block
        unique_voxels = np.unique(voxels, axis=0)
        
        print(f"TopoMapper: Compressed {len(points)} raw points to {len(unique_voxels)} logical voxels.")
        return unique_voxels.tolist()
      
