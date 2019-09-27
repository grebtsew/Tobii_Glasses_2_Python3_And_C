#include "stdafx.h"
#include <string.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cpprest/http_client.h>
#include <cpprest/filestream.h>

using namespace std;
using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace concurrency::streams;       // Asynchronous streams

int data_stream_main();
http_response POST_request(json::value data);