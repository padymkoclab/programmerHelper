(function($){

    /*

    */
    $('#table_formats td').bind({
        click: function(event) {

            var class_name = 'active_format_output';

            $('#table_formats td').removeClass(class_name)
            $(this).addClass(class_name);
        },
    });

})(jQuery);
