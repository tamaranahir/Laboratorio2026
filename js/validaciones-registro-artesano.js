// TERCER AVANCE
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("form-registro-artesano");
    const selectProvincia = document.getElementById("provincia");
    const selectDepartamento = document.getElementById("departamento");

    //  1. FUNCIONALIDAD: SELECTS EN CASCADA (PROVINCIA -> DEPARTAMENTO)
    const departamentosPorProvincia = {
        "catamarca": ["Capital", "Belén", "Tinogasta", "Santa María", "Andalgalá", "Valle Viejo", "Fray Mamerto Esquiú", "Pomán", "Santa Rosa", "Ambato", "Ancasti", "Antofagasta de la Sierra", "Capayán", "El Alto", "La Paz", "Paclín"],
        "tucuman": ["Capital", "Tafí del Valle", "Yerba Buena", "Monteros", "Chicligasta", "Famaillá", "Cruz Alta", "Lules", "Tafí Viejo"],
        "santiago": ["Capital", "Banda", "Río Hondo", "Robles", "Choya", "Guasayán", "Avellaneda", "General Taboada"],
        "cordoba": ["Capital", "Colón", "Punilla", "Río Cuarto", "San Justo", "Calamuchita", "Santa María", "Cruz del Eje"],
        "salta": ["Capital", "Cafayate", "Cachi", "Orán", "Rosario de la Frontera", "Metán", "San Carlos", "La Caldera"]
    };

    if (selectProvincia && selectDepartamento) {
        selectProvincia.addEventListener("change", function () {
            const provinciaSeleccionada = this.value;

            // Limpiamos las opciones previas del departamento
            selectDepartamento.innerHTML = "";

            if (provinciaSeleccionada === "") {
                const opcionDefecto = document.createElement("option");
                opcionDefecto.value = "";
                opcionDefecto.textContent = "-- Seleccione primero una provincia --";
                selectDepartamento.appendChild(opcionDefecto);
                selectDepartamento.disabled = true;
                return;
            }

            selectDepartamento.disabled = false;

            const opcionInicial = document.createElement("option");
            opcionInicial.value = "";
            opcionInicial.textContent = "-- Seleccione un departamento --";
            selectDepartamento.appendChild(opcionInicial);

            const departamentos = departamentosPorProvincia[provinciaSeleccionada];
            departamentos.forEach(depto => {
                const option = document.createElement("option");
                option.value = depto.toLowerCase().replace(/\s+/g, '-');
                option.textContent = depto;
                selectDepartamento.appendChild(option);
            });
        });
    }

    // 2. VALIDACIONES PARA ENVIAR EL FOMRULARIO
    if (form) {
        form.addEventListener("submit", (event) => {
            let esValido = true;
            let errores = [];

            // A. Validación: Apellido y Nombre
            const nombre = document.getElementById("nombre_completo");
            if (nombre) {
                if (nombre.value.trim() === "") {
                    esValido = false;
                    errores.push("Debe ingresar su Apellido y Nombre.");
                    nombre.classList.add("is-invalid");
                } else {
                    nombre.classList.remove("is-invalid");
                }
            }

            // B. Validación: DNI (Exactamente 8 dígitos numéricos)
            const dni = document.getElementById("dni");
            if (dni) {
                const valorDni = dni.value.trim();
                const regexDni = /^\d{8}$/;
                if (!regexDni.test(valorDni)) {
                    esValido = false;
                    errores.push("El DNI debe contener exactamente 8 números sin puntos ni espacios.");
                    dni.classList.add("is-invalid");
                } else {
                    dni.classList.remove("is-invalid");
                }
            }

            // C. Validación: Fecha de nacimiento (Mayoría de edad: 18 años)
            const fechaNac = document.getElementById("fecha_nacimiento");
            if (fechaNac) {
                const valorFecha = fechaNac.value;
                if (!valorFecha) {
                    esValido = false;
                    errores.push("Debe completar su fecha de nacimiento.");
                    fechaNac.classList.add("is-invalid");
                } else {
                    const hoy = new Date();
                    hoy.setHours(0, 0, 0, 0);
                    const fechaIngresada = new Date(valorFecha + "T00:00:00");

                    if (fechaIngresada > hoy) {
                        esValido = false;
                        errores.push("La fecha de nacimiento no puede ser posterior al día de hoy.");
                        fechaNac.classList.add("is-invalid");
                    } else {
                        let edad = hoy.getFullYear() - fechaIngresada.getFullYear();
                        const mesDiff = hoy.getMonth() - fechaIngresada.getMonth();
                        if (mesDiff < 0 || (mesDiff === 0 && hoy.getDate() < fechaIngresada.getDate())) {
                            edad--;
                        }

                        if (edad < 18) {
                            esValido = false;
                            errores.push("Debe ser mayor de 18 años para postularse en Poncho Digital.");
                            fechaNac.classList.add("is-invalid");
                        } else {
                            fechaNac.classList.remove("is-invalid");
                        }
                    }
                }
            }

            // D. Validación: Teléfono (Exactamente 10 dígitos numéricos)
            const tel = document.getElementById("telefono");
            if (tel) {
                const valorTel = tel.value.trim();
                const regexTel = /^\d{10}$/;
                if (!regexTel.test(valorTel)) {
                    esValido = false;
                    errores.push("El teléfono debe contener exactamente 10 números (Ej: 3834123456).");
                    tel.classList.add("is-invalid");
                } else {
                    tel.classList.remove("is-invalid");
                }
            }

            // E. Validación: Correo Electrónico
            const correo = document.getElementById("correo_electronico");
            if (correo) {
                const valorCorreo = correo.value.trim();
                const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!regexCorreo.test(valorCorreo)) {
                    esValido = false;
                    errores.push("Por favor, ingrese un correo electrónico válido.");
                    correo.classList.add("is-invalid");
                } else {
                    correo.classList.remove("is-invalid");
                }
            }

            // F. NUEVO: Validación de Selección de Sexo (Radio Buttons)
            const sexos = document.getElementsByName("sexo");
            let sexoSeleccionado = false;
            sexos.forEach(radio => {
                if (radio.checked) {
                    sexoSeleccionado = true;
                }
            });

            if (!sexoSeleccionado) {
                esValido = false;
                errores.push("Debe seleccionar una opción para el Sexo.");
                sexos.forEach(radio => radio.classList.add("is-invalid"));
            } else {
                sexos.forEach(radio => radio.classList.remove("is-invalid"));
            }

            // G. Validación: Selección de Provincia
            if (selectProvincia) {
                if (selectProvincia.value === "") {
                    esValido = false;
                    errores.push("Debe seleccionar una Provincia de origen.");
                    selectProvincia.classList.add("is-invalid");
                } else {
                    selectProvincia.classList.remove("is-invalid");
                }
            }

            // H. Validación: Selección de Departamento
            if (selectDepartamento) {
                if (selectDepartamento.value === "") {
                    esValido = false;
                    errores.push("Debe seleccionar su Departamento o Jurisdicción.");
                    selectDepartamento.classList.add("is-invalid");
                } else {
                    selectDepartamento.classList.remove("is-invalid");
                }
            }

            // I. NUEVO: Validación de Nombre del Emprendimiento o Marca
            const nombreMarca = document.getElementById("nombre_marca");
            if (nombreMarca) {
                if (nombreMarca.value.trim() === "") {
                    esValido = false;
                    errores.push("Debe ingresar el Nombre de su Emprendimiento o Marca.");
                    nombreMarca.classList.add("is-invalid");
                } else {
                    nombreMarca.classList.remove("is-invalid");
                }
            }

            // J. Validación: Selección de Rubro o Especialidad
            const rubro = document.getElementById("rubro");
            if (rubro) {
                if (rubro.value === "") {
                    esValido = false;
                    errores.push("Debe seleccionar un Rubro o Especialidad.");
                    rubro.classList.add("is-invalid");
                } else {
                    rubro.classList.remove("is-invalid");
                }
            }

            // K. NUEVO: Validación de Descripción de Técnicas (Con longitud mínima)
            const descripcionTecnicas = document.getElementById("descripcion_tecnicas");
            if (descripcionTecnicas) {
                if (descripcionTecnicas.value.trim() === "") {
                    esValido = false;
                    errores.push("Debe ingresar una descripción de las técnicas y materias primas.");
                    descripcionTecnicas.classList.add("is-invalid");
                } else if (descripcionTecnicas.value.trim().length < 15) {
                    esValido = false;
                    errores.push("La descripción técnica debe ser más detallada (mínimo 15 caracteres).");
                    descripcionTecnicas.classList.add("is-invalid");
                } else {
                    descripcionTecnicas.classList.remove("is-invalid");
                }
            }

            // L. Validación: Carga obligatoria de foto del producto
            const fotoProducto = document.getElementById("foto_producto");
            if (fotoProducto) {
                if (fotoProducto.files.length === 0) {
                    esValido = false;
                    errores.push("Debe cargar al menos una fotografía de exhibición de sus productos.");
                    fotoProducto.classList.add("is-invalid");
                } else {
                    fotoProducto.classList.remove("is-invalid");
                }
            }

            // M. Validación: Declaración Jurada obligatoria
            const declaracion = document.getElementById("declaracion");
            if (declaracion && !declaracion.checked) {
                esValido = false;
                errores.push("Debe aceptar bajo juramento que los productos son artesanales.");
                declaracion.classList.add("is-invalid");
            } else if (declaracion) {
                declaracion.classList.remove("is-invalid");
            }

            // VALIDACIÓN FINAL DE ERRORES ACUMULADOS (O EXITO)
            if (!esValido) {
                event.preventDefault(); // Frena el envío
                alert("Por favor, corrija los siguientes errores antes de continuar:\n\n- " + errores.join("\n- "));
            } else {
                alert("¡Formulario de postulación validado correctamente! Enviando su solicitud...");
            }
        });
    }
});