/*********************************************
 * OPL 12.6.0.0 Model
 * Author: bscuser
 * Creation Date: 22/10/2018 at 10:40:54
 *********************************************/

 int numServices = ...;
 int numDrivers = ...;
 int numBuses = ...;
 int maxBuses = ...;
 
 tuple Service
 {
	int starting_time;
	int duration_time;
	int kilometers;
	int passangers_num;
 }
 
 
 tuple Bus
 {
 	int passangers_cap;
 	int price_min;
 	int price_km;
 }
 
 tuple Drivers
 {
 	int max_working_time;
 	int BM;
 	int CBM;
 	int CEM; 
 }
 range B = 1..numBuses;
 range D = 1..numDrivers;
 range S = 1..numServices;
 
 Service services[S]=...;
 Bus buses[B]=...;
 Drivers drivers[D]=...;
 
 
 range M = 1..1440;//minutes a day.
 
 dvar float+ cost;
 
 dvar boolean busServesService[B][S];
 dvar boolean DriverServesService[D][S];
 
 minimize cost;
 subject to
 {
 	//same 	bus cannot serve overlap in time
 	
 	//respect max hours for drivers
 	forall(d in D)
 	  sum(s in S)
 	    (services[s].duration_time-services[s].starting_time)*DriverServesService[d][s] <= drivers[d].max_working_time;
 
    //respect capacity bus
    forall(b in B)
      forall(s in S)
        busServesService[b][s]*buses[b].passangers_cap>=services[s].passangers_num;
        
    //use at most maxBuses
      (sum(b in B)
        sum(s in S)
          busServesService[b][s]!=0)<=maxBuses;
          
       
 	//same driver cannot serve overlap in time
 	
 	//respect working minutes for each driver
 
 }
 