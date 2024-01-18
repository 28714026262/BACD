$(function(){
    $('#input1').keyup(function(){
        $('#message').text('Hello! ' + $('#input1').val());
    })
})