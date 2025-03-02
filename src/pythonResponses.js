const { spawn } = require('child_process');
const path = require('path');

let pythonProcess = null;

const startPythonScript = (response) => {
  if (!pythonProcess) {
    const pyPath = path.join(__dirname, 'video.py'),
    pythonProcess = spawn('python', [pyPath]); // Ensure "video.py" is in the same directory or provide the correct path

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python Output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      console.log(`Python process exited with code ${code}`);
      pythonProcess = null; // Reset when process stops
    });

    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ message: 'Python script started' }));
  } else {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ error: 'Python script is already running' }));
  }
};

const stopPythonScript = (response) => {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
    console.log('Python script stopped.');

    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ message: 'Python script stopped' }));
  } else {
    response.writeHead(400, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ error: 'No Python script is currently running' }));
  }
};

module.exports = {
  startPythonScript,
  stopPythonScript,
};
