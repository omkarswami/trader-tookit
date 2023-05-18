import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def get_color_codes(volume_profile_array):
    shades=['#ffffff','#eae7e8','#d5cfd2','#c1b7bc','#ac9fa6','#988890','#83707a','#6e5864','#5a404e','#452838','#311122']

    color_codes=[]
    #print(delivery_profile_array)
    min_del=min([i for i in delivery_profile_array if i > 0])
    ratio_list=list(map(lambda x:x/min_del, volume_profile_array))
    divisor=max(ratio_list)/10
    mapped_range=list(map(lambda x:round(x/divisor),ratio_list))
    color_codes=list(map(lambda x:shades[x],mapped_range))
    print(color_codes)
    return color_codes

# function converts price volume dataframe into levels dataframe
def get_delivery_profile(pv_dataframe):
    ltp=pv_dataframe.iloc[-1,4]
    percent_array=np.arange(-5.0,5.0,0.25)
    print(percent_array)
    levels_array=[]
    for e in percent_array:
        levels_array.append((ltp+(e/100)*ltp))
    levels_array=sorted(levels_array)
    profile_result_col=["Lower Level","Upper Level","Volume","Label"]
    profile_result=pd.DataFrame(columns=profile_result_col)
    i=0
    while i < (len(levels_array)-1):
        deliverable_total_records=pv_dataframe[(pv_dataframe["Close"]>=levels_array[i])&(pv_dataframe["Close"]<levels_array[i+1])]
        deliverable_total=deliverable_total_records["Volume"].sum()
        label=str(percent_array[i])+'to'+str(percent_array[i+1])+'%'+"("+str(round(levels_array[i],2))+"-"+str(round(levels_array[i+1],2))+")"
        entry_row=[levels_array[i],levels_array[i+1],deliverable_total,label]
        profile_result.loc[i]=entry_row
        i=i+1
    color_codes= get_color_codes(profile_result["Volume"].tolist())
    profile_result["Color Code"]=color_codes
    print(profile_result)
    return profile_result
plt.style.use('dark_background')  
# folder path to price volume data files
folder_path="downloads/"
file_path=""
option=""
if len(sys.argv) != 2:
    #option is filename of data file or part of filename if filename is RELIANCE-PRICE-VOL.csv use RELIANCE-PRICE-VOL.csv or RELIANCE if multiple files have RELIANCE in their name use specific file name
    print("SPECIFY SYMBOL")
elif  len(sys.argv) == 2:
    option=sys.argv[1]
    for i in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path,i)) and option in i:
            file_path=os.path.join(folder_path,i)
    if file_path=="":
        print("FILE DOES NOT EXIST PLEASE DOWNLOAD FILE OF STOCK.")
    else:    
        df = pd.read_csv(file_path)        
        volume_profile=get_delivery_profile(df)
        fig, ax1 = plt.subplots()
        for index, row in volume_profile.iterrows():
            ax1.axhspan(ymin=row["Lower Level"],ymax=row["Upper Level"],color=row["Color Code"])
        ax1.set_title('VOLUME PROFILE - '+option)
        ax1.set_ylabel('Price')
        ax1.set_yticks(volume_profile["Lower Level"])
        fig.set_size_inches(13,8)
        plt.show()
        
