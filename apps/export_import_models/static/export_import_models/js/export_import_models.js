$(function() {

    // the variable ct_model_pk must be assigned in html file with using DTL
    try {
        ct_model_pk;
        objects_pks;
    } catch (e) {
        // statements
        console.error('Attention!!! Variable not assigned. ' + e);
    }

    var $all_fields = django.jQuery("input[type='checkbox'][name^='model_field']");
    var $btn_select_all_fields = django.jQuery('#btn_select_all_fields');
    var $btn_preview = django.jQuery('#link_admin_export_preview');
    var $btn_download = django.jQuery('#link_admin_export_download');
    var $btn_download_as_csv = django.jQuery('#link_download_as_csv');
    var $formaters = django.jQuery('[name=format_exported_data]');

    //
    function get_format_output(format) {
        return django.jQuery('[name=format_exported_data]:checked').val();
    };

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

    // Preview output data either in JSON or in YAML or XML
    function_changing_href_on_based_choices_fields_and_format = function(event) {

        // get format and fields
        var format = get_format_output();
        var names_choices_fields = get_names_fields_model();

        // make a correct url as Django`s reverse
        var href_for_preview = REVERSE['export_import_models:admin_export_preview'](
            'preview',
            format,
            ct_model_pk,
            names_choices_fields,
            objects_pks
        );
        var href_for_download = REVERSE['export_import_models:admin_export_preview'](
            'download',
            format,
            ct_model_pk,
            names_choices_fields,
            objects_pks
        );
        var href_for_download_as_csv = REVERSE['export_import_models:admin_export_csv'](
            ct_model_pk,
            names_choices_fields,
            objects_pks
        );

        // replace a value of a attribute href on new value
        $btn_preview.attr('href', href_for_preview);
        $btn_download.attr('href', href_for_download);
        $btn_download_as_csv.attr('href', href_for_download_as_csv);
    }
    // add listener of a event to elements
    $formaters.click(function_changing_href_on_based_choices_fields_and_format);
    $all_fields.click(function_changing_href_on_based_choices_fields_and_format);

    // Make all input for fields as checked
    $btn_select_all_fields.click(function(event) {
        $all_fields.prop('checked', 'checked');
    });

    // activate default fields and format output data
    $formaters.first().click()

});
