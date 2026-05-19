# Arquitectura Técnica — HADES INTEROP

## Visión General

HADES INTEROP implementa el patrón **Hub-and-Spoke** para interoperabilidad: en lugar de que cada sistema conozca a todos los demás (N×N conexiones), cada uno solo conoce al hub central (N conexiones).

```
Sin HADES: N×(N-1)/2 conexiones bilaterales
Con HADES: N conexiones al hub central
Ejemplo: 20 dependencias = 190 conexiones vs 20 conexiones
```

---

## Flujo de una Instrucción PUJ

```
Dependencia A
     │
     │  POST /interop
     │  { "action": "...", "fuentes": [...] }
     ▼
┌─────────────────────────────────────┐
│  1. Validación estructural          │
│     └─ Campos requeridos            │
│     └─ Fuentes registradas          │
│                                     │
│  2. Despacho                        │
│     └─ Paralelo a cada fuente       │
│     └─ Timeout por fuente: 5s       │
│                                     │
│  3. Aggregación                     │
│     └─ Consolida resultados         │
│     └─ Calcula tiempo total         │
│                                     │
│  4. Firma de integridad             │
│     └─ Hash del payload completo    │
└─────────────────────────────────────┘
     │
     │  200 OK
     │  { "estado": "EJECUTADO", "resultados": {...}, "tiempo_ms": N }
     ▼
Dependencia A recibe respuesta unificada
```

---

## Protocolo Universal JSON (PUJ)

### Estructura de Solicitud

```json
{
  "action": "string (requerido)",
  "fuentes": ["array de fuentes (opcional)"],
  "parametros": { "objeto arbitrario (opcional)" },
  "prioridad": "NORMAL | ALTA | CRITICA (opcional)"
}
```

### Estructura de Respuesta

```json
{
  "meta": {
    "sistema": "HADES INTEROP",
    "protocolo": "PUJ",
    "version": "1.0.0"
  },
  "solicitud": { "action": "...", "fuentes": [...] },
  "estado": "EJECUTADO | ERROR | PARCIAL",
  "resultados": {
    "nombre_fuente": {
      "estado": "OK | NO_DISPONIBLE | ERROR",
      "datos": { ... }
    }
  },
  "tiempo_ms": 847,
  "integridad": "hash SHA-512 del payload",
  "timestamp": "ISO 8601"
}
```

### Acciones Estándar

| Action | Descripción |
|---|---|
| `ping` | Verificar conectividad con las fuentes |
| `consulta_ciudadano` | Consulta unificada por CURP |
| `consulta_vehiculo` | Consulta por placa o NIV |
| `alerta_institucional` | Enviar alerta a dependencias destino |
| `sincronizar` | Solicitar sincronización de registros (Pro) |

---

## Seguridad

### Autenticación (Open Core)
- Tokens por dependencia firmados con HMAC-SHA512
- Rotación automática cada 24h
- Lista blanca de IPs por dependencia

### Integridad de Datos
- Cada respuesta incluye hash del payload completo
- El receptor puede verificar que los datos no fueron alterados en tránsito
- Logs inmutables con timestamp del servidor

### Soberanía de Datos (HADES Pro)
- Todo el tráfico permanece dentro de la red interna estatal
- Sin telemetría externa
- Operable en hardware local (ARM/x86)

---

## Rendimiento

| Métrica | Valor objetivo |
|---|---|
| Latencia gateway (sin fuentes) | < 2ms |
| Latencia con 3 fuentes paralelas | < 500ms |
| Latencia máxima garantizada | < 2,000ms |
| Solicitudes concurrentes | 500+ (hardware estándar) |
| Disponibilidad objetivo | 99.5% |

---

## Despliegue

### Mínimo (Demo)
- Node.js 18+
- RAM: 512MB
- CPU: cualquier x86_64 o ARM64

### Producción recomendada
- 2 instancias con balanceador de carga
- RAM: 4GB por instancia
- Operable en Android/Termux para pilotos de bajo costo

---

*Ver [`protocolo-puj.md`](protocolo-puj.md) para la especificación completa.*
