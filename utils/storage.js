import * as FileSystem from 'expo-file-system'

export const saveScan = async (pointCloud) => {
  const fileName = `scan_${Date.now()}.json`
  const path = FileSystem.documentDirectory + fileName

  await FileSystem.writeAsStringAsync(
    path,
    JSON.stringify(pointCloud)
  )

  return path
}

export const loadScan = async (filePath) => {
  const data = await FileSystem.readAsStringAsync(filePath)
  return JSON.parse(data)
}
