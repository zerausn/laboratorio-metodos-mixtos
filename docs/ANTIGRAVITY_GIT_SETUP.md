# Antigravity y GitHub

## Raices de trabajo

- `Note9` se trabaja desde `C:\Users\ZN-\Documents\Antigravity`
- `laboratorio-metodos-mixtos` se trabaja desde `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos`

## Regla operativa

Cada proyecto debe abrirse en Antigravity o VS Code desde su propia raiz git.

- Si abres `C:\Users\ZN-\Documents\Antigravity`, Git opera sobre `zerausn/Note9`
- Si abres `C:\Users\ZN-\Documents\Antigravity\Laboratorio metodos mixtos`, Git opera sobre `zerausn/laboratorio-metodos-mixtos`

No se debe trabajar el laboratorio desde la raiz de `Note9`, porque son repositorios independientes.

## Remotos

- `Note9` -> `git@github.com:zerausn/Note9.git`
- `laboratorio-metodos-mixtos` -> `git@github.com:zerausn/laboratorio-metodos-mixtos.git`

## Pull y push validados

Se validaron localmente los siguientes comandos:

```powershell
git pull --ff-only origin main
git push --dry-run origin main
```

Los dos funcionan tanto en `Note9` como en `laboratorio-metodos-mixtos`.

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
