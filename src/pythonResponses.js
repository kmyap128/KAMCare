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


module.exports = {
  startPythonScript,
};
