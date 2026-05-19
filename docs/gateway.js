/**
 * HADES INTEROP — Motor de Enrutamiento PUJ
 * Protocolo Universal JSON v1.0
 *
 * Desarrollado en Jalisco, México
 * Licencia: HADES Open Core — ver LICENSE.md
 */

'use strict';

import { createServer } from 'http';
import { createHash, createHmac } from 'crypto';

// ─── Configuración ───────────────────────────────────────────────────────────

const CONFIG = {
  version: '1.0.0',
  port: process.env.PORT || 3000,
  maxBodySize: 1024 * 1024, // 1MB
  timeout: 5000,            // 5s por solicitud
};

const GATEWAY_META = {
  sistema: 'HADES INTEROP',
  protocolo: 'PUJ',
  version: CONFIG.version,
  region: 'Jalisco, México',
  soberania: '100% local',
};

// ─── Registro de Fuentes (adaptadores) ───────────────────────────────────────
// En producción, cada fuente tiene su propio adaptador que sabe cómo
// conectarse al sistema legacy correspondiente.

const FUENTES_REGISTRADAS = new Map([
  ['registro_civil',  { nombre: 'Registro Civil',           activa: true }],
  ['repuve',          { nombre: 'REPUVE',                   activa: true }],
  ['hacienda',        { nombre: 'Secretaría de Hacienda',   activa: true }],
  ['seguridad',       { nombre: 'Seguridad Pública',        activa: true }],
  ['imss',            { nombre: 'IMSS Jalisco',             activa: false }], // próxima integración
]);

// ─── Utilidades de seguridad ──────────────────────────────────────────────────

/**
 * Genera huella BLAKE3-compatible (SHA-512 truncado) para integridad
 * En producción usar la librería blake3-wasm para el hash real.
 */
function hashIntegridad(payload) {
  return createHash('sha512').update(JSON.stringify(payload)).digest('hex').slice(0, 64);
}

/**
 * Valida estructura mínima de una instrucción PUJ
 */
function validarInstruccion(instruccion) {
  if (!instruccion || typeof instruccion !== 'object') {
    return { valida: false, error: 'Cuerpo de solicitud inválido' };
  }
  if (!instruccion.action || typeof instruccion.action !== 'string') {
    return { valida: false, error: 'Campo "action" requerido' };
  }
  if (instruccion.fuentes && !Array.isArray(instruccion.fuentes)) {
    return { valida: false, error: 'Campo "fuentes" debe ser un arreglo' };
  }
  const fuentesDesconocidas = (instruccion.fuentes || [])
    .filter(f => !FUENTES_REGISTRADAS.has(f));
  if (fuentesDesconocidas.length > 0) {
    return { valida: false, error: `Fuentes no registradas: ${fuentesDesconocidas.join(', ')}` };
  }
  return { valida: true };
}

// ─── Motor de enrutamiento ────────────────────────────────────────────────────

/**
 * Despacha una instrucción PUJ a las fuentes solicitadas.
 * En producción, cada case llama al adaptador de sistema correspondiente.
 */
async function despachar(instruccion) {
  const fuentes = instruccion.fuentes || [];
  const resultados = {};

  for (const fuente of fuentes) {
    const meta = FUENTES_REGISTRADAS.get(fuente);
    if (!meta.activa) {
      resultados[fuente] = { estado: 'NO_DISPONIBLE', mensaje: 'Integración pendiente' };
      continue;
    }

    // Aquí iría la llamada al adaptador real del sistema legacy.
    // Por ahora retorna estructura de ejemplo para demostración.
    resultados[fuente] = await adaptadorSimulado(fuente, instruccion);
  }

  return resultados;
}

/**
 * Adaptador de demostración — reemplazar con conectores reales en producción.
 */
