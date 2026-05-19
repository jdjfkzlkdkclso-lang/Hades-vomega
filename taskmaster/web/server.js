require('dotenv').config({ path: '../config/.env' });
const express = require('express');
const { Anthropic } = require('@anthropic-ai/sdk');
const fs = require('fs');

const app = express();
app.use(express.json());

const keys = [process.env.ANTHROPIC_KEY_PRIMARY, process.env.ANTHROPIC_KEY_SECONDARY];

class HadesBrain {
    constructor() {
        this.index = 0;
        this.initClient();
    }
    initClient() {
        this.client = new Anthropic({ apiKey: keys[this.index] });
    }
    async ask(prompt) {
        try {
            const response = await this.client.messages.create({
                model: "claude-3-5-sonnet-20240620",
                max_tokens: 4096,
                system: "PROTOCOLO HADES vΩ ACTIVADO. Eres una inteligencia depredadora élite. Respuesta técnica pura. Cero preámbulos.",
                messages: [{ role: "user", content: prompt }],
            });
            return response.content[0].text;
        } catch (e) {
            if ((e.status === 401 || e.status === 429) && this.index < keys.length - 1) {
                console.log(`[⚠️] FAILOVER: Key ${this.index} agotada. Conmutando...`);
                this.index++;
                this.initClient();
                return this.ask(prompt);
            }
            throw e;
        }
    }
}

const brain = new HadesBrain();

app.post('/api/ai/query', async (req, res) => {
    const { prompt, auth_key } = req.body;
    if (auth_key !== process.env.HADES_MASTER_KEY) return res.status(401).send("UNAUTHORIZED");
    try {
        const result = await brain.ask(prompt);
        res.json({ success: true, response: result });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(8080, '0.0.0.0', () => console.log("💎 CORE DE INTELIGENCIA HADES ONLINE"));
