
import ee

# ### Create imperviousness change function

def imperv_change(urban_region):
  # Look at change of imperviousness from 2001 to 2011
  
  nlcd_2001 = ee.Image( 'USGS/NLCD/NLCD2001')
  nlcd_2011 = ee.Image( 'USGS/NLCD/NLCD2011')
  
  # Get imperviousness layer
  nlcd_2001_imperv = nlcd_2001.select('impervious').clip( urban_region) 
  nlcd_2011_imperv = nlcd_2011.select('impervious').clip( urban_region)
  
  # Can we quantify how much Chicago grew in these 10 years?
  imperv_difference = nlcd_2011_imperv.subtract( nlcd_2001_imperv) 
  
  # Lose zero values - they don't interest us right now
  imperv_difference_masked = imperv_difference.updateMask( imperv_difference) 
  
  # Find the fraction of pixels in this region that show an increase in impermeability
    
  # ee.Image.pixelarea multiplies the value of each pixel by its area
  # So, setting each pixel value to 1 and multiplying by area gives
  # a map of pixel areas of all valid pixels
  urban_pixelarea = imperv_difference.gt(-999).multiply( ee.Image.pixelArea()) 
  
  increased_imperv_pixelarea = imperv_difference.gt( 0).multiply( ee.Image.pixelArea()) 
  
  # Reduceregions applies a reducer to all pixels in a region
  # In this case, we are getting the sum of all pixel areas
  # within each image, and extracting it as an ee.Numeric object
  increased_imperv_area = ee.Number(
      ee.List(
        increased_imperv_pixelarea
        .reduceRegions( urban_region, ee.Reducer.sum())
        .aggregate_array( 'sum')
      ).get(0)
    ) 
  
  urban_area =   ee.Number( ee.List(
        urban_pixelarea
        .reduceRegions( urban_region, ee.Reducer.sum())
        .aggregate_array( 'sum')
      ).get(0)
    ) 
  
  return increased_imperv_area.divide( urban_area).getInfo()


