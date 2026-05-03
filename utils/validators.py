def validate_coordinates(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)

        if not (-90 <= lat <= 90):
            return False, "Invalid latitude"

        if not (-180 <= lon <= 180):
            return False, "Invalid longitude"

        return True, (lat, lon)

    except:
        return False, "Invalid numeric format"
