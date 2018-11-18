#include <vector>
#include <iostream>
using namespace std;
struct service
{
    int begin;
    int duration;

    bool overlaps(service &s)
    {
        int end = this->begin + this->duration;
        int s_end = s.begin + s.duration;
        return this->begin <= s_end &&  s.begin <= end;
    }
};

int readInt()
{
    int a;
    cin>>a;
    return a;
}
int main() {

    vector<service> v_srv;
    int numServices = readInt();
    for(int i=0;i<numServices; ++i)
        v_srv.push_back({readInt(),readInt()});

    vector<vector<bool>> service_overlap(numServices, vector<bool>(numServices));

    for(int i=0; i<numServices; ++i)
        for(int j=0; j<numServices; ++j)
            service_overlap[i][j] = v_srv[i].overlaps(v_srv[j]);

    cout<<"service_overlap = ["<<endl;

   for(int i=0; i<numServices; ++i)
   {
	   cout<<"[ ";
	for(int j=0; j<numServices; ++j){
		cout<<service_overlap[i][j]<<", ";
	}
	cout<<"],"<<endl;
   }
   cout<<"];"<<endl;
}