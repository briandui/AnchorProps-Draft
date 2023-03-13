# AnchorProps
# Start of a script to hold functions for basic anchor properties as a function of applied
# anchor loads and soil type. This is the "stage 1" simple model. It is a fairly manual method to start with.

import numpy as np
import moorpy as mp
import yaml



def getAnchorProps(fx, fz, anchor="drag-embedment", soil='medium-clay', method="static", display=0):          #new variable "method" added 
    '''Calculates anchor required capacity, mass, and cost based on specified loadings and anchor type
    
    Parameters
    ----------
    fx : float
        horizontal maximum anchor load [N]
    fz : float
        vertical maximum anchor load [N]
    anchor : string
        anchor type name
    soil : string
        soil type name
    method : string
        anchor analysis method 
    
    Returns
    -------
    capacity : float
        required anchor holding capacity [kN]
    mass : float
        anchor mass [mT]
    cost : float
        anchor cost [mT]
    '''

    # to consider later: scale QS loads by 20% to approximate dynamic loads
    
    # note: capacity is measured here in kg force

    if anchor == "drag-embedment":
        # required capacity -- condition 'intact'    

        if method == "static":
            capacity_x = 1.8*fx/9.81                     # default safety factor for quasi-static (HOMGE ) 
        elif method == 'dynamic':
            capacity_x = 1.5*fx/9.81                     # default safety factor for dynamic (HOMEGE & API RP-2SK)
        else:
            raise Exception("Error - invalid method")
        capacity = capacity_x


        # figure out required anchor size based on the soil type
        if soil == 'soft-clay':
            # calculate anchor mass based on required capacity
            mass = (capacity - 879.48)/346.59          # based off Matt's capacity curves 
            
        elif soil == 'medium-clay':
            mass = (capacity - 1209.8)/476.76          # how do we account for small capacities (negavtive mass)?  

        elif soil == "hard-clay" or "sand":
            mass = (capacity- 1708.3)/581.48
        
        else:
            raise Exception("Error - invalid soil type")
        
        # calculate cost based on mass (assuming some cost coefficient per kg of steel)
        # cost = 27.2someCoefficient*mass  
        cost = 2500 * mass  

        # ------Costs from Moorpy-----------
        fzCost = 0
        #if fz > 0:
        #   fzCost = 1e3*fz
        #if display > 0: print('WARNING: Nonzero vertical load specified for DEA.')
        cost_c = 0.188 * capacity + fzCost
        #------------------------------------
        

    elif anchor == "suction":
        capacity_x = 1.6*fx/9.81
        capacity_z = 2.0*fz/9.81
        capacity = np.linalg.norm([capacity_x,capacity_z])
       
        if soil == "soft-clay":
            mass = 0.0071*capacity + 3.9169                 # how do we make this mass curves quadratic?
        
        elif soil == "medium-clay":
            mass = 0.0043*capacity - 2.085
        
        else:
            raise Exception("Error - invalid soil type")
            print('not supported yet...')
        
        cost = 3500 * mass
        cost_c = 1.08 * capacity

    elif anchor == "plate":
        capacity_x = 2.0*fx/9.81
        capacity_x = 3.0*fx/9.81                         # applied safety factor for minimal know soil conditions (from Handbook of Marine Geotech)
        capacity_z = 2.0*fz/9.81
        capacity = np.linalg.norm([capacity_x,capacity_z])

        if soil == "soft-clay":
            mass = (capacity - 6417)/161.61
        
        if soil == "medium-clay":
            mass = (capacity - 6483.1)/379.74
        
        else:
            raise Exception("Error - invalid soil type")
        
        cost = 2500 * mass


    elif anchor == "micropile":
        capacity_x = 2.0*fx/9.81
        capacity_z = 2.0*fz/9.81
        capacity = np.linalg.norm([capacity_x,capacity_z])

        if soil == "...":
            print('not supported yet')
            # no capacity curves found yet 
        else:
            raise Exception("Error - invalid soil type")
        
        cost_c = (200000*1.2/500000)*capacity
    
    elif anchor == "SEPLA":
        capacity = 2.0*fx/9.81

        if soil == "soft-clay":
            mass = (-1.712E-13*capacity**3 + 1.214E-07*capacity**2 + 6.849E-04*capacity + 1.426)   #polynomial curve fit
        else:
            raise Exception("Error - invalid soil type")
        
        cost = 2500 * mass   #frabication of steel for plate $/ton (according to O'Loghlin et al. 2015)
        cost_c = 0.45* capacity 
        
        
    else:
        raise Exception(f'getAnchorProps received an unsupported anchor type ({anchor})')
    
    return capacity, mass, cost, cost_c
    


