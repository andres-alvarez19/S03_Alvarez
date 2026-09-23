# S03 — Cumplimiento malicioso y subasta de criterios

Entrega preparada para el encargo **E-6: convertir informes de defecto en casos de prueba ejecutables**.

## Contenido

- `work_order.json`: orden final después de la subasta.
- `bitacora.md`: criterios iniciales, autoataques, correcciones, subasta y trazabilidad de R3.
- `blocking_questions.md`: bloque de preguntas derivado de los datos bloqueantes.
- `evals/`: banco mínimo obligatorio.
- `schemas/work_order.json`: **schema local reconstruido** desde la plantilla del apunte.
- `schemas/external_review.json`: contrato estructurado de la revisión externa.
- `auction.json`: registro machine-readable de la subasta.
- `prompts/external_review.md`: prompt exacto y auditable del revisor adversarial.
- `scripts/validate_submission.py`: validación estructural + reglas semánticas mínimas.
- `scripts/run_external_review.py`: ejecución de revisión cruzada mediante Google Gemini.
- `audits/`: protocolo y corridas inmutables de revisión externa.
- `.github/workflows/validate.yml`: CI para validar la entrega.
- `.github/workflows/external-review.yml`: workflow manual para ejecutar y auditar al agente externo.

## Validación local

```bash
python -m pip install -r requirements.txt
python scripts/validate_submission.py
```

## Revisión cruzada externa

La revisión adversarial se prepara para **Google Gemini** mediante el SDK oficial `google-genai`.
La credencial se lee únicamente desde `GEMINI_API_KEY`; no se versiona ni se imprime.

Configuración completa: `docs/external-review.md`.

Resumen operativo:

1. Crear una clave compatible con Gemini en Google AI Studio usando un proyecto del nivel gratuito.
2. Guardarla en GitHub Actions como repository secret `GEMINI_API_KEY`.
3. Ejecutar manualmente el workflow **external-agent-review**.
4. El workflow valida la entrega, llama una vez al modelo, valida la respuesta y hace commit de la auditoría en `audits/runs/<run_id>/`.

La corrida conserva el prompt exacto, respuesta JSON, versión legible, modelo, SDK, commit evaluado, timestamps y hashes SHA-256. Nunca conserva la API key.

## Importante

`schemas/work_order.json` es una reconstrucción local basada en los documentos de Semana 3.
No se afirma que sea idéntico al schema oficial mencionado por la asignatura.

La revisión de R3 quedará documentada como **revisión con agente externo**, no como revisión humana. Si el docente exige literalmente otro estudiante, esa condición seguirá requiriendo intervención humana.
