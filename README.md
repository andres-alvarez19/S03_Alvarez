# S03 — Cumplimiento malicioso y subasta de criterios

Entrega preparada para el encargo **E-6: convertir informes de defecto en casos de prueba ejecutables**.

## Contenido

- `work_order.json`: orden final después de la subasta.
- `bitacora.md`: criterios iniciales, autoataques, correcciones, subasta y estado de R3.
- `blocking_questions.md`: bloque de preguntas derivado de los datos bloqueantes.
- `evals/`: banco mínimo obligatorio.
- `schemas/work_order.json`: **schema local reconstruido** desde la plantilla del apunte.
- `auction.json`: registro machine-readable de la subasta.
- `scripts/validate_submission.py`: validación estructural + reglas semánticas mínimas.
- `.github/workflows/validate.yml`: CI para ejecutar la validación local.

## Validación

```bash
python -m pip install -r requirements.txt
python scripts/validate_submission.py
```

## Importante

`schemas/work_order.json` es una reconstrucción local basada en los documentos de Semana 3.
No se afirma que sea idéntico al schema oficial mencionado por la asignatura.

La revisión cruzada R3 requiere otra persona. La bitácora incluye autoataques y plantillas de ataque,
pero mantiene la revisión real como pendiente en vez de inventar evidencia.
