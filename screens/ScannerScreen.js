import React from 'react'
import { View, Button, StyleSheet } from 'react-native'
import { saveScan } from '../utils/storage'

export default function ScannerScreen({ navigation }) {

  const generateFakePointCloud = () => {
    let points = []

    for (let i = 0; i < 5000; i++) {
      points.push([
        (Math.random() - 0.5) * 2,
        (Math.random() - 0.5) * 2,
        (Math.random() - 0.5) * 2
      ])
    }

    return points
  }

  const handleStopScan = async () => {
    const pointCloud = generateFakePointCloud()

    const filePath = await saveScan(pointCloud)

    navigation.navigate('Viewer', { file: filePath })
  }

  return (
    <View style={styles.container}>
      <Button title="Stop Scan" onPress={handleStopScan} />
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center'
  }
})
