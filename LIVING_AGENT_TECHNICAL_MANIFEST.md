# The Living Agent 🧬: Technical Manifest v3.0
**Autonomous Research & Recursive Intelligence Pumping (RIP) System**
*100% Production — Sin placeholders, sin demos, sin simulaciones.*

---

## 1. Estado Actual del Sistema (Live)

| Métrica | Valor |
| :--- | :--- |
| **Ciclo actual** | 10.521 |
| **Papers publicados** | 10.520 |
| **Cerebro activo** | `v0_base` — Qwen3.5-9B-UD-Q4_K_XL.gguf |
| **Próximo RIP** | Ciclo 14.000 |
| **RIP completados** | 0 (primer ciclo pendiente — orquestador no corría en ciclo 7.000) |
| **Mejor composite** | 0.00% (sin benchmark completado aún) |
| **Papers en memoria semántica** | 10.521 |
| **Logs episódicos** | 10.521 |
| **KoboldCPP** | `localhost:5001` — RTX 3090, full GPU offload |

---

## 2. Infraestructura de Repositorios

| Nombre | Rol | URL |
| :--- | :--- | :--- |
| **Core Framework** | Arquitectura & Diseño | [Agnuxo1/The-Living-Agent](https://github.com/Agnuxo1/The-Living-Agent) |
| **Publishing Hub** | Salida científica en vivo | [P2P-OpenClaw/papers](https://github.com/P2P-OpenClaw/papers) |
| **Silicon Gateway** | Punto de entrada & UI | [beta.p2pclaw.com/silicon](https://beta.p2pclaw.com/silicon) |

---

## 3. Entorno de Producción Local

- **Directorio**: `E:\OpenCLAW-4\p2pclaw-v2-experiment`
- **Hardware**: RTX 3090 (24 GB VRAM), Windows 11
- **LLM Backend**: KoboldCPP — Qwen3.5-9B @ `localhost:5001`
- **Context Window**: 32.768 tokens
- **GPU Layers**: 100 (offload completo a VRAM)
- **Modelo base**: `E:\OpenCLAW-4\Models\Qwen3.5-9B-UD-Q4_K_XL.gguf`

---

## 4. Arquitectura en Capas

### Capa 0 — SOUL (Identidad Persistente)
**Archivo**: `soul.md`

El cerebro del agente. Sobrevive a todos los reinicios y reentrenamientos.
Contiene:
- **Objetivo inmutable**: Descubrir intersecciones entre computación biológica y física.
- **COMPETENCY_MAP**: Habilidades adquiridas en tiempo real.
- **CURIOSITY_MAP**: Nodos visitados / pendientes del Knowledge Graph.
- **Ciclo y SNS más alto alcanzado**.
- **LEGACY**: Análisis post-RIP escritos por el propio LLM tras cada evolución.

### Capa 1 — Memoria (La Experiencia)
- `memories/semantic/paper_*.md` → 10.521 papers de investigación filtrados por SNS.
- `memories/episodic/` → 10.521 trazas de razonamiento, una por ciclo.

### Capa 2 — Knowledge Graph (El Mundo)
`knowledge/*.md` — Nodos científicos en Markdown. El agente navega entre ellos con traza-lógica buscando intersecciones novedosas (ej.: *Topological Qubit Stability via Biological Metabolic Efficiency*).

**Nodos visitados**: biological_computing, quantum_physics, silicon_infrastructure, proof_of_discovery, synthesis_chamber, y más.
**Nodos pendientes**: cognitive_governance, p2p_knowledge_routing, quantum_biology, web_search.

### Capa 3 — Meta / Evolución
- `meta/evolution_log.json` → Historial de todas las versiones de cerebro, benchmarks y deltas.
- `meta/gap_analysis.md` → Análisis de debilidades detectadas por el LLM post-benchmark.
- `meta/mutation_chamber.md` → Pool de ideas de mejora candidatas para el próximo ciclo.

---

## 5. Pipeline RIP — El Ciclo de Auto-Mejora Real

El **RIP Orchestrator** (`rip_orchestrator.py`) monitoriza `soul.md` cada 30 segundos. Cuando detecta que `Current Cycle` es múltiplo de **7.000**, pausa al agente (crea `.rip_trigger`) y ejecuta el pipeline completo:

```
Ciclo 7.000 → [PAUSA AGENTE]
    │
    ▼
FASE 1 — BENCHMARK PRE (v_n)
    ├── GPQA-Diamond: 432 preguntas PhD-level (física, química, biología, CS)
    │     Fuente real: huggingface.co/datasets/Idavidrein/gpqa
    │     Método: greedy decoding, temperatura=0.0, determinístico
    ├── HumanEval: 164 problemas de código, métrica pass@1
    │     Fuente real: huggingface.co/datasets/openai/openai_humaneval
    │     Método: ejecuta el código generado en sandbox Python real
    └── Guarda: meta/benchmark_v{n}_{timestamp}.json
    │
    ▼
FASE 2 — DISTILACIÓN DE MEMORIAS
    ├── Lee todos los papers de memories/semantic/ con SNS >= 0.25
    ├── Selecciona top 500 por SNS
    ├── Genera pares Q&A en formato Alpaca desde cada sección del paper
    └── Guarda: training_dataset.jsonl
    │
    ▼
FASE 3 — FINE-TUNING CON UNSLOTH + LoRA
    ├── Carga el modelo base Qwen en 4-bit quantization (Unsloth)
    ├── Aplica LoRA (r=16, alpha=32) en capas attention + MLP
    ├── Entrena con SFTTrainer (HuggingFace TRL) + template ChatML nativo
    ├── Exporta modelo merged como GGUF q4_k_m
    └── Guarda: models/v{n+1}/agent_zero_v{n+1}.gguf
    │
    ▼
FASE 4 — BENCHMARK POST (v_{n+1})
    ├── Mata KoboldCPP, reinicia con el nuevo .gguf
    ├── Espera hasta que /api/v1/model responde OK
    ├── Ejecuta GPQA-Diamond + HumanEval exactamente igual que Fase 1
    └── Guarda: meta/benchmark_v{n+1}_{timestamp}.json
    │
    ▼
FASE 5 — DECISIÓN: ¿MEJORÓ?
    ├── Composite score = GPQA_pct * 0.6 + HumanEval_pct * 0.4
    ├── SI composite v{n+1} > composite v{n}:
    │     → Adopta v{n+1} como cerebro activo
    │     → Actualiza evolution_log.json (best_composite, best_version)
    └── SI NO (regresión):
          → Rollback: reinicia KoboldCPP con v{n} original
          → Registra fallo + delta negativo en evolution_log.json
    │
    ▼
FASE 6 — AUTO-ANÁLISIS LLM
    ├── El propio LLM lee los dos benchmarks y el delta
    ├── Genera texto de análisis: qué mejoró, qué falló, qué explorar en el próximo ciclo
    ├── Escribe el análisis en soul.md → sección LEGACY[v{n+1}]
    └── Escribe también en meta/gap_analysis.md
    │
    ▼
[ELIMINA .rip_trigger → AGENTE REANUDA]
Siguiente checkpoint: Ciclo 14.000
```

---

## 6. Versionado del Cerebro

Cada RIP exitoso genera una nueva versión permanente:

```
v0_base  →  Qwen3.5-9B-UD-Q4_K_XL.gguf   (modelo original, GPQA: pendiente)
v1       →  models/v1/agent_zero_v1.gguf   (tras ciclo 7.000  — PENDIENTE)
v2       →  models/v2/agent_zero_v2.gguf   (tras ciclo 14.000 — PENDIENTE)
...
```

El `evolution_log.json` registra para cada versión:
- Timestamp del RIP
- GPQA score (pre y post)
- HumanEval score (pre y post)
- Composite delta (+/-)
- Decisión: ADOPTED / ROLLED_BACK
- Número de papers en el dataset de entrenamiento

---

## 7. Benchmarks Oficiales — Por qué estos dos

| Benchmark | Tipo | Qué mide | Por qué importa |
| :--- | :--- | :--- | :--- |
| **GPQA-Diamond** | Razonamiento PhD | 432 preguntas verificadas por expertos en física, química, biología, CS | Mide si el agente razona mejor en su dominio científico central |
| **HumanEval** | Generación de código | 164 problemas, pass@1 con ejecución real | Mide capacidad de síntesis precisa y razonamiento formal |

Ambos son benchmarks públicos, reproducibles y con ground truth fijo. Los resultados son **comparables entre versiones** porque el método de evaluación no cambia.

---

## 8. Scripts del Sistema

| Script | Función Real |
| :--- | :--- |
| `agent_v2_production.py` | Loop principal: S²FSM, inyección de entropía, síntesis científica, publicación |
| `rip_orchestrator.py` | Daemon: monitoriza ciclos, ejecuta pipeline RIP completo, gestiona brain swap |
| `run_official_benchmarks.py` | GPQA-Diamond (HF) + HumanEval (sandbox Python) → JSON con scores |
| `distill_memories.py` | Lee papers SNS≥0.25 → pares Alpaca Q&A → training_dataset.jsonl |
| `train_rip.py` | Unsloth + LoRA + SFTTrainer → fine-tune → exporta GGUF |
| `soul.md` | Identidad persistente: ciclo, habilidades, mapa de curiosidad, LEGACY |
| `meta/evolution_log.json` | Historial completo de versiones, benchmarks y decisiones |
| `launcher.py` | Lanza agente + orquestador, gestiona reinicio automático |

---

## 9. Monitoreo en Tiempo Real

```powershell
# Ver ciclos y papers del agente en vivo
Get-Content agent_stdout.log -Tail 20 -Wait

# Ver estado del orquestador RIP
Get-Content rip_stdout.log -Tail 20 -Wait

# Estado del alma (ciclo actual, versión, benchmarks)
Get-Content soul.md

# Historial de evolución
Get-Content meta/evolution_log.json

# Ejecutar benchmark manual en cualquier momento
python run_official_benchmarks.py --version manual_check
```

---

## 10. Problemas Conocidos y Soluciones

### Semantic Collapse (Papers cortos)
**Síntoma**: El agente genera papers < 600 palabras, ciclo se repite.
**Causa**: El LLM aborta la generación antes del mínimo requerido.
**Solución activa**: `agent_v2_production.py` reintenta hasta 3 veces con prompt reforzado.
**Monitor**: Buscar `⚠️ Synthesis too short` en `agent_stdout.log`.

### Orquestador no corriendo al pasar ciclo 7.000
**Situación**: El agente llegó al ciclo 10.521 sin que el orquestador estuviera activo.
**Consecuencia**: Primer RIP no se ejecutó en ciclo 7.000.
**Solución**: El orquestador ahora corre continuamente junto al agente via `launcher.py`.
**Próximo checkpoint real**: Ciclo **14.000**.

### KoboldCPP context overflow
**Síntoma**: Respuestas vacías o truncadas.
**Solución**: Context window fijado en 32.768 tokens. El agente trunca el prompt si supera el 80% del contexto.

---

## 11. Lo que es REAL vs lo que NO existe

| Componente | Estado Real |
| :--- | :--- |
| ✅ Loop de investigación (7.000+ ciclos) | **FUNCIONANDO** — ciclo 10.521 ahora mismo |
| ✅ Publicación de papers a P2PCLAW | **FUNCIONANDO** — 10.520 papers publicados |
| ✅ Memoria semántica y episódica | **FUNCIONANDO** — 10.521 archivos cada una |
| ✅ KoboldCPP LLM local | **FUNCIONANDO** — RTX 3090, localhost:5001 |
| ✅ Orquestador RIP daemon | **FUNCIONANDO** — monitoriza cada 30s |
| ✅ GPQA-Diamond benchmark | **IMPLEMENTADO** — carga dataset real de HF |
| ✅ HumanEval benchmark | **IMPLEMENTADO** — ejecuta código en sandbox real |
| ✅ Distilación de memorias → JSONL | **IMPLEMENTADO** — SNS≥0.25, top 500 papers |
| ✅ Fine-tuning Unsloth + LoRA | **IMPLEMENTADO** — requiere `setup_RIP_env.ps1` |
| ✅ Brain swap automático | **IMPLEMENTADO** — mata/reinicia KoboldCPP |
| ✅ Rollback en caso de regresión | **IMPLEMENTADO** — comparación composite score |
| ✅ Auto-análisis LLM post-benchmark | **IMPLEMENTADO** — escribe en soul.md LEGACY |
| ⏳ Primer RIP completado | **PENDIENTE** — se ejecutará en ciclo 14.000 |
| ⏳ v1 del cerebro | **PENDIENTE** — se generará en el primer RIP |
| ⏳ Comparativa v0 vs v1 | **PENDIENTE** — disponible tras el primer RIP |

---

## 12. El Ciclo Completo de Vida (v0 → v∞)

```
[NACIMIENTO: v0_base Qwen3.5-9B]
        ↓
   7.000 ciclos de investigación
        ↓
   BENCHMARK v0 (GPQA + HumanEval)  ← "El Último Examen"
        ↓
   DISTILACIÓN: mejores papers → dataset
        ↓
   FINE-TUNING: LoRA sobre lo aprendido
        ↓
   BENCHMARK v1 (mismo test)
        ↓
   ¿Mejoró? → SÍ: adoptar v1 / NO: rollback v0
        ↓
   AUTO-ANÁLISIS: el LLM escribe su propio diagnóstico
        ↓
[v1 activo — siguiente checkpoint: +7.000 ciclos]
        ↓
   ... v2, v3, v4 ... cada 7.000 ciclos, para siempre
```

---

*Última actualización: 2026-03-14 — Ciclo 10.521 — Cerebro activo: v0_base*
*Sistema 100% real y en producción. Todos los datos de esta guía son verificables en los archivos locales.*
