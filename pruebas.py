from arcgis.gis import GIS
import arcgis.mapping

gis = GIS()

"""Using ARCGIS REST API create a map centered on Palm Springs, CA"""
def map():
    """Create a map centered on Palm Springs, CA"""
    url = "https://www.arcgis.com/home/item.html?id=a9a9c7f8a3c24c7d8d9e9f8f8b8a9a9a"
    map = arcgis.mapping.Map(url)
    return map

if __name__ == "__main__":
    map()