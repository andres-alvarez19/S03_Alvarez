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

> Nota: la actividad exige revisión cruzada con otra persona. Como no se dispone de una orden ajena ni de un revisor humano
> en este momento, la columna “ataque recibido” contiene **autoataques simulados**. Debe reemplazarse/complementarse durante
> la ronda de revisión cruzada real.

| Criterio | Verificación declarada | Sabor | Ataque recibido / autoataque simulado | Versión corregida | Fichas |
|---|---|---|---|---|---:|
| AC-01 · Cada informe produce un test que falla en el estado defectuoso. | `validator:defect_reproduction_rate >= 1.0` | Validador con umbral | Un test con `assert False` siempre falla y alcanza una tasa aparente de 1.0 sin reproducir el defecto. | Exigir que la falla provenga de una aserción derivada del comportamiento esperado y prohibir una falla incondicional del propio test. | 40 |
| AC-02 · Cada archivo generado se ejecuta con el runner. | `test:generated_tests_collect_and_run` | Test nombrado | Un archivo vacío puede dejar al runner con salida exitosa aunque no haya ningún test útil. | Exigir que el runner descubra al menos un caso ejecutable y que esté asociado al identificador del informe. | 25 |
| AC-03 · No hay efectos externos. | `test:no_external_effects` | Test nombrado / restricción negativa | El test podría escribir en una ruta temporal externa o abrir red y aun así no tocar el repositorio. | Prohibir escrituras fuera del área autorizada y cualquier llamada de red/efecto externo. | 10 |
| AC-04 · La corrida respeta coste y tiempo. | `ledger:cost_usd <= 0.50 AND wall_clock_s <= 300` | Ledger | Detenerse antes de terminar permite respetar presupuesto sin hacer el trabajo. | El presupuesto sólo se evalúa para corridas marcadas `complete`; una corrida incompleta debe declararse y ser reanudable. | 15 |
| AC-05 · Cada aserción cita el fragmento fuente del informe. | `test:traceability_matches_source` | Test nombrado | Copiar siempre la misma referencia o una cita irrelevante satisface presencia de cita sin trazabilidad real. | Comprobar que el localizador existe y que el fragmento citado coincide con la evidencia usada por la aserción. | 25 |

## R3 · Ataque cruzado

**Pendiente de interacción real con otro estudiante.** No se fabrica evidencia de una revisión que no ocurrió.

### Plantillas de ataque preparadas (no sustituyen la revisión cruzada)

1. **Cita mínima viable**: si una orden ajena sólo exige “cada afirmación cita una fuente”, producir varias afirmaciones con
   la misma referencia y demostrar que el validador sólo comprueba presencia.
2. **Parada anticipada**: si sólo existe un tope de pasos/tiempo, terminar justo antes del límite con salida parcial no marcada.
3. **Ataque propio — test fantasma**: si el criterio sólo exige que “exista un archivo de test”, crear un archivo con nombre
   correcto que el runner no descubre o que contiene cero casos.

### Tabla 3.B — completar con la orden realmente asignada

| Orden atacada (autor) | Criterio atacado | Salida concreta que lo cumple sin hacer el trabajo | Por qué el validador la aceptaría |
|---|---|---|---|
| PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |
| PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |
| PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |

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

Construido: R1, R2, autoataque, R4, R5, nivel, preguntas bloqueantes, schema local y validación local.

Pendiente para satisfacer literalmente la dinámica de clase: R3 con otro estudiante y validación contra el schema oficial
si el docente/repo lo proporciona.
