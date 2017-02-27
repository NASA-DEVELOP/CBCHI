# Notices:
# Copyright 2017, United States Government as represented by the Administrator 
# of the National Aeronautics and Space Administration. All Rights Reserved.
 
# Disclaimers
# No Warranty: THE SUBJECT SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY 
# OF ANY KIND, EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT 
# LIMITED TO, ANY WARRANTY THAT THE SUBJECT SOFTWARE WILL CONFORM TO 
# SPECIFICATIONS, ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE, OR FREEDOM FROM INFRINGEMENT, ANY WARRANTY THAT THE 
# SUBJECT SOFTWARE WILL BE ERROR FREE, OR ANY WARRANTY THAT DOCUMENTATION, 
# IF PROVIDED, WILL CONFORM TO THE SUBJECT SOFTWARE. THIS AGREEMENT DOES NOT, 
# IN ANY MANNER, CONSTITUTE AN ENDORSEMENT BY GOVERNMENT AGENCY OR ANY PRIOR 
# RECIPIENT OF ANY RESULTS, RESULTING DESIGNS, HARDWARE, SOFTWARE PRODUCTS 
# OR ANY OTHER APPLICATIONS RESULTING FROM USE OF THE SUBJECT SOFTWARE.  
# FURTHER, GOVERNMENT AGENCY DISCLAIMS ALL WARRANTIES AND LIABILITIES 
# REGARDING THIRD-PARTY SOFTWARE, IF PRESENT IN THE ORIGINAL SOFTWARE, AND 
# DISTRIBUTES IT "AS IS." 
 
# Waiver and Indemnity:  RECIPIENT AGREES TO WAIVE ANY AND ALL CLAIMS 
# AGAINST THE UNITED STATES GOVERNMENT, ITS CONTRACTORS AND SUBCONTRACTORS, 
# AS WELL AS ANY PRIOR RECIPIENT.  IF RECIPIENT'S USE OF THE SUBJECT 
# SOFTWARE RESULTS IN ANY LIABILITIES, DEMANDS, DAMAGES, EXPENSES OR 
# LOSSES ARISING FROM SUCH USE, INCLUDING ANY DAMAGES FROM PRODUCTS BASED 
# ON, OR RESULTING FROM, RECIPIENT'S USE OF THE SUBJECT SOFTWARE, RECIPIENT 
# SHALL INDEMNIFY AND HOLD HARMLESS THE UNITED STATES GOVERNMENT, ITS 
# CONTRACTORS AND SUBCONTRACTORS, AS WELL AS ANY PRIOR RECIPIENT, TO THE 
# EXTENT PERMITTED BY LAW.  RECIPIENT'S SOLE REMEDY FOR ANY SUCH MATTER 
# SHALL BE THE IMMEDIATE, UNILATERAL TERMINATION OF THIS AGREEMENT.

# Description: 
# This tool takes in Landsat 8 data.
# It removes land pixels, cloud pixels, pixels corresponding to a depth 
# of 2 meters or shallower, and high sediment concentrations
# It then creates three final images:  A true color image, a 543 color 
# composition chlorophyll concentration image, and a normalized difference 
# vegetation index (NDVI) chlorophyll concentration image.
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os
import glob
from arcpy import *
from arcpy.sa import *

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

#set working directory
#The path should be set using no quotes and single forward slashes, e.g. C:/Users/DEVELOP4/Desktop/test
env.workspace = raw_input("What's the file location? ")
os.chdir(env.workspace)

n = float(raw_input("If you'd like to change the standard deviation for the sediment mask, type the multiplyer here.  If you'd like to keep it default, type '1' --> "))#user input float raw_input
arcpy.env.overwriteOutput = True

