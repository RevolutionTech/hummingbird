#include "sdl/SDL.h"
#include <iostream>

using namespace std;

int main(){
	Uint32 subsystem_mask=SDL_INIT_VIDEO|SDL_INIT_AUDIO;

	if(SDL_WasInit(subsystem_mask)==subsystem_mask)
	  printf("Video and Audio initialized.\n");
	else
	  printf("Video and Audio not initialized.\n");	
	/*
	cout << "Hello world!" << endl;*/
	return 0;
}
