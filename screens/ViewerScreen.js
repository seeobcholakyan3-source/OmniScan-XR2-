import React from 'react'
import { GLView } from 'expo-gl'
import * as THREE from 'three'
import { loadScan } from '../utils/storage'

export default function ViewerScreen({ route }) {

  const { file } = route.params

  const onContextCreate = async (gl) => {
    const scene = new THREE.Scene()

    const camera = new THREE.PerspectiveCamera(
      75,
      gl.drawingBufferWidth / gl.drawingBufferHeight,
      0.1,
      1000
    )

    camera.position.z = 3

    const renderer = new THREE.WebGLRenderer({ gl })
    renderer.setSize(gl.drawingBufferWidth, gl.drawingBufferHeight)

    const points = await loadScan(file)

    const geometry = new THREE.BufferGeometry()
    const vertices = new Float32Array(points.flat())

    geometry.setAttribute(
      'position',
      new THREE.BufferAttribute(vertices, 3)
    )

    const material = new THREE.PointsMaterial({ size: 0.02 })
    const cloud = new THREE.Points(geometry, material)

    scene.add(cloud)

    const render = () => {
      requestAnimationFrame(render)
      cloud.rotation.y += 0.003
      renderer.render(scene, camera)
      gl.endFrameEXP()
    }

    render()
  }

  return <GLView style={{ flex: 1 }} onContextCreate={onContextCreate} />
}
