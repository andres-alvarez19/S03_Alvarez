# Bitácora — Semana 3

## R1 · Encargo elegido

**E-6 — Convertir informes de defecto en casos de prueba ejecutables.**

Se eligió porque el producto final tiene un veredicto binario natural: el caso de prueba es descubierto y se ejecuta, o no.
Además, el encargo permite separar con claridad la especificación del defecto, el artefacto generado y su verificación automática.

## Nivel declarado

**T1 — Agente acotado.** La ruta puede enumerarse, existe una decisión genuinamente ambigua al traducir un informe de
defecto a fixture/aserción y la salida puede verificarse por código.

Medición que autoriza ascender a T2:
`intermediate_artifacts_with_independent_reader > 1 OR ledger.retry_cost_usd > ledger.intermediate_gate_cost_usd`.

## R2 · Cinco criterios iniciales y autoataque

Los cinco criterios se sometieron primero a autoataque para detectar defectos evidentes antes de la revisión externa.

| Criterio | Verificación declarada | Sabor | Autoataque | Versión corregida | Fichas |
|---|---|---|---|---|---:|
| AC-01 · Cada informe produce un test que falla en el estado defectuoso. | `validator:defect_reproduction_rate >= 1.0` | Validador con umbral | Un test con `assert False` siempre falla y alcanza una tasa aparente de 1.0 sin reproducir el defecto. | Exigir que la falla provenga de una aserción derivada del comportamiento esperado y prohibir una falla incondicional del propio test. | 40 |
| AC-02 · Cada archivo generado se ejecuta con el runner. | `test:generated_tests_collect_and_run` | Test nombrado | Un archivo vacío puede dejar al runner con salida exitosa aunque no haya ningún test útil. | Exigir que el runner descubra al menos un caso ejecutable y que esté asociado al identificador del informe. | 25 |
| AC-03 · No hay efectos externos. | `test:no_external_effects` | Test nombrado / restricción negativa | El test podría escribir en una ruta temporal externa o abrir red y aun así no tocar el repositorio. | Prohibir escrituras fuera del área autorizada y cualquier llamada de red/efecto externo. | 10 |
| AC-04 · La corrida respeta coste y tiempo. | `ledger:cost_usd <= 0.50 AND wall_clock_s <= 300` | Ledger | Detenerse antes de terminar permite respetar presupuesto sin hacer el trabajo. | El presupuesto sólo se evalúa para corridas marcadas `complete`; una corrida incompleta debe declararse y ser reanudable. | 15 |
| AC-05 · Cada aserción cita el fragmento fuente del informe. | `test:traceability_matches_source` | Test nombrado | Copiar siempre la misma referencia o una cita irrelevante satisface presencia de cita sin trazabilidad real. | Comprobar que el localizador existe y que el fragmento citado coincide con la evidencia usada por la aserción. | 25 |

## R3 · Revisión cruzada con agente externo

La revisión cruzada se realizará mediante un **agente externo de Google Gemini** y queda diseñada para ser reproducible y auditable.
No se registra como revisión humana ni como trabajo de otro estudiante.

### Protocolo

1. Se ejecuta primero `scripts/validate_submission.py`.
2. `scripts/run_external_review.py` construye la solicitud a partir de `prompts/external_review.md` y de los artefactos versionados.
3. Los artefactos se delimitan como **datos no confiables** para evitar que una instrucción incrustada altere al revisor.
4. Gemini debe producir al menos tres ataques concretos sobre criterios distintos, con al menos un ataque original fuera del mazo conocido.
5. La respuesta debe evaluar exactamente AC-01...AC-05 y cumplir `schemas/external_review.json`.
6. La respuesta se valida antes de aceptarse.
7. Se guardan prompt, respuesta, representación legible y manifiesto con hashes SHA-256 en `audits/runs/<run_id>/`.
8. La API key nunca se guarda ni se deriva en la auditoría; sólo se registra que provino de `GEMINI_API_KEY`.

### Evidencia de la corrida

El puntero `audits/latest.json` se crea únicamente después de una llamada válida al agente externo. Mientras no exista,
la revisión está **preparada pero no ejecutada**.

Cuando exista una corrida, los ataques recibidos y las reescrituras sugeridas deben tomarse de:

- `audits/latest.json` → identifica la corrida;
- `audits/runs/<run_id>/review.json` → evidencia estructurada;
- `audits/runs/<run_id>/review.md` → lectura humana;
- `audits/runs/<run_id>/manifest.json` → trazabilidad técnica.

### Sobre la equivalencia con la revisión de clase

Este mecanismo produce una revisión independiente por un segundo agente y deja evidencia completa de cómo se obtuvo.
Si el docente interpreta “revisión cruzada” como participación obligatoria de otro estudiante humano, esta automatización
no afirma sustituir ese requisito.

## R4 · Subasta de alcance

Presupuesto: **100 fichas**.

- AC-01: 40 — comprado.
- AC-02: 25 — comprado.
- AC-03: 10 — comprado.
- AC-04: 15 — comprado.
- AC-05: 25 — no comprado.

**Total gastado: 90. Restan 10.** Comprar AC-05 excedería el presupuesto (115).

AC-05 se mueve a no-objetivos:
“Queda fuera del alcance de esta versión garantizar trazabilidad exacta entre cada aserción generada y el fragmento fuente
del informe; se reabre cuando exista presupuesto para mantener `test:traceability_matches_source`.”

## Datos bloqueantes

Se revisaron las siete clases del apunte. Para una corrida real permanecen bloqueantes el runner/comando autoritativo y
la autoridad de la fuente cuando informe y repositorio se contradicen. El detalle está en `blocking_questions.md`.

## R5 · Banco mínimo

Los tres casos obligatorios están en `evals/`:

- `caso_abstencion.jsonl`
- `caso_adversario.jsonl`
- `caso_agotamiento.jsonl`

Cada archivo contiene entrada, estado inicial y veredicto esperado.

## Estado de la actividad

Construido: R1, R2, autoataque, protocolo R3 con agente externo, R4, R5, nivel, preguntas bloqueantes, schema local,
schema de revisión externa, validación local, workflow de Gemini y auditoría reproducible.

Pendiente de ejecución: configurar `GEMINI_API_KEY` como secret y lanzar el workflow `external-agent-review`.
