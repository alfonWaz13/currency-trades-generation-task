# 🧩 Prueba Técnica – Alfonso Ramírez

Esta es la resolución completa de la prueba técnica realizada por Alfonso Ramírez.

---

## ⚙️ Requisitos previos

### Entorno Python

Antes de ejecutar el proyecto, es necesario crear un entorno virtual como se indicaba en el README original de la prueba. 
Una vez creado y activado, deben instalarse tanto las dependencias principales como las de desarrollo, presentes en los 
archivos `requirements.txt` y `requirements-dev.txt`.


🍎 **MACOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

🪟**WINDOWS**
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```



### Base de datos MySQL (Docker)

El proyecto utiliza una base de datos MySQL desplegada mediante `docker-compose`.

**Antes de ejecutarlo, es importante asegurarse de que el puerto `3306` esté libre.**
En caso de tener MySQL corriendo localmente en ese puerto, se debe detener temporalmente para evitar conflictos. 
Una vez liberado el puerto, se puede ejecutar el archivo `docker-compose.yml` para levantar la base de datos con la 
configuración necesaria.

```bash
docker-compose up -d
```
Esto creará un contenedor de MySQL con las credenciales y la base de datos necesarias para el proyecto.

---

## 🧠 Estructura y evolución del proyecto

Cada paso de la resolución ha sido desarrollado en una rama independiente. A medida que se completaba cada bloque 
funcional, se mergeaba a la rama `main`. Esto permite ver con claridad la evolución progresiva del desarrollo y la 
organización modular de la solución.

La rama `main` está limpia, estructurada y muestra el avance de la implementación. 

En lugar de mergear las ramas originales de cada step, de han copiado los tests que probaban cada una de las
funcionalidades. Se hizo esto para agilizar el desarrollo y para que el arbol de commits quedase más limpio. En un
desarrollo real iría rebaseando cada rama para incluir nuevos cambios, pero ya desde la primera rama el repositorio
cambió bastante.
---

## ✍️ Commits bien documentados

**Los commits son bastante clarificadores** y dejan claro: 

- Qué se resolvió en cada momento.
- Qué problemas se detectaron.
- Qué soluciones se aplicaron.

Leyendo los commits se puede seguir de forma detallada y razonada todo el proceso de resolución de la prueba.

---

## 🔄 Diseño desacoplado y flexible

El proyecto incluye las clases `MemoryCurrencyTradeIdRepository` y `SqliteCurrencyTradeIdRepository`, que no forman 
parte de la implementación final, pero se han conservado para que no pase desapercibido que se ha hecho una evolución
del repositorio conforme se han ido viendo nuevas necesidades. Cambiar de uno a otro es sencillo y simplemente es necesario
instanciar la clase final que se va a utilizar en el archivo de tests end to end. **En la implementación del sistema real 
estas clases se borrarían por no ser utilizadas.**

---

## ✅ Ejecución de tests

Una vez instalado el entorno virtual, las dependencias, y levantada la base de datos MySQL en Docker, es posible 
ejecutar los tests.

```bash
python -m pytest
```

---

Gracias! 😄

**Alfon**
