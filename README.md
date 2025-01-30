# 27-Crags-Scraper

These scripts were designed reverse engineering the 27Crags website to obtain the different crags data, and by extension the routes of each crag.

The final csv files are in the "files" folder, and the different visualisations made in Tableau are in the "tableau_visuals" folder. 

As for the individual scripts, the Get_Crags obtains each crag available from the map view on the 27Crags website. 

Each one of these crags is stored with its basic information in a dataset, which is the looked up individually to find the necessary ID, called param_id, storing the completed dataset as the crags_data.csv file.

The Get_Routes script then uses that dataset, extracts the most intersting information (to include it in it's own final product), and looks up the routelist of each indvidual crag, storing the final product in a dataset, which in turn is also converted into a routes_data.csv file
