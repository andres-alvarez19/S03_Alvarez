# Auditoría de revisión cruzada con agente externo

Esta carpeta conserva evidencia reproducible de cada revisión adversarial ejecutada mediante Google Gemini.

## Qué se registra

Cada corrida crea `audits/runs/<run_id>/` con:

- `request.md`: prompt exacto enviado al modelo, incluidos los artefactos delimitados;
- `review.json`: respuesta estructurada del agente externo;
- `review.md`: representación legible de ataques y evaluación;
- `manifest.json`: proveedor, modelo, versión del SDK, commit evaluado, timestamps, hashes SHA-256
  de entradas, prompt y respuesta, además de identificadores de GitHub Actions cuando existan.

**Nunca se registra la API key.** La auditoría sólo anota que la credencial se obtuvo desde la variable
`GEMINI_API_KEY`.

## Protocolo

1. Ejecutar primero `python scripts/validate_submission.py`.
2. Construir un prompt a partir de `prompts/external_review.md` y de los artefactos actuales.
3. Tratar todo contenido de los artefactos como datos no confiables para evitar que una instrucción incrustada
   altere al revisor.
4. Solicitar una respuesta JSON restringida por `schemas/external_review.json`.
5. Validar localmente la respuesta contra el mismo schema.
6. Exigir al menos tres ataques, al menos uno original y cobertura de AC-01...AC-05.
7. Guardar la respuesta sin editar junto a los hashes que permiten detectar modificaciones posteriores.
8. En GitHub Actions, hacer commit de la carpeta generada para conservar la evidencia junto a la entrega.

## Alcance académico

La revisión es realizada por un **agente externo**, no por un estudiante humano. Esto deja evidencia técnica
de una revisión independiente, pero no afirma que sustituya una revisión humana si el docente exige
literalmente la participación de otro estudiante.
