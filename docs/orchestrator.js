const { GoogleGenerativeAI } = require("@google/generative-ai");
const fs = require('fs');

const API_POOL = [
    "AIzaSyBRfI0uywwHNHHjQI1OZqzNrt3NsFHFa1o",
    "AIzaSyDvsGDX4iEb8bOljrZfXf70rnqvl0qjZZI",
    "AIzaSyCLguwc1m8eIRYKNolkoQv-JDUgh1lFnfc",
    "AIzaSyCH54lq3s-Lwq83MNnpcsvzWTEQvu6a3PE",
    "AIzaSyAk2-W9RQKf_rvmJ_3362SQ5vRRCUL9LbU"
];

async function runTask(targetFile) {
    if (!targetFile || !fs.existsSync(targetFile)) {
        console.error("[!] Error: No se proporcionó archivo de tarea.");
        process.exit(1);
    }

    const taskContent = fs.readFileSync(targetFile, 'utf8');
    let success = false;

    for (const key of API_POOL) {
        try {
            const genAI = new GoogleGenerativeAI(key);
            const model = genAI.getGenerativeModel({ 
                model: "gemini-1.5-flash",
                systemInstruction: "HADES vΩ. Depredador⁹⁰. Cero prosa. Solo código puro ejecutable." 
            });

            console.log(`[>>] Intentando con Oráculo: ${key.substring(0, 8)}...`);
            const result = await model.generateContent(taskContent);
            const response = result.response.text();
            
            fs.writeFileSync('HADES_OUTPUT.md', response);
            console.log("[+] MATERIALIZADO: HADES_OUTPUT.md");
            success = true;
            break; 
        } catch (e) {
            console.warn(`[!] Oráculo saturado/inválido. Rotando...`);
        }
    }

    if (!success) console.error("[!!!] FALLO TOTAL: Todas las APIs agotadas.");
}

runTask(process.argv);
