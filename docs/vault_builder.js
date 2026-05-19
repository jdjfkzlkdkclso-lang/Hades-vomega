const crypto = require('crypto');
const fs = require('fs');
const readline = require('readline').createInterface({ input: process.stdin, output: process.stdout });

const question = (q) => new Promise((res) => readline.question(q, res));

(async () => {
    console.log("\n[!] GENERADOR DE BÓVEDA HADES");
    const key = await question("API_KEY: ");
    const pass = await question("MASTER_KEY: ");
    const salt = crypto.randomBytes(16), iv = crypto.randomBytes(12);
    const secret = crypto.pbkdf2Sync(pass, salt, 100000, 32, 'sha256');
    const cipher = crypto.createCipheriv('aes-256-gcm', secret, iv);
    let enc = cipher.update(key, 'utf8', 'hex');
    enc += cipher.final('hex');
    fs.writeFileSync('vault.hades', JSON.stringify({ iv: iv.toString('hex'), salt: salt.toString('hex'), tag: cipher.getAuthTag().toString('hex'), data: enc }));
    console.log("[OK] vault.hades creado.");
    process.exit(0);
})();
