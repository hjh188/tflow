jQuery(document).ready(function(){
    // Menu sortable
    $("#sidebar_menu_top,#menu").sortable({
        stop: function(event, ui) {
            var sidebar_menu_top = $("#sidebar_menu_top").sortable("toArray");
            var sidebar_menu_bottom = $("#menu").sortable("toArray");
            $.post('/tflow/tuser/users/', {lu_sql: 'set_menu', lu_sql_param: 'sidebar_menu_top[],sidebar_menu_bottom[],username',
                                           'sidebar_menu_top[]': sidebar_menu_top, 'sidebar_menu_bottom[]': sidebar_menu_bottom, username: username});
        },
    });

    $("#sidebar_threeicons,#menu").disableSelection();
});
