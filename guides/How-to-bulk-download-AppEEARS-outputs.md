# How to bulk download your AppEEARS outputs using wget  

This how-to shows how to bulk download [AppEEARS](https://appeears.earthdatacloud.nasa.gov/) outputs using [wget](https://www.gnu.org/software/wget/) from the command line. Follow the steps below to download your AppEEARS outputs.  

## Step 1  

Submit your request using AppEEARS [website](https://appeears.earthdatacloud.nasa.gov/) or [API](https://appeears.earthdatacloud.nasa.gov/api/). More details on how to submit a point or area sample can be found in [AppEEARS Documentation](https://appeears.earthdatacloud.nasa.gov/help) and [API Documentation](https://appeears.earthdatacloud.nasa.gov/api/).  

## Step 2  

Using the AppEEARS Download Sample page, save the list of files you want to download. If you want all the outputs, select all and then click on `Save Download List`.  
![download list](https://github.com/nasa/AppEEARS-Data-Resources/assets/84464058/683fe565-07bf-4c36-b330-91d384052896)


## Step 3  

To download the outputs using wget from the command line, a `Bearer Token` is required. To generate this Token, you make a request to the AppEEARS [login service](https://appeears.earthdatacloud.nasa.gov/api/#login) from the command line, passing along your NASA Earthdata Login username and password in the request.  

The line below submits a HTTP POST request for a `Bearer Token`. Replace `Insert_Your_EDL_Username` and `Insert_Your_EDL_Password` with your Earthdata Login username and password respectively. Add the line to your command line interface and press enter to get a token:  

```text
wget -q -O - --method POST --user=Insert_Your_EDL_Username --password=Insert_Your_EDL_Password--auth-no-challenge https://appeears.earthdatacloud.nasa.gov/api/login
```

The return should look like:  

`{"token_type": "Bearer", "token": "r0HkNQtYquKjkOZbY-6P8mgjA8....", "expiration": "2023-05-04T14:05:47Z"} `

where the value contained in `"token"` is your `Bearer Token` (e.g., r0HkNQtYquKjkOZbY-6P8mgjA8....)

## Step 4  

To download the files:  

- In the command below, replace `Insert_Your_Token` with your token.  
- Replace `Input_File_List` with the full path to the saved downloaded list in the line below.
- Add the modified line in your command line and press enter.  

```text
wget --header "Authorization: Bearer Insert_Your_Token” -i Input_File_List  
```  

---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 06-29-2023  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
