import WaveSurfer from "https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js";

import RegionsPlugin from "https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/regions.esm.js";


// ======================================================
// ELEMENTOS DEL HTML
// ======================================================

const contenedor = document.querySelector("#waveform");

const botonPlay = document.querySelector("#playPause");

const botonSeleccion = document.querySelector(
    "#playSelection"
);

const textoInicio = document.querySelector(
    "#tiempoInicio"
);

const textoFin = document.querySelector(
    "#tiempoFin"
);

const textoDuracion = document.querySelector(
    "#duracionSeleccion"
);

const inputInicio = document.querySelector(
    "#inicioRecorte"
);

const inputFin = document.querySelector(
    "#finRecorte"
);

const formularioRecorte = document.querySelector(
    "#formRecorte"
);


// ======================================================
// CREAR WAVESURFER
// ======================================================

if (
    contenedor &&
    botonPlay &&
    botonSeleccion &&
    textoInicio &&
    textoFin &&
    textoDuracion
) {

    const regions = RegionsPlugin.create();

    const wavesurfer = WaveSurfer.create({

        container: "#waveform",

        // Evita cargar un source.mp3 anterior desde caché.
        url: `/audio/source?v=${Date.now()}`,

        waveColor: "#94a3b8",

        progressColor: "#f97316",

        cursorColor: "#0f172a",

        height: 120,

        barGap: 2,

        barWidth: 2,

        barRadius: 2,

        normalize: true,

        dragToSeek: false,

        plugins: [
            regions
        ]
    });


    let regionSeleccion = null;


    // ==================================================
    // FORMATEAR SEGUNDOS COMO MM:SS
    // ==================================================

    function formatearTiempo(segundos) {

        segundos = Math.max(
            0,
            Math.floor(segundos)
        );

        const minutos = Math.floor(
            segundos / 60
        );

        const segundosRestantes =
            segundos % 60;

        return (
            String(minutos).padStart(2, "0")
            +
            ":"
            +
            String(segundosRestantes).padStart(2, "0")
        );
    }


    // ==================================================
    // ACTUALIZAR LA SELECCIÓN
    // ==================================================

    function actualizarSeleccion(region) {

        if (!region) {

            return;
        }

        const inicio = region.start;

        const fin = region.end;

        const duracion = fin - inicio;


        // Valores visibles.

        textoInicio.textContent =
            formatearTiempo(inicio);

        textoFin.textContent =
            formatearTiempo(fin);

        textoDuracion.textContent =
            formatearTiempo(duracion);


        // Valores ocultos enviados a Flask.

        if (inputInicio && inputFin) {

            inputInicio.value =
                inicio.toFixed(3);

            inputFin.value =
                fin.toFixed(3);
        }


        console.log(
            "Inicio seleccionado:",
            inicio.toFixed(3)
        );

        console.log(
            "Fin seleccionado:",
            fin.toFixed(3)
        );
    }


    // ==================================================
    // AUDIO CARGADO
    // ==================================================

    wavesurfer.on(
        "ready",
        function (duracion) {

            console.log(
                "Audio cargado correctamente"
            );

            console.log(
                "Duración:",
                duracion,
                "segundos"
            );


            // Una sola región que inicialmente
            // cubre toda la canción.

            regionSeleccion = regions.addRegion({

                start: 0,

                end: duracion,

                color: "rgba(249, 115, 22, 0.22)",

                drag: true,

                resize: true
            });


            actualizarSeleccion(
                regionSeleccion
            );
        }
    );


    // ==================================================
    // MOVIMIENTO DE LA REGIÓN
    // ==================================================

    regions.on(
        "region-update",
        function (region) {

            regionSeleccion = region;

            actualizarSeleccion(
                regionSeleccion
            );
        }
    );


    regions.on(
        "region-updated",
        function (region) {

            regionSeleccion = region;

            actualizarSeleccion(
                regionSeleccion
            );
        }
    );


    // ==================================================
    // AUDIO COMPLETO
    // ==================================================

    botonPlay.addEventListener(
        "click",
        function () {

            wavesurfer.playPause();

        }
    );


    // ==================================================
    // AUDIO SELECCIONADO
    // ==================================================

    botonSeleccion.addEventListener(
        "click",
        function () {

            if (!regionSeleccion) {

                return;
            }

            regionSeleccion.play();

        }
    );


    wavesurfer.on(
        "play",
        function () {

            botonPlay.textContent =
                "⏸ Pausar";

        }
    );


    wavesurfer.on(
        "pause",
        function () {

            botonPlay.textContent =
                "▶ Reproducir";

        }
    );


    wavesurfer.on(
        "finish",
        function () {

            botonPlay.textContent =
                "▶ Reproducir";

        }
    );


    regions.on(
        "region-out",
        function (region) {

            if (
                regionSeleccion &&
                region.id === regionSeleccion.id
            ) {

                wavesurfer.pause();

                botonPlay.textContent =
                    "▶ Reproducir";
            }
        }
    );


// ==================================================
// ENVIAR RECORTE A FLASK SIN RECARGAR LA PÁGINA
// ==================================================

const resultadoRecorte = document.querySelector(
    "#resultadoRecorte"
);

const botonRecortar = document.querySelector(
    "#procesarRecorte"
);


if (formularioRecorte) {

    formularioRecorte.addEventListener(
        "submit",
        async function (evento) {

            // Evita que el navegador cambie de página.
            evento.preventDefault();


            if (!regionSeleccion) {

                alert(
                    "Todavía no existe una selección."
                );

                return;
            }


            // Guardar los últimos valores de la región.
            actualizarSeleccion(
                regionSeleccion
            );


            console.log(
                "Inicio enviado:",
                inputInicio.value
            );

            console.log(
                "Fin enviado:",
                inputFin.value
            );


            // Evitar dos clics mientras se procesa.
            if (botonRecortar) {

                botonRecortar.disabled = true;

                botonRecortar.textContent =
                    "Procesando recorte...";
            }


            if (resultadoRecorte) {

                resultadoRecorte.hidden = false;

                resultadoRecorte.className =
                    "resultado-recorte procesando";

                resultadoRecorte.textContent =
                    "Procesando selección...";
            }


            try {

                const datosFormulario = new FormData(
                    formularioRecorte
                );


                const respuesta = await fetch(
                    formularioRecorte.action,
                    {
                        method: "POST",
                        body: datosFormulario
                    }
                );


                const resultado = await respuesta.json();


                if (!respuesta.ok) {

                    throw new Error(
                        resultado.mensaje
                        ||
                        "No se pudo completar el recorte."
                    );
                }


                if (resultadoRecorte) {

                    resultadoRecorte.className =
                        "resultado-recorte correcto";

                    resultadoRecorte.textContent =
                        resultado.mensaje;
                }


                console.log(
                    "Respuesta de Flask:",
                    resultado
                );

            } catch (error) {

                console.error(
                    "Error procesando el recorte:",
                    error
                );


                if (resultadoRecorte) {

                    resultadoRecorte.className =
                        "resultado-recorte error";

                    resultadoRecorte.textContent =
                        error.message;
                }

            } finally {

                if (botonRecortar) {

                    botonRecortar.disabled = false;

                    botonRecortar.textContent =
                        "Recortar y regenerar";
                }
            }
        }
    );
}


    // ==================================================
    // ERRORES
    // ==================================================

    wavesurfer.on(
        "error",
        function (error) {

            console.error(
                "Error cargando el audio:",
                error
            );
        }
    );

}