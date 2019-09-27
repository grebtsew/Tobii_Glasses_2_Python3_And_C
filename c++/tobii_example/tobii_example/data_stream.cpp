#include "stdafx.h"
#include <string.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <stdio.h>
#include <string.h>
#include <winsock2.h>
#include <thread>

#pragma comment( lib, "ws2_32.lib")

using namespace std;
using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;       // Asynchronous streams

http_response POST_request(json::value data);
http_response GET_request(wstring baseURL);
void keep_alive_timer(string keep_alive_message);
void udp_socket_stream();
json::value get_json(http_response response);

const string SERVER = "192.168.71.50";	//ip address of udp server
const int BUFLEN = 512;	//Max length of buffer
const int PORT = 49152;	//The port on which to listen for incoming data

const string KA_DATA_MSG = "{\"type\": \"live.data.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}";
const string KA_EYES_MSG = "{\"type\": \"live.eyes.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}"; // used to sync eyes
const string KA_VIDEO_MSG = "{\"type\": \"live.video.unicast\", \"key\": \"some_other_GUID\", \"op\": \"start\"}";

struct sockaddr_in si_other;
SOCKET s;

int data_stream_main()
{
	printf("TOBII GLASSES 2 exampel in c++ \n");

	WSAData data;
	int err = WSAStartup(MAKEWORD(2, 2), &data);
	if (err != 0)
	{
		cout << "Failed. Error Code : " << err;
		exit(EXIT_FAILURE);
	}

	int slen = sizeof(si_other);
	char buf[BUFLEN];
	char message[BUFLEN];
	WSADATA wsa;

	//Initialise winsock
	printf(" Initialising Winsock...\n");
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		printf(" Failed.Error Code : %d", WSAGetLastError());
		Sleep(10000);
		exit(EXIT_FAILURE);
	}

	printf(" Create Socket \n");
	if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == SOCKET_ERROR)
	{
		printf(" socket() failed with error code : %d", WSAGetLastError());
		Sleep(10000);
		exit(EXIT_FAILURE);
	}

	//setup address structure
	memset((char *)& si_other, 0, sizeof(si_other));
	si_other.sin_family = AF_INET;
	si_other.sin_port = htons(PORT);
	si_other.sin_addr.S_un.S_addr = inet_addr(SERVER.c_str());

	printf("Will now connect and show streamed data\n");
	// OutputStream Keep alive thread
	std::thread keep_alive_thread(keep_alive_timer, KA_DATA_MSG); // change or add threads with more messages

	// InputStream Read udp socket stream
	std::thread udp_socket_stream(udp_socket_stream);

	keep_alive_thread.join();
	udp_socket_stream.join();

	return 0;
}

/* These functions handles the udp socket connection and stream */

void keep_alive_timer(const string keep_alive_message) {
	/*Send Keep Alive messages every second */

	int slen = sizeof(si_other);
	char message[BUFLEN];
	WSADATA wsa;

	std::string data_message = keep_alive_message;
	strcpy(message, data_message.c_str());


	printf("Start sending keep alive messages \n");
	while (1)
	{
		printf("Keep Alive Data Sent \n");
		if (sendto(s, message, strlen(message), 0, (struct sockaddr *) & si_other, slen) == SOCKET_ERROR)
		{
			printf(" sendto() failed with error code : %d", WSAGetLastError());
			Sleep(10000);
			exit(EXIT_FAILURE);
		}
		Sleep(2000);
	}

	closesocket(s);
	WSACleanup();
}

void udp_socket_stream() {
	/*
	Read and print Stream from udp socket.
	*/

	int slen = sizeof(si_other);
	char buf[BUFLEN];

	while (1)
	{
		//clear the buffer by filling null, it might have previously received data
		memset(buf, '\0', BUFLEN);
		//try to receive some data, this is a blocking call
		if (recvfrom(s, buf, BUFLEN, 0, (struct sockaddr *) & si_other, &slen) == SOCKET_ERROR)
		{
			printf(" recvfrom() failed with error code : %d", WSAGetLastError());
			Sleep(1000);
			exit(EXIT_FAILURE);
		}

		puts(buf);
	}

	closesocket(s);
	WSACleanup();

}


/* These functions handle communication with the rest api, if needed!
	I will only implement a small example, for more information about how to
	calibrate, check the python implementation.*/

json::value get_json(http_response response) {
	return response.extract_json(true).wait();
}

http_response POST_request(wstring baseURL, json::value data) {

	http_client httpClient(baseURL);

	http_response httpResponse = httpClient.request(methods::POST, data.as_string()).get();

	/* 
	if (httpResponse.status_code() == status_codes::OK)
	{
		wstring output = httpResponse.extract_utf16string().get();
		//	wcout << output << endl;
	}
	*/
	return httpResponse;
}

http_response GET_request(wstring baseURL) {
	wstring baseUrl = L"http://www.example.com";
	http_client httpClient(baseUrl);

	// Simple GET request
	http_response httpResponse = httpClient.request(methods::GET).get();
	/*
	if (httpResponse.status_code() == status_codes::OK)
	{
		wstring output = httpResponse.extract_utf16string().get();
		//	wcout << output << endl;
	}
	*/
	return httpResponse;

}

