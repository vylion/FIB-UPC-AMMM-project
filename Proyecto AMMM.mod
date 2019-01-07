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
 
 tuple Drivers
 {
 	int max_working_time;
 	int BM;
 	float CBM;
 	float CEM; 
 }
 
 tuple Bus
 {
 	int passangers_cap;
 	float price_min;
 	float price_km;
 }
 
 range B = 1..numBuses;
 range D = 1..numDrivers;
 range S = 1..numServices;
 int service_overlap[S][S]=...;
 
 Service services[S]=...;
 Drivers drivers[D]=...;
 Bus buses[B]=...;
 
 dvar boolean busServesService[B][S];
 dvar boolean driverServesService[D][S];
 dvar int+ driverOvertime[D];
 dvar int+ driverHours[D];
 dvar float+ costBuses;
 dvar float+ costDrivers;
 
 minimize (costBuses + costDrivers);

 subject to
 {
 	// every service must be served by one bus
 	forall(s in S)
 	  sum(b in B)
 	    busServesService[b][s] == 1;
 	   
 	// every service must be served by one driver
 	forall(s in S)
 	  sum(d in D)
 	    driverServesService[d][s] == 1;

 	//same   bus cannot serve overlap in time
   forall(b in B, s1,s2 in S: s1!=s2)
     busServesService[b][s1] + busServesService[b][s2] + service_overlap[s1][s2] <= 2;
     
    //same driver cannot serve overlap in time
   forall(d in D, s1,s2 in S: s1!=s2)
     driverServesService[d][s1] + driverServesService[d][s2] + service_overlap[s1][s2] <= 2;
 	
 	// respect max hours for drivers
 	forall(d in D)
 	  (sum(s in S) services[s].duration_time*driverServesService[d][s]) <= drivers[d].max_working_time;
 
    // respect capacity bus
    forall(b in B, s in S)
        buses[b].passangers_cap >= services[s].passangers_num*busServesService[b][s];
    
    // use at most maxBuses
    sum(b in B)
      (sum(s in S)
        busServesService[b][s] >= 1) <= maxBuses;
 	 
 	 // total hours that a driver works
 	 forall(d in D)
	   driverHours[d] + driverOvertime[d] >= sum(s in S) driverServesService[d][s]*services[s].duration_time;
 	 
 	 // driver non-overtime hours can't exceed BM
  	 forall(d in D)
  	   driverHours[d] <= drivers[d].BM;
   
 	// cost of all buses
 	costBuses >= sum(b in B)
 	  sum(s in S)
 	    busServesService[b][s]*(services[s].kilometers*buses[b].price_km + services[s].duration_time*buses[b].price_min);
 	
 	// cost of all drivers
 	costDrivers >= sum(d in D)
 	  (driverOvertime[d]*drivers[d].CEM + driverHours[d]*drivers[d].CBM);
 }