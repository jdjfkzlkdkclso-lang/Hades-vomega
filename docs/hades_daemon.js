const net = require('net');
const { spawn } = require('child_process');
const fs = require('fs');
const SOCKET = '/tmp/hades.sock';
let core = null;

if (fs.existsSync(SOCKET)) fs.unlinkSync(SOCKET);

function start() {
    if (core) core.kill();
    // Forzamos --expose-gc para el monitoreo cuántico
    core = spawn('node', ['--expose-gc', 'core_hades.js'], {
        env: { ...process.env },
        stdio: 'inherit'
    });
}

net.createServer((s) => {
    s.on('data', (d) => {
        const cmd = d.toString().trim().toUpperCase();
        if (cmd === 'RESTART') start();
        if (cmd === 'STATUS') s.write(`PID: ${core ? core.pid : 'OFF'}\n`);
    });
}).listen(SOCKET, () => {
    console.log(`[DEPREDADOR⁹⁰] Daemon en ${SOCKET}`);
    start();
});
