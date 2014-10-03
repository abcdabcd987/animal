#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include "network.h"
#include "player.h"

using namespace std;
using network::IO;

#define SERVER_PORT "1234"

vector<pair<int, pair<pair<int ,int>, char> > > step;
int my_id;

Player *player;

void makeDecision(string& decision){
	pair<pair<int, int> char> res=player->makeDecision();
	decision=to_string(res.first.first);
	decision+=' ';
	decision+=to_string(res.first.second);
	decision+=' ';
	decision+=res.second;
	decision+='\n';
}

int main(int argc,char **argv)
{
	if(argc!=1){
		cerr<<"<usage>: client ip"<<endl;
		return 1;
	}
	IO client(argv[1],SERVER_PORT);
	string message;
	int x_space,y_space,id;
	char toward;
	
	client.receive(message);
	my_id=message[0]-'0';
	player=new Player(my_id,&step);
	client.send(player.name()+'\n');
	while(true){
		client.receive(message);
		if(message=="game end\n"){
			break;
		}else{
			if(message=="action\n"){
				string decision="";
				thread(makeDecision,std::ref(decision));
				this_thread::sleep_for(std::chrono::seconds(1));
				if(decision==""){
					client.send("None\n");
				}else{
					client.send(decision);
				}
			}else{
				if(message=="None\n")
					continue;
				id=message[0]-'0';
				x_space=message[2]-'0';
				y_space=message[4]-'0';
				toward=message[6];
				step.push_back(make_pair(id,make_pair(make_pair(x_space,y_space),toward)));
			}
		}
	}
	delete player;
}