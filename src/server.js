const http = require('http');
const htmlHandler = require('./htmlResponses.js');
const jsonHandler = require('./jsonResponses.js');
const pyHandler = require('./pythonResponses.js');

const port = process.env.PORT || process.env.NODE_PORT || 3000;

const handleGet = (request, response, parsedUrl) => {
  console.log(parsedUrl.pathname);
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
};

const onRequest = (request, response) => {
  const protocol = request.connection.encrypted ? 'https' : 'http';
  const parsedUrl = new URL(request.url, `${protocol}://${request.headers.host}`);
  handleGet(request, response, parsedUrl);
};

http.createServer(onRequest).listen(port, () => {
  console.log(`Listening on 127.0.0.1:${port}`);
});
