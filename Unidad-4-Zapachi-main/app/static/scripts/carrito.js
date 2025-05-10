document.addEventListener("DOMContentLoaded", function() {
    cargarCarrito();
    
    // Manejar cambios en el carrito
    document.addEventListener("click", function(e) {
        if (e.target.classList.contains("cambiar-cantidad")) {
            const productoId = e.target.dataset.productoId;
            const accion = e.target.dataset.accion;
            actualizarItemCarrito(productoId, accion);
        }
        
        if (e.target.classList.contains("eliminar-item")) {
            const productoId = e.target.dataset.productoId;
            eliminarItemCarrito(productoId);
        }
    });
    
    // Vaciar carrito
    document.getElementById("vaciar-carrito").addEventListener("click", vaciarCarrito);
    
    // Finalizar compra
    document.getElementById("finalizar-compra").addEventListener("click", finalizarCompra);
});

async function cargarCarrito() {
    try {
        const respuesta = await fetch('/api/carrito');
        const datos = await respuesta.json();
        renderizarCarrito(datos.productos, datos.total);
    } catch (error) {
        console.error("Error al cargar el carrito:", error);
    }
}

async function actualizarItemCarrito(productoId, accion) {
    try {
        const respuesta = await fetch('/api/carrito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                producto_id: productoId,
                cantidad: accion === 'aumentar' ? 1 : -1
            })
        });
        
        const datos = await respuesta.json();
        if (datos.exito) {
            cargarCarrito();
        }
    } catch (error) {
        console.error("Error al actualizar el carrito:", error);
    }
}

async function eliminarItemCarrito(productoId) {
    try {
        const respuesta = await fetch('/api/carrito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                producto_id: productoId,
                cantidad: 0  // Cantidad 0 para eliminar
            })
        });
        
        const datos = await respuesta.json();
        if (datos.exito) {
            cargarCarrito();
        }
    } catch (error) {
        console.error("Error al eliminar del carrito:", error);
    }
}

async function vaciarCarrito() {
    if (confirm("¿Estás seguro de que quieres vaciar el carrito?")) {
        try {
            const respuesta = await fetch('/api/carrito/vaciar', {
                method: 'POST'
            });
            
            const datos = await respuesta.json();
            if (datos.exito) {
                cargarCarrito();
            }
        } catch (error) {
            console.error("Error al vaciar el carrito:", error);
        }
    }
}

async function finalizarCompra() {
    try {
        const respuesta = await fetch('/api/finalizar-compra', {
            method: 'POST'
        });
        
        const datos = await respuesta.json();
        if (datos.exito) {
            alert("¡Compra realizada con éxito! Número de pedido: " + datos.pedido_id);
            cargarCarrito();
        } else {
            alert("Error al procesar la compra: " + datos.mensaje);
        }
    } catch (error) {
        console.error("Error al finalizar compra:", error);
        alert("Ocurrió un error al procesar tu compra");
    }
}

function renderizarCarrito(productos, total) {
    const cuerpoCarrito = document.getElementById("cuerpo-carrito");
    const precioTotal = document.getElementById("precio-total");
    
    cuerpoCarrito.innerHTML = "";
    
    if (productos.length === 0) {
        cuerpoCarrito.innerHTML = `<tr><td colspan="6" class="text-center">Tu carrito está vacío</td></tr>`;
        precioTotal.textContent = "0";
        return;
    }
    
    productos.forEach(producto => {
        cuerpoCarrito.innerHTML += `
            <tr>
                <td>
                    <img src="${producto.url_imagen}" alt="${producto.nombre}" style="width: 50px;">
                    ${producto.nombre}
                </td>
                <td>${producto.talla || 'N/A'}</td>
                <td>$${producto.precio.toFixed(2)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary cambiar-cantidad" 
                            data-producto-id="${producto.id}" 
                            data-accion="disminuir">−</button>
                    <span class="mx-2">${producto.cantidad}</span>
                    <button class="btn btn-sm btn-outline-primary cambiar-cantidad" 
                            data-producto-id="${producto.id}" 
                            data-accion="aumentar">+</button>
                </td>
                <td>$${producto.total_item.toFixed(2)}</td>
                <td>
                    <button class="btn btn-sm btn-danger eliminar-item" 
                            data-producto-id="${producto.id}">🗑</button>
                </td>
            </tr>
        `;
    });
    
    precioTotal.textContent = total.toFixed(2);
}