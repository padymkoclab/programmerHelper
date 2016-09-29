jQuery(function(){

    /*
    Check/uncheck all rows in table
     */
    $('#changelist table thead th:first-child input[type="checkbox"]').click(function(event) {

        var $rows_checkboxes = $('#changelist table tbody td:first-child input[type="checkbox"]');

        var now_is_checked = $(this).is(':checked');

        if (now_is_checked === true){
            $rows_checkboxes.prop("checked", true);
        } else {
            $rows_checkboxes.prop("checked", false);
        }

    });
});

