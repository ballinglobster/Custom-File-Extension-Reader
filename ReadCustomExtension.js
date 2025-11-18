window.addEventListener("DOMContentLoaded", function() {
    function initChannel() {
        if (typeof qt !== "undefined" && typeof QWebChannel !== "undefined") {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.backend = channel.objects.backend;
                //if (backend.compressionFinished) backend.compressionFinished.connect(function(p){ alert("Compressed to: " + p); });
                //if (backend.compressionFailed) backend.compressionFailed.connect(function(e){ alert("Compression failed: " + e); });
            });
            return true;
        }
        return false;
    }

    if (!initChannel()) {
        // try again after a short delay
        setTimeout(initChannel, 100);
    }

    (function() {
        const konami = ["ArrowUp", "ArrowUp", "ArrowDown", "ArrowDown", "ArrowLeft", "ArrowRight", "ArrowLeft", "ArrowRight", "b", "a"];
        let buffer = [];
        window.addEventListener("keydown", function(e) {
            buffer.push(e.key);
            if (buffer.length > konami.length) buffer.shift();
            if (buffer.length === konami.length)
            {
                const a = buffer.map(k => k.toLowerCase());
                const b = konami.map(k => k.toLowerCase());
                if (a.join(",") === b.join(","))
                {
                    buffer = [];
                    alert("You discovered a secret...");
                    if (window.backend && window.backend.launchDoom)
                    {
                        window.backend.launchDoom();
                    }
                    else alert("Backend or launchDoom method not available.");
                }
            }
        }, true);
    })();
});

function readSingleFile(e)
{
    var file = e.target.files[0];
    if (!file) return;

    var reader = new FileReader();
    reader.onload = function(e)
    {
        var contents = e.target.result;
        if (contents === "")
        {
            contents = "File is empty.";
            DisplayContents(contents);
        }
        else if (contents === "thelobsterdev")
        {
            window.open("https://thelobster.dev", "_blank");
        }
        else if (contents === "John Doe")
        {
            alert("Hello, John Doe!");
        }
        else
        {
            DisplayContents(contents);
        }
    };

    reader.readAsText(file);
}

function DisplayContents(contents)
{
    var element = document.getElementById("file-content");
    element.textContent = contents;
    
}

function compressSelectedFile()
{
    var input = document.getElementById("file-input");
    var file = input.files[0];
    if (!file)
    {
        alert("No file selected for compression.");
        return;
    }

    var reader = new FileReader();
    reader.onload = function(e)
    {
        var bytes = new Uint8Array(e.target.result);
        var binary = "";
        for (var i = 0; i < bytes.byteLength; i++)
        {
            binary += String.fromCharCode(bytes[i]);
        }
        var b64 = btoa(binary);

        var methodElement = document.getElementById("compression-method");
        var method = (methodElement && methodElement.value) ? methodElement.value : "gzip";

        if (window.backend && window.backend.receiveFileForCompression)
        {
            window.backend.receiveFileForCompression(file.name, b64, method);
        }
        else
        {
            alert("Backend is not available.");
        }
    }

    reader.readAsArrayBuffer(file);
}

function decompressSelectedFile()
{
    var input = document.getElementById("file-input");
    var file = input.files[0];
    if (!file)
    {
        alert("No file selected for compression.");
        return;
    }

    var reader = new FileReader();
    reader.onload = function(e)
    {
        var bytes = new Uint8Array(e.target.result);
        var binary = "";

        for (var i = 0; i < bytes.byteLength; i++)
        {
            binary += String.fromCharCode(bytes[i]);
        }
        var b64 = btoa(binary);

        var methodElement = document.getElementById("compression-method");
        var method = (methodElement && methodElement.value) ? methodElement.value : "gzip";

        if (window.backend && window.backend.receiveFileForDecompression)
        {
            window.backend.receiveFileForDecompression(file.name, b64, method);
        }
        else
        {
            alert("Backend is not available.");
        }
    }

    reader.readAsArrayBuffer(file);
}

document.getElementById('file-input')
    .addEventListener('change', readSingleFile, false);

document.getElementById('compress-btn')
    .addEventListener('click', compressSelectedFile, false);

document.getElementById('decompress-btn')
    .addEventListener('click', decompressSelectedFile, false);