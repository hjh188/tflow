$(document).ready(function(){
    // hide the sidemenu
    $('.left-side').toggleClass("collapse-left");
    $(".right-side").toggleClass("strech");

    // init the modal
    $('#create-project-modal').modal({
        backdrop: false,
        show: false,
        keyboard: false,
    });

    // do the dynamical setting here before the modal show
    $('#create-project-modal').on('show.bs.modal', function(){
        $.get('/tflow/tuser/users/?lu_sql_search_condition=username!="' + username + '"&lu_response_field=id,username', function(data){
            $("#project-leader").empty();

            // put the login user in the first and set the default selected
            $("#project-leader").append('<option value=' + username + '>' + username + '</option>');
            $.each(data.data, function(i, user){
                $("#project-leader").append('<option value=' + user.username + '>' + user.username + '</option>');
            });

            // solve the bootstrap select not refresh after dynamical element append
            $("#project-leader").selectpicker('refresh');
        });
    });

    // create project action
    $("#create-project-btn").on('click', function(){
        $.ajax({
            url: '/tflow/tproject/projects/',
            type: 'POST',
            data: $("#create-project-form").serialize(),
            success: function(data){
                $("#create-project-modal").modal('hide');
            },
            error: function(data){
                alert(data.responseText);
            },
        });
    });
});


