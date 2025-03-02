const http = require('http');
const htmlHandler = require('./htmlResponses.js');
const jsonHandler = require('./jsonResponses.js');
const pyHandler = require('./pythonResponses.js');

const port = process.env.PORT || process.env.NODE_PORT || 3000;

const handleRequest = (request, response, parsedUrl) => {
  console.log(parsedUrl.pathname);
  if( request.method === 'GET'){
    if (parsedUrl.pathname === '/style.css') {
        htmlHandler.getCSS(request, response);
    } else if (parsedUrl.pathname === '/kam_care-02.png') {
        htmlHandler.getLogo(request, response);
    } else if (parsedUrl.pathname === '/drug.json') {
        jsonHandler.getJSON(request, response);
    } else if (parsedUrl.pathname === '/start-python') {
        pyHandler.startPythonScript(response);
    } else {
        htmlHandler.getIndex(request, response);
    }
  }
  else if (request.method === 'POST' && parsedUrl.pathname === '/start-text-to-speech') {
    pyHandler.startTextToSpeech(request, response);
  } else {
    // If it's not a recognized path or method
    response.statusCode = 404;
    response.end('Not Found');
  }
};

const onRequest = (request, response) => {
  const protocol = request.connection.encrypted ? 'https' : 'http';
  const parsedUrl = new URL(request.url, `${protocol}://${request.headers.host}`);
  handleRequest(request, response, parsedUrl);
};

http.createServer(onRequest).listen(port, () => {
  console.log(`Listening on 127.0.0.1:${port}`);
});
