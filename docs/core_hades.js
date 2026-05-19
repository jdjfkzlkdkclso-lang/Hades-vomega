const crypto = require('crypto');
const fs = require('fs');
const { performance } = require('perf_hooks');
const { GoogleGenerativeAI } = require("@google/generative-ai");

const PHI = 1.618; // Umbral de la Sección Áurea (ms)

function decrypt(master) {
    const v = JSON.parse(fs.readFileSync('vault.hades', 'utf8'));
    const k = crypto.pbkdf2Sync(master, Buffer.from(v.salt, 'hex'), 100000, 32, 'sha256');
    const d = crypto.createDecipheriv('aes-256-gcm', k, Buffer.from(v.iv, 'hex'));
    d.setAuthTag(Buffer.from(v.tag, 'hex'));
    let res = d.update(v.data, 'hex', 'utf8');
    return res + d.final('utf8');
}

async function executeTask(genAI) {
    const start = performance.now();
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
    
    try {
        const res = await model.generateContent("TAREA: [ AUDITORÍA DE RED ELITE ]");
        const end = performance.now();
        const latency = end - start;

        process.stdout.write(`\n[💎 LATENCIA]: ${latency.toFixed(4)}ms`);
        
        if (latency > PHI) {
            process.stderr.write(`\n[⚠️ ANOMALÍA]: Latencia > PHI. Ejecutando purga V8...`);
            if (global.gc) {
                global.gc();
                process.stderr.write(` [OK] Memoria purgada.`);
            }
        }
        
        process.stdout.write(`\n[NÚCLEO]: ${res.response.text()}\n`);
    } catch (e) {
        process.stderr.write(`\n[ERROR]: ${e.message}\n`);
    }
}

const MK = process.env.HADES_MASTER_KEY;
if (!MK) process.exit(1);
const genAI = new GoogleGenerativeAI(decrypt(MK));

setInterval(() => executeTask(genAI), 15000);