async function adaptadorSimulado(fuente, instruccion) {
  // Simula latencia de red interna (~10-50ms)
  await new Promise(r => setTimeout(r, Math.random() * 40 + 10));

  const demos = {
    registro_civil: { nombre: 'Ejemplo Ciudadano', vigente: true, tipo_documento: 'acta' },
    repuve:         { vehiculos: 1, ultimo_modelo: 2019, estatus: 'LIMPIO' },
    hacienda:       { adeudos: 'ninguno', rfc_valido: true },
    seguridad:      { antecedentes: false, alerta_activa: false },
  };

  return { estado: 'OK', datos: demos[fuente] || {} };
}

// ─── Servidor HTTP ────────────────────────────────────────────────────────────

const server = createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('X-Powered-By', 'HADES-INTEROP');
  res.setHeader('X-Protocolo', 'PUJ/1.0');
  res.setHeader('X-Region', 'Jalisco-MX');

  // Health check
  if (req.method === 'GET' && req.url === '/') {
    return res.end(JSON.stringify({ ...GATEWAY_META, estado: 'ACTIVO' }, null, 2));
  }

  // Estado de fuentes registradas
  if (req.method === 'GET' && req.url === '/fuentes') {
    const fuentes = Object.fromEntries(
      [...FUENTES_REGISTRADAS.entries()].map(([k, v]) => [k, v])
    );
    return res.end(JSON.stringify({ fuentes }, null, 2));
  }

  // Endpoint principal PUJ
  if (req.method === 'POST' && req.url === '/interop') {
    let body = '';
    let bodySize = 0;

    req.setTimeout(CONFIG.timeout, () => {
      res.statusCode = 408;
      res.end(JSON.stringify({ error: 'TIMEOUT', mensaje: 'Solicitud tardó demasiado' }));
    });

    req.on('data', chunk => {
      bodySize += chunk.length;
      if (bodySize > CONFIG.maxBodySize) {
        res.statusCode = 413;
        res.end(JSON.stringify({ error: 'PAYLOAD_GRANDE' }));
        req.destroy();
        return;
      }
      body += chunk;
    });

    req.on('end', async () => {
      const inicio = performance.now();

      let instruccion;
      try {
        instruccion = JSON.parse(body);
      } catch {
        res.statusCode = 400;
        return res.end(JSON.stringify({ error: 'JSON_INVALIDO' }));
      }

      const validacion = validarInstruccion(instruccion);
      if (!validacion.valida) {
        res.statusCode = 422;
        return res.end(JSON.stringify({ error: 'INSTRUCCION_INVALIDA', detalle: validacion.error }));
      }

      try {
        const resultados = await despachar(instruccion);
        const tiempo_ms = parseFloat((performance.now() - inicio).toFixed(2));

        const respuesta = {
          meta: GATEWAY_META,
          solicitud: { action: instruccion.action, fuentes: instruccion.fuentes || [] },
          estado: 'EJECUTADO',
          resultados,
          tiempo_ms,
          integridad: hashIntegridad(resultados),
          timestamp: new Date().toISOString(),
        };

        res.end(JSON.stringify(respuesta, null, 2));

      } catch (err) {
        res.statusCode = 500;
        res.end(JSON.stringify({ error: 'ERROR_INTERNO', mensaje: err.message }));
      }
    });

    return;
  }

  // 404 para cualquier otra ruta
  res.statusCode = 404;
  res.end(JSON.stringify({ error: 'RUTA_NO_ENCONTRADA', rutas: ['GET /', 'GET /fuentes', 'POST /interop'] }));
});

server.listen(CONFIG.port, () => {
  console.log(`
╔══════════════════════════════════════════════╗
║         HADES INTEROP — PUJ v${CONFIG.version}         ║
║  Interoperabilidad Gubernamental · Jalisco   ║
╚══════════════════════════════════════════════╝
  Puerto  : ${CONFIG.port}
  Fuentes : ${FUENTES_REGISTRADAS.size} registradas
  Estado  : ACTIVO
`);
});

export default server;
