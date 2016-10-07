(function($) {

    $.fn.change_status_all_checkboxes = function(where_display_count_selected){

        if (where_display_count_selected !== undefined){
            if (where_display_count_selected.length !== 1){
                throw TypeError('The variable "where_display_count_selected" must be is an alone element.');
            }
        }

        var display_count_selected = function(count){

            if (where_display_count_selected !== undefined){
                where_display_count_selected.text(count);
            }
        };


        var $table = $(this).parents('table');

        var lookup_main_checkbox = 'tr th input[type="checkbox"]:first-child';
        var lookup_related_checkboxes = 'tr td input[type="checkbox"]:first-child';

        $(this).bind({
            change: function () {

                var count_checked;
                var is_checked = $(this).is(':checked');
                var $related_checkboxes = $table.find(lookup_related_checkboxes);

                $related_checkboxes.prop('checked', is_checked);

                if (is_checked === true){
                    count_checked = $related_checkboxes.length;
                } else {
                    count_checked = 0;
                }

                // update counter, if it passed
                display_count_selected(count_checked);
            },
        });

        $table.find(lookup_related_checkboxes).bind({
            change: function(){
                var count_checkboxes = $table.find(lookup_related_checkboxes).length;
                var count_checked = $table.find(lookup_related_checkboxes).filter(':checked').length;

                var $main_checkbox = $table.find(lookup_main_checkbox);

                if (($main_checkbox.is(':checked') === false) && (count_checkboxes === count_checked)){
                    $main_checkbox.prop('checked', true);
                } else if (($main_checkbox.is(':checked') === true) && (count_checked === 0)){
                    $main_checkbox.prop('checked', false);
                }

                // update counter, if it passed
                display_count_selected(count_checked);

            },
        });

    };


})(jQuery)
