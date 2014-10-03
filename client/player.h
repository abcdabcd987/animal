#ifndef PLAYER_H_INCLUDE
#define PLAYER_H_INCLUDE

#include  <vector>
#include <string>

using namespace std;


/**
*@para my_id 0 present that your are the first player, while 1 present that your are the second player.
*@para operators all operators that 2 players had done. each element is in the format of <id,< <x,y> ,direction> >
**/
class Player{
private:
	int my_id;
	const vector<pair<int, pair<pair<int ,int>, char> > >  *operators;
public:
	Player(int _my_id,vector<pair<int, pair<pair<int ,int>, char> > >  *_operators):my_id(_my_id),operators(_operators){}
	~Player(){}

	/**
	*@return your AI name.
	**/
	string name();

	/** 
	*make a decision which animal goes.
	*@return the Animal which is localed at pair<int, int> would goes. The char is one of U(up),D(down),L(left),R(right).
	**/
	pair<pair<int, int> char> makeDecision();
};

#endif
