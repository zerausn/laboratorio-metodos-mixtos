# Registro de decisiones tecnicas

Este archivo inicia el log de decisiones tecnicas formales para el repo
consolidado `Laboratorio metodos mixtos`.

## Decision 1 - Mantener historia previa en documentos ya existentes

- Contexto: el repo ya tenia historia en `HISTORIAL_CONVERSACIONES.md`,
  `REPO_FUSION_ASP.md` y otros documentos heredados.
- Decision: no duplicar toda esa historia aqui. Este archivo se usa para
  decisiones nuevas o para resumir cambios de arquitectura a partir de ahora.

## Decision 2 - Automatizacion baseline con validacion ligera

- Contexto: el repo tiene dependencias pesadas y opcionales que vuelven fragil
  una CI generica basada en instalar todo el stack en cada PR.
- Decision: la capa `.antigravity/automation.json` y el workflow
  `agent-validate.yml` arrancan con validacion por `compileall` sobre app,
  backend, tests y reconstruccion documental. La suite completa de `pytest`
  queda como objetivo posterior cuando el entorno quede mas portable.
