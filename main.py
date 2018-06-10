'''
This script is the main function for the scripts that retrieve accumulated Growing Degree Days (gdds) 
for corn from NDAWN and plots the accumulated gdds for each date in the specified range
Additionally, the change of the accumulated gdds from the 5 year average is also plotted

Author Cody R. Gette

'''


import pandas as pd
import plot_gdds as pgdd
import build_features as bf
import os
import subprocess

#dates use fmt YYYY-mm-dd
begin_date = '2017-05-15'
end_date = '2017-09-30'

#Uncomment if you have ImageMagick installed and you want to automatically save a gif of the files
#gif=True

def main(gif = False):
    # Make sure a directory exists for the gdd data
    print("Checking for file pathways...")
    if not os.path.isdir("./data"):
        os.mkdir('data')
    if not os.path.isdir("./maps"):
        os.mkdir('maps')
    if not os.path.isdir("./maps/AGDD"):
        os.mkdir('maps/AGDD')
    if not os.path.isdir("./maps/Delta"):
        os.mkdir('maps/Delta')
    print("Building county location information...")
    bf. build_county_info()
    print("Retrieving data from NDAWN...")
    df = bf.make_new_gdd(begin_date, end_date)
    print("Making plots...")
    pgdd.plot_gdds(begin_date, end_date, df)

    if gif:
        #Optional: Run ImageMagick to convert pngs to animated gif
        print("Saving gif...")
        params1 = ['convert', './maps/Delta/*.png', './maps/Delta/delta_gdds_ND.gif']
        params2 = ['convert', './maps/AGDD/*.png', './maps/AGDD/gdds_ND.gif']
        subprocess.check_call(params1)
        subprocess.check_call(params2)
        

        
if __name__ == "__main__":
   
    main()
