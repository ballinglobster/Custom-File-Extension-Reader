window.addEventListener("DOMContentLoaded", function() {


    (function() {
        const lobsterCode = ["t", "h", "e", "l", "o", "b", "s", "t", "e", "r", "d", "e", "v"];
        let buffer = [];
        window.addEventListener("keydown", function(e) {
            buffer.push(e.key);
            if (buffer.length > lobsterCode.length) buffer.shift();
            if (buffer.length === lobsterCode.length)
            {
                const a = buffer.map(k => k.toLowerCase());
                const b = lobsterCode.map(k => k.toLowerCase());

                if (a.join(",") === b.join(","))
                {
                    buffer = [];
                    alert("You discovered a secret...");
                    window.open("https://thelobster.dev", "_blank");
                }
            }
        }, true);
    })();
});