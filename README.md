Last updated:  2015-11-16

This document provides information and instructions for running the Chesapeake Bay Chlorophyll Hotspot Identifier (CBCHI).

INTRODUCTION:
-------------------------------
The CBCHI was designed as part of the NASA DEVELOP Fall 2015 Virginia Water Resources II project.  Its development was intended to address the difficulty of locating high concentrations of chlorophyll and harmful algal blooms on the Chesapeake Bay.  The CBCHI uses Landsat 8 surface reflectance products to create two maps highlighting chlorophyll concentration.  To learn more about this project, visit:  http://www.devpedia.developexchange.com/dp/index.php?title=Virginia_Water_Resources_WC_Fall_2015

REQUIREMENTS:
---------------------------------
This script requires the following python modules: 
ArcPy:  http://pro.arcgis.com/en/pro-app/arcpy/get-started/what-is-arcpy-.htm
 os:  https://docs.python.org/2/library/os.html
glob: https://docs.python.org/2/library/glob.html?highlight=glob#module-glob

The script also requires Landsat 8 surface reflectance products and the "cfmask" cloud mask provided by the surface reflectance data package.  For more information on this product, see:  http://landsat.usgs.gov/documents/provisional_l8sr_product_guide.pdf

The script also requires the file titled "bathmask.tif", and its supporting files, to be in the same folder as the Landsat 8 OLI images this code will be applied to.

RUNNING THE SCRIPT:
----------------------------------
Open the script in Python 2.7 IDLE and run it.  The script will prompt the user to input the path of the file location.  The script will read this as a string, so enter the file path without any quotes.

The script will prompt the user to specify how many standard deviations they want to use for the sediment mask applied to the Landsat 8 images.

The final images the script produces will be saved in the original file path.  The names the files will be saved as adhere to the following format:

True color composition:  “truecolor.tif”
NDVI chlorophyll concentration map:  “ndvi_chl_sd_(n).tif”, where (n) is the number of standard deviations used in the creation of the sediment mask, specified by the user.
543 color composition chlorophyll concentration map:  “comp_band_543_chl_sd_(n).tif”, where (n) is the number of standard deviations used in the creation of the sediment mask, specified by the user.

USING FINAL PRODUCTS:
-----------------------------------
The final images can be opened in ArcMap and stretched to display various extents of chlorophyll concentration, based on the users needs.
