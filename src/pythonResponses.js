const { spawn } = require('child_process');
const path = require('path');

let pythonProcess = null;

const startPythonScript = (response) => {
  if (!pythonProcess) {
    const pyPath = path.join(__dirname, 'video.py'),
    pythonProcess = spawn('python', [pyPath]); 

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python Output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code, signal) => {
      console.log(`Python process exited with code ${code}`);
    });

    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ message: 'Python script started' }));
  } else {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ error: 'Python script is already running' }));
  }
};

const startTextToSpeech = (request, response) => {
    let body = '';
    request.on('data', chunk => {
        body += chunk.toString();
    });
    request.on('end', () => {
        const { text } = JSON.parse(body);  // Extract text from the body of the request
    
        if (!text) {
          response.statusCode = 400;
          response.end(JSON.stringify({ error: 'No text provided' }));
          return;
        }
        const pyPath = path.join(__dirname, 'text-to-speech.py');

    
        // Spawn Python process to handle Text-to-Speech
        const pythonProcess = spawn('python', [pyPath, text]);
        
        let result = '';
    
        pythonProcess.stdout.on('data', (data) => {
          result += data.toString();
        });
    
        pythonProcess.stderr.on('data', (data) => {
          console.error(`Python Error: ${data}`);
        });
    
        pythonProcess.on('close', (code) => {
          if (code === 0) {
            try {
              const parsedResult = JSON.parse(result);  // Expecting a JSON response from Python
    
              if (parsedResult.file) {
                response.statusCode = 200;
                response.setHeader('Content-Type', 'application/json');
                response.end(JSON.stringify({ message: 'Speech generated', file: parsedResult.file }));
              } else {
                response.statusCode = 500;
                response.end(JSON.stringify({ error: 'Error generating speech' }));
              }
            } catch (error) {
              response.statusCode = 500;
              response.end(JSON.stringify({ error: 'Error parsing Python response' }));
            }
          } else {
            response.statusCode = 500;
            response.end(JSON.stringify({ error: `Python process exited with code ${code}` }));
          }
        });
      });
};

module.exports = {
  startPythonScript,
  startTextToSpeech,
};
