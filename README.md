ND_Visualize_Corn_GDDs
==============================

This project retrieves and visualizes North Dakota Growing Degree Days data from NDAWN using python. 
Data from NDAWN is retrieved with an API request.

Visualizations are made as Choropleth plots for each county in North Dakota.
Animated gifs are generated showing the change in accumulated GDDs as well as the change from the 5 year average.

Getting Started
--------------------------

Clone the repo and navigate to the `main.py` file. Open the
file and edit the
`begin_date`, and
`end_date`
variables. The begin and end dates are the dates between which you want to
plot the GDDs.
Additionally, if ImageMagick is installed on your machine, set
`gif=True` to save an animated gif of the plots.

Once the variables are set, run `main.py`


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data		   <- GDD and location data 
    │
    ├── maps         	   <- Visualized gdds and delta_gdds for provided date range
    │
    ├── main.py            <- Main python function: edit input dates here 
    │
    ├── build_features.py  <- Builds GDD data from NDAWN and cleans county data
    │     
    ├── plot_gdds.py   	   <- Produces png files for each date and animated gif
    │
    ├── stations.csv       <- location info for each NDAWN weather station
    └── NDcounties.csv     <- List of counties in North Dakota 

Visualization
--------
![Accumulated GDDs](./maps/AGDD/gdds_ND_2017.gif)

![Delta GDDs](./maps/Delta/delta_gdds_ND_2017.gif )

