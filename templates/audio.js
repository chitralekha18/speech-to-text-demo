// Initialize WaveSurfer
var wavesurfer = WaveSurfer.create({
    container: '#waveform'
});

// Once the user loads a file in the fileinput, the file should be loaded into waveform
document.getElementById("fileinput").addEventListener('change', function(e){
    var file = this.files[0];

    if (file) {
        var reader = new FileReader();
        
        reader.onload = function (evt) {
            // Create a Blob providing as first argument a typed array with the file buffer
            var blob = new window.Blob([new Uint8Array(evt.target.result)]);

            // Load the blob into Wavesurfer
            wavesurfer.loadBlob(blob);
        };

        reader.onerror = function (evt) {
            console.error("An error ocurred reading the file: ", evt);
        };

        // Read File as an ArrayBuffer
        reader.readAsArrayBuffer(file);
    }
}, false);

// Play button
const button = document.querySelector('[data-action="play"]');
button.addEventListener('click', wavesurfer.playPause.bind(wavesurfer));
const stopButton = document.querySelector('[data-action="stop"]');
stopButton.addEventListener('click', wavesurfer.pause.bind(wavesurfer));