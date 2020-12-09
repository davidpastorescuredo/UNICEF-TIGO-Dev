#CDRs for development

#Copyright <2020> <UNICEF>

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#%autosave 0
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import rasterio as rio
from rasterio.windows import Window
import os
from pathlib import Path
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import geopandas as gpd
import shapely.speedups
shapely.speedups.enable()
from shapely.ops import cascaded_union
from geopandas import GeoDataFrame
import networkx as nx
import pickle
import math

version='1'#Track version of the code

#To Define: Save path
save_path='xxxxxx'

#SPATIAL RESOLUTION
tag='-sector'#Aggregation level proposed

#To Implement -> Load antenna map
#################################
#Write code here...
#Here it is necessary to make a previous mapping (another script) between Antennas and the geographical aggregation to be used (Shapefile)
#We need to know how GPS are related to antenna_ids in the CDR database to do this script for mapping with geo_unit

#Result -> DataFrame, antenna_map = ['antenna_id', 'longitude', 'latitude', 'geo_unit']
#################################

#DAILY RESOLUTION
t_day = datetime(2020,1,1)
t_end = datetime.now() - timedelta(days = 1)
t_end = datetime(t_end.year,t_end.month,t_end.day)

#To Define -> FIELDS OF THE CDRS
user_field='xxxxxx'
antenna_field='xxxxx'
#other relevant fields

while t_day <= t_end:
    
    day = t_day.strftime('%Y%m%d00')
    
    if os.path.exists(save_path+'Net_%s.cnf' % day) == False:
            
        print('calculating network for {}'.format(day))

        #To Implement -> READ CDRs CORRESPONDING TO "day"
        #################################
        #Write code here...
        
   
        #Result -> DataFrame, variable "full_data"
        #################################
        
        #To Implement -> Assign the geographical unit to each CDR (using the previous mapping antenna -> units)
        #################################
        #Write code here...
        #Use antenna_map dataframe
        
        
        #Result -> Modified DataFrame with the spatial resolution, variable "full_data" with the field ['geo_unit']
        #################################        
        
        print(full_data.shape)
        users=full_data[user_field]
        susers=list(set(users))
         
        G=nx.DiGraph()
        Gu=nx.Graph()
        
        for u in susers:
            
            traj=full_data[full_data[user_field]==u].copy()
            traj.sort_values(by='start',ascending=True,inplace=True)
             
            for t in range(0, traj.shape[0]-1):
                   
                orig_r=traj.iloc[t]
                dest_r=traj.iloc[t+1]

                antenna_orig=orig_r[antenna_field]
                antenna_dest=dest_r[antenna_field]
                
                a_record=antenna_map[antenna_map[:,'antenna_id']==antenna_orig]
                olat=a_record['latitude'].values[0]
                olon=a_record['longitude'].values[0]
                
                a_record=antenna_map[antenna_map[:,'antenna_id']==antenna_dest]
                dlat=a_record['latitude'].values[0]
                dlon=a_record['longitude'].values[0]
                
                orig=orig_r['geo_unit']
                dest=dest_r['geo_unit']
               
                d=math.sqrt(math.pow((olat-dlat),2)+math.pow((olon-dlon),2))   
     
                if not G.has_node(orig):
                    G.add_node(orig)
                if not G.has_node(dest):
                    G.add_node(dest)
                if not G.has_edge(orig,dest):
                    G.add_edge(orig,dest)
                    #Flow
                    G[orig][dest]['flow']=1
                    #Distance
                    G[orig][dest]['distance']=d
                else:
                    G[orig][dest]['flow']=G[orig][dest]['flow']+1

                if not Gu.has_node(orig):
                    Gu.add_node(orig)
                if not Gu.has_node(dest):
                    Gu.add_node(dest)
                if not Gu.has_edge(orig,dest):
                    Gu.add_edge(orig,dest)
                    #Flow
                    Gu[orig][dest]['flow']=1
                    #Distance
                    Gu[orig][dest]['distance']=d
                else:
                    Gu[orig][dest]['flow']=Gu[orig][dest]['flow']+1

        with open(save_path+'Net_'+day+'.cnf', 'wb') as handle:
            pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL) 

        with open(save_path+'Netu_'+day+'.cnf', 'wb') as handle:
            pickle.dump(Gu, handle, protocol=pickle.HIGHEST_PROTOCOL) 
           
    t_day += timedelta(days=1)

