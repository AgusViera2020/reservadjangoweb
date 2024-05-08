document.addEventListener('DOMContentLoaded', function() {
    // Cambiar contenido al hacer clic en las pestañas
    function cambiarContenido(evento) {
        console.log('Tab clicked:', evento.target); // Log the clicked tab for debugging
        var tabId = evento.target.getAttribute('href'); // Obtener el ID de la pestaña
        var contenido = document.querySelector(tabId); // Obtener el contenido correspondiente

        // Mostrar el contenido de la pestaña actual y ocultar el resto
        document.querySelectorAll('.tab-pane').forEach(function(tab) {
            if (tab.id === tabId.substring(1)) {
                tab.classList.add('show', 'active');
            } else {
                tab.classList.remove('show', 'active');
            }
        });

        document.querySelectorAll('.nav-link').forEach(function(navItem) {
            if (navItem.getAttribute('href') === tabId){
                navItem.classList.add('active');
            } else {
                navItem.classList.remove('active');
            }
        });
    }

    // Agregar evento clic a cada enlace de pestaña
    document.querySelectorAll('.nav-link').forEach(function(enlace) {
        enlace.addEventListener('click', cambiarContenido);
    });

    // Establecer fecha predeterminada y rango de fechas
    var today = new Date();
    var yyyy = today.getFullYear();
    var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
    var dd = String(today.getDate()).padStart(2, '0');
    var todayString = yyyy + '-' + mm + '-' + dd;

    var fechaInput = document.getElementById('fecha');
    var maxDate = new Date(today);
    maxDate.setMonth(maxDate.getMonth() + 1);
    var todayFormatted = today.toISOString().split('T')[0];
    var maxDateFormatted = maxDate.toISOString().split('T')[0];

    var minDate = new Date(today);
    if (minDate.getDay() === 0) { // Si es domingo
        minDate.setDate(minDate.getDate() + 1); // Ajustar al próximo día
    }

    var minDateFormatted = minDate.toISOString().split('T')[0];

    fechaInput.setAttribute('min', minDateFormatted);
    fechaInput.setAttribute('max', maxDateFormatted);
    fechaInput.value = todayString;

    // Validación de campos faltantes en el formulario
    var form = document.getElementById('miFormulario');
    var errorMessage = document.getElementById('error');

    form.addEventListener('submit', function(event) {
        var nombre = document.getElementById('nombre');
        var telefono = document.getElementById('telefono');
        var fecha = document.getElementById('fecha');
        var servicio = document.getElementById('servicio'); 
        var hora = document.getElementById('hora');

        if (nombre.value === '' || telefono.value === '' || fecha.value === '' ||
            servicio.value === '' || hora.value === '') {
            event.preventDefault();
            errorMessage.style.display = 'block';

            // Marcar visualmente los campos no completados
            if (nombre.value === '') {
                nombre.style.border = '1px solid red';
            }
            if (telefono.value === '') {
                telefono.style.border = '1px solid red';
            }
            if (fecha.value === '') {
                fecha.style.border = '1px solid red';
            }
            if (servicio.value === 'Elija un servicio...') {
                servicio.style.border = '1px solid red';
            }
            if (hora.value === 'Elija una hora...') {
                hora.style.border = '1px solid red';
            }
        } else {
            errorMessage.style.display = 'none';
        }
    });

    // Función para procesar la respuesta del servidor
    function handleServerResponse(response) {
        var successMessageDiv = document.getElementById('success_message');
        var errorMessageDiv = document.getElementById('error');
    
        if (response.error_message) {
            errorMessageDiv.innerHTML = '<b>' + response.error_message + '</b>';
            errorMessageDiv.style.display = 'block';
            successMessageDiv.style.display = 'none';
        } else if (response.success_message) {
            successMessageDiv.innerHTML = '<b>' + response.success_message + '</b>';
            successMessageDiv.style.display = 'block';
            errorMessageDiv.style.display = 'none';
        } else {
            // Handle other types of responses if needed
        }
    }

    // Asignar el evento submit al formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault();
    
        var formData = new FormData(form);
        fetch('/reserva/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            handleServerResponse(data);
        })
        .catch(error => {
            console.error('Error al procesar la solicitud:', error);
            errorMessageDiv.innerHTML = '<b>Error al procesar la solicitud.</b>';
            errorMessageDiv.style.display = 'block';
            successMessageDiv.style.display = 'none';
        });
    });

    // Actualizar horas según la fecha seleccionada
$('#fecha').on('change', function() {
    var fechaSeleccionada = $(this).val();

    $.ajax({
        url: '/obtener_horas/',
        type: 'GET',
        data: {'fecha': fechaSeleccionada},
        success: function(data) {
            $('#hora').empty();
            $.each(data.horas_disponibles, function(index, hora) {
                $('#hora').append($('<option>', {
                    value: hora,
                    text: hora
                }));
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al obtener las horas disponibles:', error);
        }
    });
});
});
