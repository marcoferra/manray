$(function() {
    console.log( "readsssy!" );

    $("#uploadForm").submit(function(event){
        console.log("Submitting");
        event.preventDefault();
    
        var formData = new FormData($(this)[0]);
    
        $.ajax({
        url: '/add',
        type: 'POST',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (returndata) {
            
            imageSrc.src = returndata.filePath;
            console.log(returndata);
        }
        });
    
        return false;
    });
})


