jQuery(function(){

    check_up_count_selected_objects = function check_up_count_selected_objects (){
        var count_selected = $('#changelist table tbody td input[type="checkbox"]:checked').length;
        $('#count_selected_objects').text(count_selected);
    }

    /*
    Check/uncheck all rows in table
     */
    $('#changelist table thead th:first-child input[type="checkbox"]').bind('click', function(event) {

        var $rows_checkboxes = $('#changelist table tbody td:first-child input[type="checkbox"]');

        var now_is_checked = $(this).is(':checked');

        if (now_is_checked === true){
            $rows_checkboxes.prop("checked", true);
        } else {
            $rows_checkboxes.prop("checked", false);
        }

        check_up_count_selected_objects()

    });

    /*

    */
   $('#changelist table tbody td input[type="checkbox"]').bind('change', function(e){
        check_up_count_selected_objects();
    });

});

