$(function() {
    console.log( "ready!" );

    $( "#fileInput" ).change(function() {
        var fileToUpload = $('#fileInput').prop('files')[0];

        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageSrc').attr('src', e.target.result);
        }
        reader.readAsDataURL(fileToUpload);

    });

   
    $("#imageSrc").on('load', function() { 
        console.log("image loaded correctly"); 

        var imgElement = $('#imageSrc').get(0);

        let image = cv.imread(imgElement);
        cv.imshow('imageCanvas', image);
        image.delete();
    })
    .on('error', function() { console.log("error loading image"); });

})


