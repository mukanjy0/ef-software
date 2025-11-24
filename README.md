# Solution

```bash
# Run the CLI app
python grade_calculator.py

# Run tests
python -m unittest test_grade_calculator.py
# or
python -m unittest discover
```

# Enunciado - CS3081 — Examen Parcial (2025-2)

## 2. Desarrollo e Implementación (11 pts)

Se debe implementar un módulo de **cálculo de la nota final**, alineado con los RF y RNF.

**Condiciones del desarrollo**

- Lenguaje libre.
- Ejecución por terminal.
- No requiere base de datos ni interfaz gráfica.
- Priorizar funcionalidad, modularidad y buena estructura.

---

## ✅ Requerimientos Funcionales (RF)

### **RF01 — Registro de Evaluaciones**

El docente podrá registrar las evaluaciones de un estudiante:

- Nota obtenida
- Porcentaje/peso sobre la nota final  
  **Variable:** `examsStudents`

### **RF02 — Asistencia Mínima**

El docente podrá registrar si el estudiante cumplió la asistencia mínima requerida.  
**Variable:** `hasReachedMinimumClasses`

### **RF03 — Política de Puntos Extra**

El docente podrá registrar, por año académico, si existe aprobación docente para otorgar puntos extra.  
**Variable:** `allYearsTeachers` (True/False)

### **RF04 — Cálculo de Nota Final**

El docente podrá solicitar el cálculo considerando:

- Evaluaciones
- Asistencia mínima
- Política de puntos extra

### **RF05 — Detalle del Cálculo**

El docente podrá visualizar:

- Promedio ponderado
- Penalización por inasistencias
- Puntos extra aplicados

---

## ✅ Requerimientos No Funcionales (RNF)

### **RNF01 — Límite de Evaluaciones**

Máximo **10** evaluaciones por estudiante.

### **RNF02 — Concurrencia**

Soporte para **50 usuarios concurrentes** solicitando cálculos.

### **RNF03 — Determinismo**

Mismos datos → misma nota final.

### **RNF04 — Performance**

Tiempo de cálculo menor a **300 ms** por solicitud.

---

## ✅ Caso de Uso: CU001 — Calcular Nota Final

**Sistema:** `CS-GradeCalculator`  
**Actor:** Docente UTEC

### Flujo Principal

1. El docente ingresa a la aplicación.
2. La aplicación solicita el código e identificador del estudiante.
3. El docente registra o revisa evaluaciones con notas y pesos.
4. El docente indica si el estudiante cumplió asistencia mínima.
5. La aplicación consulta `allYearsTeachers`.
6. La aplicación calcula la nota final.
7. La aplicación muestra:
   - Nota final
   - Detalle del cálculo

---

# Página 3 de 4 — Criterios de Evaluación (11 pts)

## ✅ 1. Cumplimiento RF / RNF — 2 pts

- Implementación correcta de RF01–RF05.
- Cumplimiento de RNF01–RNF03.
- Sin datos hardcodeados fuera de clases.
- Entradas y salidas definidas.

---

## ✅ 2. Diseño y Arquitectura OO — 2 pts

- Separación clara de responsabilidades.
- Uso adecuado de clases como:
  - `Evaluation`
  - `GradeCalculator`
  - `AttendancePolicy`
  - `ExtraPointsPolicy`
- Bajo acoplamiento / alta cohesión.
- UML simple y coherente con el código.

---

## ✅ 3. Calidad del Código — 2 pts

Evaluación basada en:

- Nombres claros.
- Sin valores mágicos.
- Manejo de errores/validaciones.
- Comentarios relevantes.
- Formato consistente y legibilidad.

> Evaluado con **SonarQube**.

---

## ✅ 4. Pruebas Automatizadas — 2 pts

Se evaluará que existan tests unitarios para:

- Cálculo normal.
- Caso sin asistencia mínima.
- Caso con/sin puntos extra.
- Casos borde:
  - 0 evaluaciones
  - Pesos inválidos
  - Asistencia negativa
- Nombres claros en tests (`shouldReturnXWhenY`)
- Cobertura mínima:
  - ≥ 50% aceptable
  - ≥ 60% excelente

---

## ✅ Checklist de Implementación

### Desarrollo

- [ ] RF01 Registro de evaluaciones
- [ ] RF02 Asistencia mínima
- [ ] RF03 Política puntos extra
- [ ] RF04 Cálculo nota final
- [ ] RF05 Detalle del cálculo

### No Funcionales

- [ ] ≤ 10 evaluaciones por estudiante
- [ ] Determinismo garantizado
- [ ] Tiempo < 300 ms
- [ ] Escalabilidad para 50 usuarios concurrentes

### Arquitectura

- [ ] Clases separadas y coherentes
- [ ] Bajo acoplamiento / alta cohesión
- [ ] UML generado

### Pruebas

- [ ] Test cálculo normal
- [ ] Test sin asistencia mínima
- [ ] Test con/sin puntos extra
- [ ] Test casos borde
- [ ] ≥ 50% coverage
