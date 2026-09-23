# Pendientes externos

1. **Configurar `GEMINI_API_KEY`** como repository secret en GitHub Actions. La credencial no puede ni debe guardarse en el repositorio.
2. **Ejecutar `external-agent-review`** una vez configurada la clave. La corrida generará y versionará la evidencia en `audits/runs/<run_id>/`.
3. **Schema oficial**: si aparece `schemas/work_order.json` del curso, reemplazar/comparar con el schema local y corregir diferencias.
4. **Valores oficiales del repositorio objetivo**: confirmar runner/comando de tests, autoridad de fuentes y presupuesto si el docente los entrega.
5. **Criterio docente sobre R3**: la solución deja auditada una revisión independiente con agente Gemini. Si la evaluación exige específicamente otro estudiante humano, esa parte no puede sustituirse técnicamente.
