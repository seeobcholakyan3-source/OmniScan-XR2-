# OmniScan-XR2
OmniScan-XR2: Advanced Geological Survey & 3D Mapping Suite
Overview
OmniScan-XR is a professional-grade, sub-surface 3D mapping ecosystem designed for the iPhone 16 Pro and PlayStation VR2 (PSVR2). By fusing high-frequency sonar telemetry with hardware-accelerated spectral analysis, the system identifies specific mineral densities—such as Gold and Diamonds—and projects them into a real-time, GPS-tagged 3D topographic mesh.

Built for the GitHub Codespaces environment, the system utilizes a high-performance cloud-relay architecture to process complex geological data while maintaining a lightweight footprint on mobile hardware.

🛰️ Key Features
AAA+ Voxel Engine: High-resolution sparse voxel mapping (5cm² precision) for deep-earth visualization.
Spectral Mineral Sonar: Real-time signal isolation using Fast Fourier Transforms (FFT) to detect Gold, Gems, and rare Earth elements.
GPS-Anchored Archiving: Automatic geolocation tagging for every scan, stored in a persistent SQLite3 database.
Cross-Reality Visualization: Exported .obj meshes with vertex coloring for instant AR viewing on iOS or immersive exploration in VR.
Resilient Telemetry Bridge: Low-latency hardware-to-cloud relay with automated packet-loss recovery.
📂 Repository Structure
OmniScan-XR2/
├── analysis/
│   ├── material_density.py # Mineral classification database
│   ├── spectral_math.py    # FFT-based signal processing
│   └── topo_mapper.py      # 3D Voxel coordinate engine
├── archive/
│   ├── raw_meshes/         # Timestamped .obj exports
│   └── survey_logs.db      # SQL index of all discoveries
├── bridge/
│   ├── Intersepter .py     # PSVR2 & Hardware bus capture (Note: file space)
│   ├── iphone_relay.py     # iPhone 16 Pro telemetry pusher
│   └── remote_listener.py  # GitHub Codespaces API receiver
├── core/
│   ├── archive_manager.py  # SQLite persistence layer
│   └── fusion_core.py      # Master system orchestrator
├── ui/
│   └── mesh_gen.py         # Wavefront .obj renderer with GPS headers
└── Makefile                # Unified system task runner
