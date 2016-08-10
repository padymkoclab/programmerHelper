$(function() {

    var $all_fields = django.jQuery("input[type='checkbox'][name^='model_field']");
    var $formaters = django.jQuery('[name=format_export_data]');
    var $btn_select_all_fields = django.jQuery('#btn_select_all_fields');
    var $btn_submit_export_preview = django.jQuery('#btn_submit_export_preview');
    var $radio_formats_exported_data = django.jQuery("input[type='radio'][name='format_export_data']");
    var $labels_radio_formats_exported_data = $radio_formats_exported_data.parent();

    //
    function get_names_fields_model() {

        //
        var names_choices_fields = [];
        var choiced_fields = django.jQuery("input[type='checkbox'][name^='model_field']:checked");

        // select only a checked fields
        choiced_fields.each(function(index, el) {
            var field_name = django.jQuery(el).val();
            names_choices_fields.push(field_name);
        });

        // transform the array to a commas-separated string
        names_choices_fields = names_choices_fields.join(',')

        return names_choices_fields
    }


    // Make all input for fields as checked
    $btn_select_all_fields.click(function(event) {
        $all_fields.prop('checked', 'checked');
    });

    // activate default fields and format output data
    $formaters.first().click()

    /**
     * [description]
     * @param  {[type]} event) {                   if (django.jQuery(this).hasClass('disabled') [description]
     * @return {[type]}        [description]
     */
   $btn_submit_export_preview.click(function(event) {
        if (django.jQuery(this).hasClass('disabled') === true) {
            event.preventDefault();
            alert('You don`t have ability for preview XLSX or CSV.!');
        } else {

        };
    });

   /**
    * [description]
    * @param  {[type]} event) {                  alert('message')   } [description]
    * @return {[type]}        [description]
    */

   var color_labels_radio_formats_exported_data = $labels_radio_formats_exported_data.css('color');
   var background_color_labels_radio_formats_exported_data = $labels_radio_formats_exported_data.css('background-color');
   $radio_formats_exported_data.click(function(event) {

        var active_background_color = 'rgb(47, 150, 180)';
        var active_text_color = 'rgb(256, 256, 256)';

        // reset all background colors in labels of radio inputs
        django.jQuery("input[type='radio'][name='format_export_data']").parent().css({
            'background-color': background_color_labels_radio_formats_exported_data,
            'color': color_labels_radio_formats_exported_data,
        });

        var $checked_radio_formats_exported_data = django.jQuery("input[type='radio'][name='format_export_data']:checked");
        var $label_of_radio_input = $checked_radio_formats_exported_data.parent();
        $label_of_radio_input.css('background-color', active_background_color);
        $label_of_radio_input.css('color', active_text_color);

        /*
        Restiction for preview format output
         */
       var format_output = django.jQuery(this).val();
       var re_exp = new RegExp('json|xml|yaml');
       var is_format_with_preview = re_exp.test(format_output);
       if (is_format_with_preview){
            $btn_submit_export_preview.removeClass('disabled');
       } else {
            $btn_submit_export_preview.addClass('disabled');
       };
   });

   django.jQuery('#format_export_data_json').click();

});
