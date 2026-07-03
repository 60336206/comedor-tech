# Flujo de trabajo Git — COMEDOR-TECH

Roles según el examen:
- **master** → rama principal, acepta correcciones de los colaboradores (hace merge, valida conflictos).
- **main** → colaborador que modifica el módulo que **identifica al lector** (pantalla de escaneo/validación → `templates/validar.html` y las rutas `/validar`, `/api/validar`, `/api/atender` en `app.py`).
- **test** → colaborador que hace el **login** e **inicializa usuarios** (admin y colaborador → `app.py` sección `USUARIOS` y rutas `/login`, `/logout`).

---

## 0. Setup inicial (lo hace quien tenga el rol master)

```bash
mkdir comedor-tech && cd comedor-tech
# copiar aquí app.py, templates/, static/, requirements.txt
git init
git add .
git commit -m "chore: estructura base del proyecto Flask COMEDOR-TECH"
git branch -M master

# crear el repo remoto en GitHub primero, luego:
git remote add origin https://github.com/TU_USUARIO/comedor-tech.git
git push -u origin master
```

Crear las dos ramas de trabajo desde master:

```bash
git checkout -b main
git push -u origin main

git checkout master
git checkout -b test
git push -u origin test
```

---

## 1. Colaborador MAIN — módulo que identifica al lector

Este colaborador trabaja siempre sobre `templates/validar.html` (y las rutas de validación en `app.py`). Debe generar **al menos 3 commits** verificados en cada iteración (mínimo 5 commits en total según el enunciado, repartidos entre los 3 colaboradores).

```bash
git checkout main

# --- commit 1 ---
# editar templates/validar.html: p.ej. cambiar el placeholder del input
git add templates/validar.html
git commit -m "feat(main): ajustar formulario de escaneo de ticket"

# --- commit 2 ---
# editar templates/validar.html: agregar validación de campo vacío en JS
git add templates/validar.html
git commit -m "feat(main): validar campo vacío antes de escanear"

# --- commit 3 ---
# editar app.py: mensaje de error más descriptivo en /api/validar
git add app.py
git commit -m "fix(main): mejorar mensaje de error en validación de ticket"

git push origin main
```

---

## 2. Colaborador TEST — login e inicialización de usuarios

```bash
git checkout master
git checkout test

# --- commit 1 ---
# editar app.py: agregar un tercer usuario o rol "Super Usuario"
git add app.py
git commit -m "feat(test): inicializar usuarios admin y colaborador"

# --- commit 2 ---
# editar templates/login.html: mejorar validación de formulario
git add templates/login.html
git commit -m "feat(test): mejorar formulario de login"

git push origin test
```

---

## 3. Generar el conflicto entre MAIN y TEST

Para que el examen se cumpla ("por último debe generar el conflicto con Main y Test"), ambos colaboradores deben modificar **la misma línea** del mismo archivo (`app.py`), por ejemplo la línea del `secret_key` o de la sección `USUARIOS`.

En `main`:
```bash
git checkout main
# editar la línea: app.secret_key = "comedor-tech-secret-2026"
# cambiarla a: app.secret_key = "main-branch-secret-key"
git add app.py
git commit -m "chore(main): actualizar clave secreta de sesión"
git push origin main
```

En `test`:
```bash
git checkout test
# editar la MISMA línea: app.secret_key = "comedor-tech-secret-2026"
# cambiarla a: app.secret_key = "test-branch-secret-key"
git add app.py
git commit -m "chore(test): actualizar clave secreta de sesión"
git push origin test
```

Ahora el **master** intenta fusionar ambas ramas y aquí aparece el conflicto:

```bash
git checkout master
git merge main
# sin conflicto todavía (main entra limpio)

git merge test
# CONFLICT (content): Merge conflict in app.py
```

---

## 4. Resolver el conflicto con P4Merge

Configurar P4Merge como herramienta de merge (una sola vez):

```bash
git config --global merge.tool p4merge
git config --global mergetool.p4merge.path "C:/Program Files/Perforce/p4merge.exe"   # Windows
# en Linux/Mac: ruta al binario p4merge, ej: /usr/bin/p4merge
git config --global mergetool.p4merge.cmd "p4merge \$BASE \$LOCAL \$REMOTE \$MERGED"
```

Resolver el conflicto:

```bash
git mergetool
```

Se abrirá P4Merge con 4 paneles (Base, Local=master/main, Remote=test, Merged). Elegir manualmente la línea final (por ejemplo, dejar `"comedor-tech-secret-2026"` como valor definitivo, combinando ambos cambios).

Guardar y cerrar P4Merge, luego:

```bash
git add app.py
git commit -m "merge: resolver conflicto entre main y test usando P4Merge"
git push origin master
```

---

## 5. Validación final (master)

El rol **master** revisa que todo compile y corre la app para validar que el conflicto quedó bien resuelto:

```bash
pip install -r requirements.txt --break-system-packages
python3 app.py
```

Login de prueba: `admin / admin123` o `colaborador / colab123`
Ticket de prueba: código `221045`

```bash
git log --oneline --graph --all
```

Este último comando muestra el historial con las 3 ramas y el merge con conflicto resuelto — es lo que normalmente pide el docente para revisar el árbol de commits.
