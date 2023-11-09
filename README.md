![image](https://github.com/nasa/AppEEARS-Data-Resources/assets/104585874/9f61f185-50ba-43c0-b992-aa21d35e2b91)



# AppEEARS-Data-Resources

Welcome to the AppEEARS-Data-Resources repository. This repository provides resources and tutorials to help users work with [AppEEARS](https://appeears.earthdatacloud.nasa.gov/) programmatically. This repository also includes notebooks showing how to access and work with AppEEARS outputs directly in the Cloud. 

> Please note that in the interest of open science this repository has been made public but is still under active development. 
---

## Requirements  

+ Earthdata Login Authentication is required to access AppEEARS API and AppEEARS outpurs direcrly from an Amazon AWS bucket. If you do not have an account, create an account [here](https://urs.earthdata.nasa.gov/users/new).
---

## Prerequisites/Setup Instructions  

Instructions for setting up a compatible environment for working with AppEEARS API locally or in the cloud are linked to below.
- [`Python` set up instructions](https://github.com/nasa/LPDAAC-Data-Resources/blob/main/setup/setup_instructions_python.md)
- [`R` set up instructions](https://github.com/nasa/LPDAAC-Data-Resources/blob/main/setup/setup_instructions_r.md)

---
## Getting Started  

### Clone or download the [AppEEARS-Data-Resources repository](https://github.com/nasa/AppEEARS-Data-Resources).  

- [Download](https://github.com/nasa/AppEEARS-Data-Resources/archive/refs/heads/main.zip)  
- To clone the repository, type `git clone https://github.com/nasa/AppEEARS-Data-Resources.git` in the command line.  
---

## Repository Contents

Content in this repository is divided into Python and R resources including tutorials, how-tos, scripts, Defined modules that will be called from the Python resources, and setup instructionsThe supporting files for use cases are stored in `Data` folder.  


> Python and R resources stored in this repositories are listed below:  


| Repository Contents | Type | Summary | 
|----|-----|----|
| **[COG_AppEEARS_S3_Direct_Access.ipynb](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/Python/tutorials/COG_AppEEARS_S3_Direct_Access.ipynb)** | Jupyter Notebook | Demonstrates how to use AppEEARS Cloud Optimized GEOTIFF (COG) outputs using Python 
| **[Point_Sample_AppEEARS_S3_Direct_Access.ipynb](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/Python/tutorials/Point_Sample_AppEEARS_S3_Direct_Access.ipynb)** | Jupyter Notebook | Demonstrates how to access AppEEARS point sample Comma-Separated Values (CSV) outputs using Python 
| **[AppEEARS_API_Area.ipynb](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/Python/tutorials/AppEEARS_API_Area.ipynb)** | Jupyter Notebook | Demonstrates how to use Python to connect to the AppEEARS API to submit and downlaod an area sample  
| **[AppEEARS_API_Point.ipynb](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/Python/tutorials/AppEEARS_API_Point.ipynb)** | Jupyter Notebook | Demonstrates how to use Python to connect to the AppEEARS API to submit and downlaod a point sample 
| **[AppEEARS_API_Area_R.Rmd](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/R/tutorials/AppEEARS_API_Area_R.Rmd)** | R Markdown  | Demonstrates how to use R to connect to the AppEEARS API to submit and downlaod an area sample
| **[AppEEARS_API_Point_R.Rmd](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/R/tutorials/AppEEARS_API_Point_R.Rmd)** | R Markdown | Demonstrates how to use R to connect to the AppEEARS API to submit and downlaod a point sample
| **[How-to-bulk-download-AppEEARS-outputs.md](https://github.com/nasa/AppEEARS-Data-Resources/blob/main/guides/How-to-bulk-download-AppEEARS-outputs.md)** | Markdown | Demonstrates how to bulk download AppEEARS outputs using wget from the command line

---

## Helpful Links    

+ [AppEEARS Website](https://appeears.earthdatacloud.nasa.gov/)
+ [Available Products in AppEEARS](https://appeears.earthdatacloud.nasa.gov/products)
+ [AppEEARS Documentation](https://appeears.earthdatacloud.nasa.gov/help)
+ [AppEEARS API Documentation](https://appeears.earthdatacloud.nasa.gov/api/)
+ [LP DAAC Website](https://lpdaac.usgs.gov/)
+ [LP DAAC GitHub](https://github.com/nasa/LPDAAC-Data-Resources)


---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 11-09-2023  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
