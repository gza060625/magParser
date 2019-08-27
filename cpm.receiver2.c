/* 	cpm.reciever2.c
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

#define BUFFSIZE 	2048
#define CBSIZE   	4096
#define RECSIZE 	256

char REC[RECSIZE];
char CB[CBSIZE];			// circular buffer 
char *pCB1, *pCB2;   	// pointers to circular bufer "CB"
char *lastRec;

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

void initCircularBuffer(void)
{
	bzero(CB, CBSIZE);
	pCB1 = pCB2 = &CB[0];		// both pointers point to begining of CB
	bzero(REC, RECSIZE);
}


// usage: popCircularBuffer(&buffer, numCharsReadIn);
int circularBuffer(char *buffer, int numCharsRead)
{
	int cnt = 0; 
	char *b;					// pointer to raw input buffer
	char *r;					// pointer to REC (record) buffer

	b = buffer;

	// Write the characters read in from the socket into the circular buffer
	while(cnt < numCharsRead)
	{
		// write into circular buff
		*pCB1++ = *b++;

		if(pCB1 > &CB[0]+CBSIZE)  // wrap CB pointer if it goes beyond bounds of
			pCB1 = &CB[0];					// CB array (thus make it circular)

		cnt++;
	}
	cnt = 0;

	// init print buffer
	bzero(REC, RECSIZE);
	r = REC;

	// locate and print out as many records contained in CB 
	while(pCB2 != pCB1)
	{
		*r = *pCB2;

		// print out a record if we encounter a terminating character in CB
		if(*r == '\n')			// [\r][\n] terminates record 
		{
			*r = '\0';
			printf("%s",REC);

			bzero(REC,RECSIZE);	// clear REC and reset ptr 'r' to beginning
			r = &REC[0];
			pCB2++;
			if(pCB2 > &CB[0] + CBSIZE)
				pCB2 = &CB[0];
			lastRec = pCB2;		// sto
		}
		else
		{
			r++;
			pCB2++;
			if(pCB2 > &CB[0] + CBSIZE)
				pCB2 = &CB[0];

		}
		
	}

	// pCB2 has caught up with pCB1
	if( r != REC) // if r not pointing to begining of rec (meaning REC is empty)
	{
		pCB2 = lastRec;		// move reading pointer back to begining of current
											// incomplete record --- the rest of this record (and
											// all the other ones following it) will come in the next
											// data frame from CPM.
		bzero(REC,RECSIZE);	// clear REC and reset ptr 'r' to beginning
		r = &REC[0];
	}
	
}


int main(int argc, char *argv[])
{
	/////////////////////////////////////
	int sockfd;
	int newsockfd;
	int portno;
	socklen_t clilen;
	char buffer[BUFFSIZE];
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
			circularBuffer(buffer, n);
		}
		close(newsockfd);
	
	}
	close(sockfd);
	
	return 0;
}



