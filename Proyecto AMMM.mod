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
 int service_overlap[S][S]=...;
 
 dvar float+ cost;
 
 dvar boolean busServesService[B][S];
 dvar boolean DriverServesService[D][S];
 dvar boolean driverMoreThanBM[D];
 dvar int driverOvertime[D];
 dvar int driverHours[D];
 
 minimize  sum(b in B, s in S)	busServesService[b][s]*(services[s].kilometers*buses[b].price_km + services[s].duration_time*buses[b].price_min)
 +sum (d in D) driverMoreThanBM[d]*driverOvertime[d]*drivers[d].CEM + sum(d in D)driverMoreThanBM[d]*drivers[d].BM*drivers[d].CBM 
 + sum ( d in D) (driverMoreThanBM[d]==0)*drivers[d].CBM*driverHours[d];;

 			
 subject to
 {
 	//same 	bus cannot serve overlap in time
 	forall(b in B, s1,s2 in S)
 	  busServesService[b][s1] + busServesService[b][s2] + service_overlap[s1][s2] <= 2;
 	 //same driver cannot serve overlap in time
 	 forall(d in D, s1,s2 in S)
 	  DriverServesService[d][s1] + DriverServesService[d][s2] + service_overlap[s1][s2] <= 2;
 	
 	//respect max hours for drivers
 	forall(d in D)
 	  (sum(s in S) services[s].duration_time*DriverServesService[d][s]) <= drivers[d].max_working_time;
 
    //respect capacity bus
    forall(b in B)
      forall(s in S)
        busServesService[b][s]*buses[b].passangers_cap>=services[s].passangers_num;
        
    //use at most maxBuses
      (sum(b in B)
        sum(s in S)
          busServesService[b][s])<=maxBuses;
          
 	//respect working minutes for each driver
 	forall(d in D)
 	  (sum(s in S) DriverServesService[d][s]*services[s].duration_time) <= drivers[d].max_working_time;
 	 
 	 //hours that a driver works
 	 forall(d in D)
 	     driverHours[d] >= sum(s in S) DriverServesService[d][s]*services[s].duration_time;
 	 
 	 //if a driver works overtime
  	 forall(d in D)
 	     driverMoreThanBM[d] == drivers[d].BM <= sum(s in S) DriverServesService[d][s]*services[s].duration_time ;
 	 
 	 //get time overtime
	 forall(d in D)
	     driverOvertime[d] >= driverMoreThanBM[d]*(driverHours[d]-drivers[d].BM);
   

 	
 }
