# Antigravity y GitHub

## Raices de trabajo

- `Note9` se recomienda trabajar desde `C:\Users\ZN-\Documents\Antigravity\Openclaw note 9`
- `laboratorio-metodos-mixtos` se trabaja desde `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos`

## Regla practica para Antigravity

Cada proyecto debe abrirse en Antigravity o VS Code desde su propia raiz git.

- Si abres `C:\Users\ZN-\Documents\Antigravity\Openclaw note 9`, Git opera sobre `zerausn/Note9`
- Si abres `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos`, Git opera sobre `zerausn/laboratorio-metodos-mixtos`

La raiz `C:\Users\ZN-\Documents\Antigravity` sigue existiendo como otra copia de trabajo de `Note9`, pero la ruta recomendada y limpia para Antigravity es `Openclaw note 9`.

No se debe trabajar el laboratorio desde ninguna copia de `Note9`, porque son repositorios independientes.

## Remotos

- `Note9` -> `git@github.com:zerausn/Note9.git`
- `laboratorio-metodos-mixtos` -> `git@github.com:zerausn/laboratorio-metodos-mixtos.git`

## Pull y push validados

Se validaron localmente los siguientes comandos:

```powershell
git pull --ff-only origin main
git push --dry-run origin main
```

Los dos funcionan en:

- `C:\Users\ZN-\Documents\Antigravity\Openclaw note 9`
- `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos`

## Git LFS

El repositorio `laboratorio-metodos-mixtos` usa `git-lfs` para los JSON grandes en `Nueva carpeta`.

Comandos utiles:

```powershell
git lfs install
git lfs pull
git lfs ls-files
```

## Archivo recomendado para abrir

Puedes abrir directamente:

- `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos\workspace.code-workspace`

o abrir la carpeta raiz del repo:

- `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos`

Para `Note9`, la carpeta recomendada es:

- `C:\Users\ZN-\Documents\Antigravity\Openclaw note 9`
