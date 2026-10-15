// ======================================================
// IMPORTAR WAVESURFER Y REGIONS
// ======================================================

import WaveSurfer from "https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js";

import RegionsPlugin from "https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/regions.esm.js";


// ======================================================
// ELEMENTOS DEL HTML
// ======================================================

const contenedor = document.querySelector(
    "#waveform"
);

const botonPlay = document.querySelector(
    "#playPause"
);

const botonSeleccion = document.querySelector(
    "#playSelection"
);

const botonRecortar = document.querySelector(
    "#procesarRecorte"
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

const resultadoRecorte = document.querySelector(
    "#resultadoRecorte"
);

const previewRecortado = document.querySelector(
    "#previewRecortado"
);

const audioRecortado = document.querySelector(
    "#audioRecortado"
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

    // Plugin para crear la selección visual.

    const regions = RegionsPlugin.create();


    // WaveSurfer siempre carga source.mp3 original.

    const wavesurfer = WaveSurfer.create({

        container: "#waveform",

        // Date.now() evita usar una versión vieja
        // guardada en caché por el navegador.

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


    // Región que el usuario puede mover
    // y cambiar de tamaño.

    let regionSeleccion = null;


    // Indica si estamos reproduciendo
    // solamente la región seleccionada.

    let reproduciendoSeleccion = false;


    // ==================================================
    // CONVERTIR SEGUNDOS A MM:SS
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


        // Mostrar valores en la interfaz.

        textoInicio.textContent =
            formatearTiempo(inicio);

        textoFin.textContent =
            formatearTiempo(fin);

        textoDuracion.textContent =
            formatearTiempo(duracion);


        // Guardar valores exactos para Flask.

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
    // CREAR REGIÓN SOBRE EL AUDIO ORIGINAL
    // ==================================================

    function crearRegionCompleta(duracion) {

        // Limpiamos una región anterior para evitar
        // tener varias regiones superpuestas.

        regions.clearRegions();


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


    // ==================================================
    // AUDIO ORIGINAL CARGADO
    // ==================================================

    wavesurfer.on(
        "ready",
        function (duracion) {

            console.log(
                "Audio original cargado correctamente"
            );

            console.log(
                "Duración:",
                duracion,
                "segundos"
            );


            crearRegionCompleta(
                duracion
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
    // REPRODUCIR O PAUSAR AUDIO ORIGINAL
    // ==================================================

    botonPlay.addEventListener(
        "click",
        function () {

            reproduciendoSeleccion = false;

            wavesurfer.playPause();

        }
    );


    // ==================================================
    // ESCUCHAR LA SELECCIÓN
    // ==================================================

    botonSeleccion.addEventListener(
        "click",
        function () {

            if (!regionSeleccion) {

                return;
            }


            reproduciendoSeleccion = true;

            regionSeleccion.play();

        }
    );


    // ==================================================
    // ESTADOS DEL REPRODUCTOR
    // ==================================================

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

            reproduciendoSeleccion = false;

            botonPlay.textContent =
                "▶ Reproducir";
        }
    );


    // Cuando termina la selección,
    // detenemos la reproducción.

    regions.on(
        "region-out",
        function (region) {

            if (
                reproduciendoSeleccion &&
                regionSeleccion &&
                region.id === regionSeleccion.id
            ) {

                wavesurfer.pause();

                reproduciendoSeleccion = false;

                botonPlay.textContent =
                    "▶ Reproducir";
            }
        }
    );


    // ==================================================
    // ENVIAR RECORTE A FLASK SIN RECARGAR
    // ==================================================

    if (formularioRecorte) {

        formularioRecorte.addEventListener(
            "submit",
            async function (evento) {

                // Evita cambiar de página.

                evento.preventDefault();


                if (!regionSeleccion) {

                    alert(
                        "Todavía no existe una selección."
                    );

                    return;
                }


                // Guardar los valores actuales
                // justo antes de enviar.

                actualizarSeleccion(
                    regionSeleccion
                );


                const inicio =
                    Number(inputInicio.value);

                const fin =
                    Number(inputFin.value);


                if (
                    !Number.isFinite(inicio) ||
                    !Number.isFinite(fin) ||
                    fin <= inicio
                ) {

                    if (resultadoRecorte) {

                        resultadoRecorte.hidden = false;

                        resultadoRecorte.className =
                            "resultado-recorte error";

                        resultadoRecorte.textContent =
                            "La selección de audio no es válida.";
                    }

                    return;
                }


                console.log(
                    "Inicio enviado:",
                    inputInicio.value
                );

                console.log(
                    "Fin enviado:",
                    inputFin.value
                );


                // Desactivar botón mientras Flask y FFmpeg
                // procesan el recorte.

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

                    const datosFormulario =
                        new FormData(
                            formularioRecorte
                        );


                    const respuesta = await fetch(
                        formularioRecorte.action,
                        {
                            method: "POST",

                            body: datosFormulario
                        }
                    );


                    let resultado;


                    try {

                        resultado =
                            await respuesta.json();

                    } catch {

                        throw new Error(
                            "Flask no devolvió una respuesta JSON válida."
                        );
                    }


                    if (!respuesta.ok) {

                        throw new Error(
                            resultado.mensaje
                            ||
                            "No se pudo completar el recorte."
                        );
                    }


                    // Mostrar resultado correcto.

                    if (resultadoRecorte) {

                        resultadoRecorte.hidden =
                            false;

                        resultadoRecorte.className =
                            "resultado-recorte correcto";

                        resultadoRecorte.textContent =
                            resultado.mensaje;
                    }


                    // Mostrar source_recortado.mp3
                    // en un reproductor separado.
                    //
                    // NO cambiamos la onda principal.
                    // La onda sigue usando source.mp3 original.

                    if (
                        resultado.archivo_recortado === true &&
                        previewRecortado &&
                        audioRecortado
                    ) {

                        console.log(
                            "Cargando vista previa del recorte..."
                        );


                        // Detener una versión anterior
                        // del resultado recortado.

                        audioRecortado.pause();

                        audioRecortado.currentTime = 0;


                        // Cargar el archivo nuevo evitando caché.

                        audioRecortado.src =
                            `/audio/recortado?v=${Date.now()}`;


                        audioRecortado.load();


                        // Mostrar el reproductor.

                        previewRecortado.hidden =
                            false;


                        console.log(
                            "Vista previa del recorte actualizada"
                        );
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

                        resultadoRecorte.hidden =
                            false;

                        resultadoRecorte.className =
                            "resultado-recorte error";

                        resultadoRecorte.textContent =
                            error.message;
                    }

                } finally {

                    if (botonRecortar) {

                        botonRecortar.disabled =
                            false;

                        botonRecortar.textContent =
                            "Recortar y regenerar";
                    }
                }
            }
        );
    }


    // ==================================================
    // ERRORES DE WAVESURFER
    // ==================================================

    wavesurfer.on(
        "error",
        function (error) {

            console.error(
                "Error cargando el audio original:",
                error
            );


            if (resultadoRecorte) {

                resultadoRecorte.hidden =
                    false;

                resultadoRecorte.className =
                    "resultado-recorte error";

                resultadoRecorte.textContent =
                    "No se pudo cargar el audio original.";
            }
        }
    );
}