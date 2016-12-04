$(document).ready(function(){
    $('#project_all_table').DataTable({
        responsive:true,
        ajax: "/tflow/tproject/projects/?lu_sql=get_project&lu_response_field=name,project_key,lead,url&lu_plain_data"
    });
});
