
document.addEventListener("DOMContentLoaded", () => {

    const formProducto = document.getElementById("form-publicar-producto");
    const inputFoto = document.getElementById("foto_producto");


if (formProducto) {
        formProducto.addEventListener("submit", (event) => {
            let esValido = true;
            let errores = [];

            // 1. Validación: Nombre de la Artesanía
            const nombreProd = document.getElementById("nombre_producto");
            if (nombreProd) {
                const valorNombre = nombreProd.value.trim();
                if (valorNombre === "") {
                    esValido = false;
                    errores.push("Debe ingresar el Nombre de la Artesanía.");
                    nombreProd.classList.add("is-invalid");
                } else if (valorNombre.length < 3) {
                    esValido = false;
                    errores.push("El nombre de la artesanía debe tener al menos 3 caracteres.");
                    nombreProd.classList.add("is-invalid");
                } else {
                    nombreProd.classList.remove("is-invalid");
                }
            }

            // 2. Validación: Precio de Venta
            const precio = document.getElementById("precio");
            if (precio) {
                const valorPrecio = parseFloat(precio.value);
                if (isNaN(valorPrecio) || valorPrecio <= 0) {
                    esValido = false;
                    errores.push("Debe ingresar un Precio de venta válido y mayor a $0.");
                    precio.classList.add("is-invalid");
                } else {
                    precio.classList.remove("is-invalid");
                }
            }

            // 3. Validación: Cantidad de Stock Inicial
            const stock = document.getElementById("stock");
            if (stock) {
                const valorStock = parseInt(stock.value, 10);
                if (isNaN(valorStock) || valorStock < 1) {
                    esValido = false;
                    errores.push("El Stock inicial debe ser de al menos 1 unidad.");
                    stock.classList.add("is-invalid");
                } else {
                    stock.classList.remove("is-invalid");
                }
            }

            // 4. Validación: Descripción de las Técnicas y Materiales
            const descripcion = document.getElementById("descripcion");
            if (descripcion) {
                const valorDesc = descripcion.value.trim();
                if (valorDesc === "") {
                    esValido = false;
                    errores.push("Debe ingresar la descripción técnica y materiales de la artesanía.");
                    descripcion.classList.add("is-invalid");
                } else if (valorDesc.length < 15) {
                    esValido = false;
                    errores.push("La descripción del producto debe ser más detallada (mínimo 15 caracteres).");
                    descripcion.classList.add("is-invalid");
                } else {
                    descripcion.classList.remove("is-invalid");
                }
            }

            // 5. Validación: Fotografía del Producto
            const fotoProd = document.getElementById("foto_producto");
            if (fotoProd) {
                if (fotoProd.files.length === 0) {
                    esValido = false;
                    errores.push("Debe cargar al menos una fotografía de exhibición para el producto.");
                    fotoProd.classList.add("is-invalid");
                } else {
                    fotoProd.classList.remove("is-invalid");
                }
            }

            // VALIDACIÓN FINAL DE ERRORES ACUMULADOS (O EXITO)
            if (!esValido) {
                event.preventDefault(); // Frena el envío
                alert("Por favor, corrija los siguientes errores antes de publicar el producto:\n\n- " + errores.join("\n- "));
            } else {
                alert("¡Artesanía validada correctamente! Guardando y publicando en el catálogo virtual...");
            }
        });
    }

    //FUNCIONALIDAD: Vista Previa
    // Creamos el contenedor principal para las vistas previas dinámicamente debajo del input de foto
    const contenedorPreview = document.createElement("div");
    contenedorPreview.id = "vistaPreviaFoto";
    contenedorPreview.className = "mt-3 d-none"; // Oculto inicialmente
    inputFoto.parentNode.appendChild(contenedorPreview);

    inputFoto.addEventListener("change", function () {
        const archivos = inputFoto.files;

        // Si no se seleccionó ningún archivo, limpiamos y ocultamos el contenedor
        if (archivos.length === 0) {
            contenedorPreview.innerHTML = "";
            contenedorPreview.classList.add("d-none");
            return;
        }

        contenedorPreview.innerHTML = ""; // Limpiamos vistas previas anteriores
        contenedorPreview.classList.remove("d-none"); // Mostramos el contenedor

        const parrafoTitulo = document.createElement("p");
        parrafoTitulo.className = "small text-muted mb-2 text-center";
        parrafoTitulo.appendChild(document.createTextNode("Vista previa de las piezas seleccionadas:"));
        contenedorPreview.appendChild(parrafoTitulo);

        // Contenedor flexible para alinear las imágenes horizontalmente en lote
        const divFlex = document.createElement("div");
        divFlex.className = "d-flex flex-wrap justify-content-center gap-2";
        contenedorPreview.appendChild(divFlex);

        // Recorremos el FileList transformándolo en array para verificar cada imagen
        Array.from(archivos).forEach((archivo) => {
            // Validamos que sea estrictamente un formato de imagen
            if (!archivo.type.startsWith("image/")) {
                alert("Por favor, seleccione únicamente archivos de imagen válidos (.png, .jpg, .webp).");
                inputFoto.value = ""; // Reseteamos el input
                contenedorPreview.innerHTML = "";
                contenedorPreview.classList.add("d-none");
                return;
            }

            const lector = new FileReader();

            lector.onload = function (evento) {
                const img = document.createElement("img");
                img.src = evento.target.result;
                img.alt = "Vista previa del producto";
                img.className = "img-fluid rounded shadow-sm";
                img.style.maxHeight = "130px";
                img.style.border = "2px solid #ebdcb9";
                img.style.borderRadius = "6px";
                img.style.objectFit = "cover";

                divFlex.appendChild(img);
            };


            lector.readAsDataURL(archivo);
        });
    });
});