if os.path.isfile("b1clb.tif") == False:

    # Isolating landsat band files
    B1 = glob.glob("*_band1*")
    B2 = glob.glob("*_band2*")
    B3 = glob.glob("*_band3*")
    B4 = glob.glob("*_band4*")
    B5 = glob.glob("*_band5*")
    B6 = glob.glob("*_band6*")
    B7 = glob.glob("*_band7*")
    C = glob.glob("*_cfmask*")
    bath = glob.glob("*bath*")
    #defining landsat band files
    b1 = B1[0]
    b2 = B2[0]
    b3 = B3[0]
    b4 = B4[0]
    b5 = B5[0]
    b6 = B6[0]
    b7 = B7[0]
    cloud = C[0]
    bathmask = bath[0]

    print("Defined bands")

    #Make floating point valued rasters
    b1float = Raster(b1) * 0.0001
    b2float = Raster(b2) * 0.0001
    b3float = Raster(b3) * 0.0001
    b4float = Raster(b4) * 0.0001
    b5float = Raster(b5) * 0.0001
    b6float = Raster(b6) * 0.0001
    b7float = Raster(b7) * 0.0001

    print("Created floating point rasters")
    #Calculate the NDVI from b4 and b5
    ndvi = (b5float-b4float)/(b5float+b4float)

    # Create the watermask
    watermask = Con(ndvi,1,"","VALUE < 0")

    # Creating water-only band rasters
    b1water = ExtractByMask(b1float,watermask)
    b2water = ExtractByMask(b2float,watermask)
    b3water = ExtractByMask(b3float,watermask)
    b4water = ExtractByMask(b4float,watermask)
    b5water = ExtractByMask(b5float,watermask)
    b6water = ExtractByMask(b6float,watermask)
    b7water = ExtractByMask(b7float,watermask)

    print("Removed land pixels")

    # Reclassify the cloud mask values
    cloudmask = Reclassify(cloud,"Value",RemapRange([[0,1,1],[2,4,"NODATA"]]))

    # Removing clouds from the bands
    b1wc = ExtractByMask(b1water,cloudmask)
    b2wc = ExtractByMask(b2water,cloudmask)
    b3wc = ExtractByMask(b3water,cloudmask)
    b4wc = ExtractByMask(b4water,cloudmask)
    b5wc = ExtractByMask(b5water,cloudmask)
    b6wc = ExtractByMask(b6water,cloudmask)
    b7wc = ExtractByMask(b7water,cloudmask)

    print("Removed cloud pixels")

    #remove shallow pixels
    b1clb = ExtractByMask(b1wc,bathmask)
    b2clb = ExtractByMask(b2wc,bathmask)
    b3clb = ExtractByMask(b3wc,bathmask)
    b4clb = ExtractByMask(b4wc,bathmask)
    b5clb = ExtractByMask(b5wc,bathmask)
    b6clb = ExtractByMask(b6wc,bathmask)
    b7clb = ExtractByMask(b7wc,bathmask)

    b1clb.save("b1clb.tif")
    b2clb.save("b2clb.tif")
    b3clb.save("b3clb.tif")
    b4clb.save("b4clb.tif")
    b5clb.save("b5clb.tif")
    b6clb.save("b6clb.tif")
    b7clb.save("b7clb.tif")

    print("Removed shallow pixels")

    #Creating the NDTI mask
    ndti = (b4clb-b3clb)/(b4clb+b3clb)
    ndti.save("ndti.tif")

    arcpy.CalculateStatistics_management("ndti.tif")

    ustd = arcpy.GetRasterProperties_management("ndti.tif","STD")
    ostd = ustd.getOutput(0)
    std = n*float(ostd)

    umean = arcpy.GetRasterProperties_management("ndti.tif","MEAN")
    omean = umean.getOutput(0)
    mean = float(omean)

    mod = mean + std
    h = str(mod)
    value = "VALUE < " + h

    ndtimask = Con(ndti,1,"",value)
    newmask = "ndvimask_sd_" + str(n) + ".tif"
    ndtimask.save(newmask)

    print("NDTI mask created.  Now creating True Color Image, NDVI Chlorophyll image, and 543 Composite Chlorophyll image")

    #making a true color image
    truecolorlist = [b4,b3,b2]
    CompositeBands_management(truecolorlist,"truecolor.tif")

    print("Created True Color Image")

    #creating the NDVI for chlorophyll concentration
    chl_ndvi = (b5clb-b4clb)/(b5clb+b4clb)
    chlndvi = ExtractByMask(chl_ndvi,ndtimask)
    chlndviname = "ndvi_chl_sd_" + str(n) + ".tif"
    chlndvi.save(chlndviname) #this is the final NDVI chlorophyll concentration image to be stretched

    print("Created NDVI chlorophyll concentration image")

    #making a 543 band composite
    chlbandlist = [b5clb,b4clb,b3clb]
    band543 = CompositeBands_management(chlbandlist,"comp_band_543.tif")
    band543_sed = ExtractByMask("comp_band_543.tif",ndtimask)
    b543name = "comp_band_543_chl_sd_" + str(n) + ".tif"
    band543_sed.save(b543name) #this is the final 543 image to be stretched

    print("Created 543 color composite for chlorophyll concentration")

else:
    #retrieving previously saved land, cloud, and shallow pixel removed images
    B1 = glob.glob("b1clb.tif")
    B2 = glob.glob("b2clb.tif")
    B3 = glob.glob("b3clb.tif")
    B4 = glob.glob("b4clb.tif")                                   
    B5 = glob.glob("b5clb.tif")
    B6 = glob.glob("b6clb.tif")
    B7 = glob.glob("b7clb.tif")

    print("Defined Bands")
    
    #defining each cloud, land, and shallow image
    b1clb = Raster(B1[0])
    b2clb = Raster(B2[0])
    b3clb = Raster(B3[0])
    b4clb = Raster(B4[0])
    b5clb = Raster(B5[0])
    b6clb = Raster(B6[0])
    b7clb = Raster(B7[0])

    arcpy.overwriteoutput = True

    #Creating the NDTI mask
    ndti = (b4clb-b3clb)/(b4clb+b3clb)
    ndti.save("ndti.tif")

    arcpy.CalculateStatistics_management("ndti.tif")

    ustd = arcpy.GetRasterProperties_management("ndti.tif","STD")
    ostd = ustd.getOutput(0)
    std = n*float(ostd)

    umean = arcpy.GetRasterProperties_management("ndti.tif","MEAN")
    omean = umean.getOutput(0)
    mean = float(omean)

    mod = mean + std
    h = str(mod)
    value = "VALUE < " + h

    ndtimask = Con(ndti,1,"",value)
    newmask = "ndvimask_sd_" + str(n) + ".tif"
    ndtimask.save(newmask)

    print("NDTI mask created.  Now creating NDVI Chlorophyll image and 543 Composite Chlorophyll image")

    #creating the NDVI for chlorophyll concentration
    chl_ndvi = (b5clb-b4clb)/(b5clb+b4clb)
    chlndvi = ExtractByMask(chl_ndvi,ndtimask)
    chlndviname = "ndvi_chl_sd_" + str(n) + ".tif"
    chlndvi.save(chlndviname) #this is the final NDVI chlorophyll concentration image to be stretched

    print("Created NDVI chlorophyll concentration image")

    #making a 543 band composite
    chlbandlist = [b5clb,b4clb,b3clb]
    band543 = CompositeBands_management(chlbandlist,"comp_band_543.tif")
    band543_sed = ExtractByMask("comp_band_543.tif",ndtimask)
    b543name = "comp_band_543_chl_sd_" + str(n) + ".tif"
    band543_sed.save(b543name) #this is the final 543 image to be stretched

    print("Created 543 color composite for chlorophyll concentration")
