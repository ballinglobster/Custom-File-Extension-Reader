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
    var element = document.getElementById('file-content');
    element.textContent = contents;
    
}

document.getElementById('file-input')
    .addEventListener('change', readSingleFile, false);