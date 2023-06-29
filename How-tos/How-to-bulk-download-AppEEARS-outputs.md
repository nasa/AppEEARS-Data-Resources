## How to bulk download your AppEEARS outputs using wget: 
This quick tutorial shows how to bult downlaod AppEEARS outputs using a command line. Follow steps below to download your AppEEARS outputs.  

# Step 1: 

Submit your request using AppEEARS website or API. More details on how to submit a point or area sample can be found in [AppEEARS Documentation](https://appeears.earthdatacloud.nasa.gov/help) and [API Documentation](https://appeears.earthdatacloud.nasa.gov/api/). 

---
# Step 2:

Using the AppEEARS Download Sample page, save the list of files you want to download. If you want all the outputs, select all and then click on “Save Download List”. 

---
# step 3:
 
To downlaod the outputs using command line, a Bearer Token is required. To generate this Token in command line, you need to make a call to the AppEEARS login service using the NASA Earthdata Login username and password. Insert your Earthdata Login username and password in the line below instead of **Insert_Your_EDL_Username** and **Insert_Your_EDL_Password**. Then type it in command line and press enter to get a token:

`wget -q -O - --method POST --user= Insert_Your_EDL_Username --password= Insert_Your_EDL_Password--auth-no-challenge https://appeears.earthdatacloud.nasa.gov/api/login `

Your token should look like: 

`{"token_type": "Bearer", "token": "r0HkNQtYquKjkOZbY-6P8mgjA8....", "expiration": "2023-05-04T14:05:47Z"} `

---

# step 4:

To download the files:  
 - Copy your token and paste it instead of **Insert_Your_Token** in the line below.
 - Insert the full path to the saved downloaded list instead of **Insert_full_Path_to_Your_Download_List** in the line below.
 - Type the modified line in your command line and press enter.

`wget --header "Authorization: Bearer Insert_Your_Token” -i Insert_full_Path_to_Your_Download_List `


---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 06-29-2023  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
