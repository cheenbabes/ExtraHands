$(document).ready(function(){

    //$('#on-call').click(function(event){
    //    $.ajax({
    //        type:'POST',
    //        url: '/action/on-call/'
    //    }).success(function(data, status){
    //        $('#on-call').removeClass('btn-warning').addClass('btn-success');
    //        $('#on-call').prop('value', 'You\'re on call!');
    //    })
    //});

    $('#editTeacherTimeDifference').click(function(){
        event.preventDefault();
       $('#timeBetweenEventsInput').removeAttr("disabled").attr("placeholder","Enter a value (hours)");
    });
});

