// core/static/core/js/simulador.js

document.addEventListener('DOMContentLoaded', function () {
    // Variables globales
    let topologias = [];
    let resultadosActuales = null;

    // Elementos del DOM
    const formSimulador = document.getElementById('form-simulador');
    const topologiaSelect = document.getElementById('id_topologia');
    const topologiaInfo = document.getElementById('topologia-info');
    const calcularBtn = document.getElementById('calcular-btn');
    const resultadosDiv = document.getElementById('resultados-simulacion');
    const loadingDiv = document.getElementById('loading');

    // Cargar topologías desde JSON
    cargarTopologias();

    // Event Listeners
    if (topologiaSelect) {
        topologiaSelect.addEventListener('change', mostrarInfoTopologia);
    }

    if (formSimulador) {
        formSimulador.addEventListener('submit', simularRed);
    }

    // Inputs numéricos - Validación en tiempo real
    const inputsNumericos = document.querySelectorAll('input[type="number"]');
    inputsNumericos.forEach(input => {
        input.addEventListener('input', validarInput);
        input.addEventListener('blur', calcularEstimacionTiempo);
    });

    /**
     * Cargar topologías desde el archivo JSON
     */
    function cargarTopologias() {
        fetch('/static/core/data/topologias.json')
            .then(response => response.json())
            .then(data => {
                topologias = data.topologias;
                llenarSelectTopologias();
            })
            .catch(error => {
                console.error('Error al cargar topologías:', error);
                mostrarNotificacion('Error al cargar topologías', 'error');
            });
    }

    /**
     * Llenar el select de topologías
     */
    function llenarSelectTopologias() {
        if (!topologiaSelect) return;

        // Limpiar opciones existentes (excepto la primera)
        while (topologiaSelect.options.length > 1) {
            topologiaSelect.remove(1);
        }

        // Agregar opciones desde JSON
        topologias.forEach(topo => {
            const option = document.createElement('option');
            option.value = topo.id;
            option.textContent = topo.nombre;
            topologiaSelect.appendChild(option);
        });
    }

    /**
     * Mostrar información de la topología seleccionada
     */
    function mostrarInfoTopologia() {
        const topologiaId = parseInt(topologiaSelect.value);
        const topologia = topologias.find(t => t.id === topologiaId);

        if (!topologia || !topologiaInfo) return;

        topologiaInfo.innerHTML = `
            <div class="topologia-detalle">
                <h4>${topologia.nombre}</h4>
                <p class="descripcion">${topologia.descripcion}</p>
                
                <div class="ventajas-desventajas">
                    <div class="ventajas">
                        <h5>✅ Ventajas:</h5>
                        <ul>
                            ${topologia.ventajas.map(v => `<li>${v}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="desventajas">
                        <h5>❌ Desventajas:</h5>
                        <ul>
                            ${topologia.desventajas.map(d => `<li>${d}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;

        topologiaInfo.style.display = 'block';
        topologiaInfo.classList.add('fade-in');
    }

    /**
     * Validar inputs numéricos en tiempo real
     */
    function validarInput(e) {
        const input = e.target;
        const valor = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);

        // Remover clase de error
        input.classList.remove('input-error');

        // Validar rango
        if (valor < min || valor > max) {
            input.classList.add('input-error');
            mostrarTooltipError(input, `Valor debe estar entre ${min} y ${max}`);
        } else {
            ocultarTooltipError(input);
        }

        // Validar que sea un número
        if (isNaN(valor)) {
            input.classList.add('input-error');
            mostrarTooltipError(input, 'Ingrese un número válido');
        }
    }

    /**
     * Calcular estimación de tiempo de implementación
     */
    function calcularEstimacionTiempo() {
        const numDispositivos = parseInt(document.getElementById('id_num_dispositivos')?.value) || 0;
        const topologiaId = parseInt(topologiaSelect?.value) || 0;

        if (numDispositivos > 0 && topologiaId > 0) {
            // Fórmula simple de estimación
            let tiempoBase = numDispositivos * 2; // 2 horas por dispositivo

            // Ajustar según topología
            const factoresTopologia = {
                1: 1.0,    // Estrella - más fácil
                2: 1.2,    // Anillo
                3: 1.5,    // Malla - más compleja
                4: 0.9     // Bus - más simple
            };

            const tiempoEstimado = tiempoBase * (factoresTopologia[topologiaId] || 1.0);

            mostrarEstimacionTiempo(tiempoEstimado);
        }
    }

    /**
     * Mostrar estimación de tiempo
     */
    function mostrarEstimacionTiempo(horas) {
        const estimacionDiv = document.getElementById('estimacion-tiempo');
        if (!estimacionDiv) return;

        const dias = Math.ceil(horas / 8); // 8 horas laborales por día

        estimacionDiv.innerHTML = `
            <div class="estimacion-card">
                <i class="fas fa-clock"></i>
                <div>
                    <strong>Tiempo estimado:</strong>
                    <p>${horas.toFixed(1)} horas (aprox. ${dias} día${dias > 1 ? 's' : ''})</p>
                </div>
            </div>
        `;
        estimacionDiv.style.display = 'block';
    }

    /**
     * Simular red (enviar formulario)
     */
    function simularRed(e) {
        e.preventDefault();

        // Validar formulario
        if (!validarFormulario()) {
            mostrarNotificacion('Por favor complete todos los campos correctamente', 'error');
            return;
        }

        // Mostrar loading
        mostrarLoading(true);
        resultadosDiv.style.display = 'none';

        // Obtener datos del formulario
        const formData = new FormData(formSimulador);

        // Enviar simulación al backend
        fetch(formSimulador.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultadosActuales = data.resultados;
                    mostrarResultados(data.resultados);
                    mostrarNotificacion('Simulación completada exitosamente', 'success');
                } else {
                    mostrarNotificacion(data.error || 'Error en la simulación', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                mostrarNotificacion('Error al procesar la simulación', 'error');
            })
            .finally(() => {
                mostrarLoading(false);
            });
    }

    /**
     * Validar formulario completo
     */
    function validarFormulario() {
        let valido = true;

        // Validar topología
        if (!topologiaSelect.value || topologiaSelect.value === '') {
            topologiaSelect.classList.add('input-error');
            valido = false;
        }

        // Validar inputs numéricos
        inputsNumericos.forEach(input => {
            const valor = parseFloat(input.value);
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);

            if (isNaN(valor) || valor < min || valor > max) {
                input.classList.add('input-error');
                valido = false;
            }
        });

        return valido;
    }

    /**
     * Mostrar resultados de la simulación
     */
    function mostrarResultados(resultados) {
        if (!resultadosDiv) return;

        resultadosDiv.innerHTML = `
            <div class="resultados-container">
                <h3>📊 Resultados de la Simulación</h3>
                
                <div class="metricas-grid">
                    <div class="metrica-card">
                        <i class="fas fa-tachometer-alt"></i>
                        <div class="metrica-contenido">
                            <span class="metrica-label">Latencia Promedio</span>
                            <span class="metrica-valor">${resultados.latencia_promedio} ms</span>
                        </div>
                    </div>
                    
                    <div class="metrica-card">
                        <i class="fas fa-signal"></i>
                        <div class="metrica-contenido">
                            <span class="metrica-label">Throughput</span>
                            <span class="metrica-valor">${resultados.throughput} Mbps</span>
                        </div>
                    </div>
                    
                    <div class="metrica-card">
                        <i class="fas fa-exclamation-triangle"></i>
                        <div class="metrica-contenido">
                            <span class="metrica-label">Pérdida de Paquetes</span>
                            <span class="metrica-valor">${resultados.perdida_paquetes}%</span>
                        </div>
                    </div>
                    
                    <div class="metrica-card ${resultados.eficiencia >= 80 ? 'success' : 'warning'}">
                        <i class="fas fa-chart-line"></i>
                        <div class="metrica-contenido">
                            <span class="metrica-label">Eficiencia</span>
                            <span class="metrica-valor">${resultados.eficiencia}%</span>
                        </div>
                    </div>
                </div>

                ${resultados.recomendaciones ? `
                <div class="recomendaciones-ia">
                    <h4>🤖 Recomendaciones de IA</h4>
                    <div class="recomendacion-texto">
                        ${resultados.recomendaciones}
                    </div>
                </div>
                ` : ''}

                <div class="acciones-resultados">
                    <button onclick="descargarPDF()" class="btn btn-pdf">
                        <i class="fas fa-file-pdf"></i> Descargar PDF
                    </button>
                    <button onclick="verGraficos()" class="btn btn-graficos">
                        <i class="fas fa-chart-bar"></i> Ver Gráficos
                    </button>
                    <button onclick="guardarSimulacion()" class="btn btn-guardar">
                        <i class="fas fa-save"></i> Guardar Simulación
                    </button>
                </div>
            </div>
        `;

        resultadosDiv.style.display = 'block';
        resultadosDiv.classList.add('fade-in');
        resultadosDiv.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Mostrar/ocultar loading
     */
    function mostrarLoading(mostrar) {
        if (!loadingDiv) return;
        loadingDiv.style.display = mostrar ? 'flex' : 'none';
    }

    /**
     * Mostrar notificación
     */
    function mostrarNotificacion(mensaje, tipo = 'info') {
        const notificacion = document.createElement('div');
        notificacion.className = `notificacion notificacion-${tipo}`;
        notificacion.innerHTML = `
            <i class="fas fa-${tipo === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${mensaje}</span>
        `;

        document.body.appendChild(notificacion);

        setTimeout(() => {
            notificacion.classList.add('show');
        }, 100);

        setTimeout(() => {
            notificacion.classList.remove('show');
            setTimeout(() => notificacion.remove(), 300);
        }, 3000);
    }

    /**
     * Mostrar tooltip de error
     */
    function mostrarTooltipError(input, mensaje) {
        let tooltip = input.nextElementSibling;

        if (!tooltip || !tooltip.classList.contains('tooltip-error')) {
            tooltip = document.createElement('div');
            tooltip.className = 'tooltip-error';
            input.parentNode.insertBefore(tooltip, input.nextSibling);
        }

        tooltip.textContent = mensaje;
        tooltip.style.display = 'block';
    }

    /**
     * Ocultar tooltip de error
     */
    function ocultarTooltipError(input) {
        const tooltip = input.nextElementSibling;
        if (tooltip && tooltip.classList.contains('tooltip-error')) {
            tooltip.style.display = 'none';
        }
    }

    /**
     * Obtener cookie CSRF
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Funciones globales para botones
    window.descargarPDF = function () {
        if (resultadosActuales) {
            window.location.href = `/simulador/pdf/${resultadosActuales.id}/`;
        }
    };

    window.verGraficos = function () {
        if (resultadosActuales) {
            window.location.href = `/simulador/resultado/${resultadosActuales.id}/`;
        }
    };

    window.guardarSimulacion = function () {
        mostrarNotificacion('Simulación guardada exitosamente', 'success');
    };
});