(function($){

    /*

    */

    var lookup_format_labels = '#table_formats td label';
    var class_name = 'active_format_output';
    $(lookup_format_labels).bind({

        click: function(event) {
            $(lookup_format_labels).removeClass(class_name);
            $(this).addClass(class_name);

            var $btn_preview = $('#btn_preview');
            if ($(this).hasClass('active_format_output') && $(this).attr('for') === 'radio_csv'){
                $btn_preview.addClass('hidden');
            } else {
                $btn_preview.removeClass('hidden');
            }
        },

    });

    /*

    */
   $('#table_fields th input[type="checkbox"]:first-child').change_status_all_checkboxes();

   $('#table_object_list th input[type="checkbox"]:first-child').
    change_status_all_checkboxes(
        $('#count_selected_objects')
    );

})(jQuery);
