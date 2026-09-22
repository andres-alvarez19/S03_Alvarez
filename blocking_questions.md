# Preguntas para cerrar ambigüedad

Estas preguntas derivan de las siete clases de dato bloqueante de la actividad. El `work_order.json`
incluye decisiones provisionales para poder construir el artefacto; si el docente entrega valores
oficiales, deben reemplazarse.

1. `source.test_runner` — ¿Cuál es el comando/runner autoritativo del repositorio objetivo?
   - A) el comando documentado por el repositorio;
   - B) el comando usado por CI;
   - C) si no existe ninguno, detener la admisión.
   - Coste de adivinar mal: producir archivos con forma de test que el repositorio real no descubre ni ejecuta.

2. `source.authority` — Si el informe de defecto contradice el comportamiento observable del repositorio, ¿qué fuente manda?
   - A) repositorio;
   - B) informe de defecto;
   - C) conservar ambos y marcar la contradicción como bloqueante.
   - Coste de adivinar mal: convertir una descripción obsoleta en un test que congela un comportamiento incorrecto.

3. `budget.run` — ¿El presupuesto propuesto de USD 0,50 y 300 s por corrida es aceptado para este encargo?
   - A) sí;
   - B) reemplazar por los valores entregados por el docente.
   - Coste de adivinar mal: diseñar una verificación de coste/latencia incompatible con la evaluación real.

status: needs_user_input para cualquier corrida real que no tenga resueltos los puntos 1 y 2.
