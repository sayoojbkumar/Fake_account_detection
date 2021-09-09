import os
import glob
import pandas as pd
os.chdir("/home/hp/Desktop/Fake_account_detection/Data_Formatting")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combo.csv", index=False, encoding='utf-8-sig')