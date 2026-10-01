// ======================================================
// IMPORTAR WAVESURFER
// ======================================================

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


// ======================================================
// SOLO INICIAMOS SI EXISTE EL REPRODUCTOR
// ======================================================

if (
    contenedor &&
    botonPlay &&
    botonSeleccion &&
    textoInicio &&
    textoFin &&
    textoDuracion
) {

    // ==================================================
    // PLUGIN DE REGIONES
    // ==================================================

    const regions = RegionsPlugin.create();


    // ==================================================
    // CREAR WAVESURFER
    // ==================================================

    const wavesurfer = WaveSurfer.create({

        container: "#waveform",

        url: "/audio/source",

        waveColor: "#8a8a8a",

        progressColor: "#ff6600",

        cursorColor: "#ffffff",

        height: 100,

        barGap: 2,

        barWidth: 2,

        barRadius: 2,

        normalize: true,

        dragToSeek: false,

        plugins: [
            regions
        ]
    });


    // ==================================================
    // REGION SELECCIONADA
    // ==================================================

    let regionSeleccion = null;


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
    // ACTUALIZAR LOS TIEMPOS EN PANTALLA
    // ==================================================

    function actualizarTiempos(region) {

        const inicio = region.start;

        const fin = region.end;

        const duracion = fin - inicio;


        textoInicio.textContent =
            formatearTiempo(inicio);

        textoFin.textContent =
            formatearTiempo(fin);

        textoDuracion.textContent =
            formatearTiempo(duracion);


        // Esto nos ayudará después cuando
        // enviemos el recorte a Flask.

        console.log(
            "Inicio:",
            inicio
        );

        console.log(
            "Fin:",
            fin
        );
    }


    // ==================================================
    // CUANDO EL AUDIO ESTÉ CARGADO
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


            // Al principio seleccionamos
            // toda la canción.

            regionSeleccion = regions.addRegion({

                start: 0,

                end: duracion,

                color: "rgba(255, 102, 0, 0.25)",

                drag: true,

                resize: true
            });


            actualizarTiempos(
                regionSeleccion
            );
        }
    );


    // ==================================================
    // CUANDO MOVEMOS LOS EXTREMOS DE LA REGION
    // ==================================================

    regions.on(
        "region-updated",
        function (region) {

            regionSeleccion = region;

            actualizarTiempos(
                regionSeleccion
            );
        }
    );


    // ==================================================
    // BOTON REPRODUCIR / PAUSAR CANCIÓN COMPLETA
    // ==================================================

    botonPlay.addEventListener(
        "click",
        function () {

            wavesurfer.playPause();

        }
    );


    // ==================================================
    // BOTON ESCUCHAR SOLAMENTE LA SELECCION
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


    // ==================================================
    // CUANDO COMIENZA A REPRODUCIR
    // ==================================================

    wavesurfer.on(
        "play",
        function () {

            botonPlay.textContent =
                "⏸ Pausar";

        }
    );


    // ==================================================
    // CUANDO SE PAUSA
    // ==================================================

    wavesurfer.on(
        "pause",
        function () {

            botonPlay.textContent =
                "▶ Reproducir";

        }
    );


    // ==================================================
    // CUANDO TERMINA LA CANCIÓN
    // ==================================================

    wavesurfer.on(
        "finish",
        function () {

            botonPlay.textContent =
                "▶ Reproducir";

        }
    );


    // ==================================================
    // CUANDO TERMINA LA REGION SELECCIONADA
    // ==================================================

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