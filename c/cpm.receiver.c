/* 	cpm.reciever.c
	Ian Schofield
	2019 August 22

	USAGE
	./cpm.receiver <port> <instrumentName>
	./cpm.receiver 30404 CPM1
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>



void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
	/////////////////////////////////////
	int sockfd;
	int newsockfd;
	int portno;
	socklen_t clilen;
	char buffer[2048];
	struct sockaddr_in serv_addr;
	struct sockaddr_in cli_addr;
	int n;
	char *instrName;
	/////////////////////////////////////
	
	// get port number (to listen to) and instrument name from command line args
	if(argc < 2){
		fprintf(stderr,"ERROR: no port provided\n");
		exit(1);
	} else {	
		portno = atoi(argv[1]);
		instrName = argv[2];
		
		printf("Listening to connections on port [%d], instrument [%s]\n",
			portno, instrName);
	}
	
	
	
	// create TCP socket
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if(sockfd < 0) {
		error("ERROR opening socket");
	}
	
	// zero out the sockaddr_in structure
	bzero((char *) &serv_addr, sizeof(serv_addr));
	
	serv_addr.sin_family = AF_INET;				// internet socket (as opposed to unix socket)
    serv_addr.sin_addr.s_addr = INADDR_ANY;		// accept connections from any host
	serv_addr.sin_port = htons(portno);			// socket listens to this port
	
	// reuse socket after closing program
	int enable = 1;
	if( setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0 )
    	error("setsockopt(SO_REUSEADDR) failed");
	
	// bind socket with this host's IP address and port number
	if( bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0 )
		error("ERROR on binding");
		
	// listen on the socket for connections: block here...
	listen(sockfd, 5);
	
	clilen = sizeof(cli_addr);
	
	int i;
	for(;;) {
	
		// accept incoming connection from client
		newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
		if(newsockfd < 0)
			error("ERROR on accept");
		
		while(1) {
		bzero(buffer, sizeof(buffer));
		n = read(newsockfd, buffer, sizeof(buffer)-1);
		//printf("%d\n", n);
		printf("%s", buffer);
		
		}
		close(newsockfd);
	
	}
	close(sockfd);
	
	return 0;
}
