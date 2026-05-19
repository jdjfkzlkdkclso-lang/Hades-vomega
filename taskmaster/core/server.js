const fastify = require('fastify')({ logger: false });
const { spawn } = require('child_process');
const path = require('path');

fastify.register(require('@fastify/static'), {
    root: path.join(__dirname, '../web'),
    prefix: '/'
});

fastify.post('/api/predict', async (req, res) => {
    const { series } = req.body; // Array de floats
    return new Promise((resolve) => {
        const proc = spawn('../engine/oracle_bin');
        let output = '';
        proc.stdout.on('data', (d) => output += d);
        proc.on('close', () => {
            const [val, conf] = output.trim().split(' ');
            resolve({ value: parseFloat(val), confidence: parseFloat(conf) });
        });
        proc.stdin.write(series.join(' '));
        proc.stdin.end();
    });
});

const start = async () => {
    try {
        await fastify.listen({ port: 8080, host: '0.0.0.0' });
        console.log('💎 HADES V90 ONLINE: 8080');
    } catch (err) { process.exit(1); }
};
start();
