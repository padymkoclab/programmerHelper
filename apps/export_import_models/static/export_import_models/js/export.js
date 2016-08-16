$(function() {
  var $btn_select_all_fields = django.jQuery('#btn_select_all_fields');
  var $radio_formats_exported_data = django.jQuery("input[type='radio'][name='format_export_data']");
  var $labels_radio_formats_exported_data = $radio_formats_exported_data.parent();

  // checkboxes with fields names
  var $all_fields = django.jQuery("#table_fields tbody input[type='checkbox']");

  // a button for check all the checkboxes with fields names as checked
  var $btn_select_all_fields = django.jQuery('#btn_select_all_fields');

  /*
  Make all input for fields as checked
   */
  $btn_select_all_fields.click(function(event) {
    event.preventDefault();
    $all_fields.prop('checked', 'checked');
  });

  /*
  A one field must checked always, if is not - checked all the fields.
   */
  $all_fields.click(function(e) {
    var count_checked_fields = django.jQuery("#table_fields tbody input[type='checkbox']").filter(':checked').length;

    if (count_checked_fields == 0) {
      $btn_select_all_fields.click();
    }
  });

   /**
    * Applying additional styles for radios box and its label
  */
  var color_labels_radio_formats_exported_data = $labels_radio_formats_exported_data.css('color');
  var background_color_labels_radio_formats_exported_data = $labels_radio_formats_exported_data.css('background-color');
  $radio_formats_exported_data.click(function(event) {

    // colors
    var active_background_color = 'rgb(47, 150, 180)';
    var active_text_color = 'rgb(256, 256, 256)';

    // reset all background colors in labels of radio inputs
    django.jQuery("input[type='radio'][name='format_export_data']").parent().css({
      'background-color': background_color_labels_radio_formats_exported_data,
      'color': color_labels_radio_formats_exported_data
    });

    // find new selected format and its label
    var $checked_radio_formats_exported_data = django.jQuery("input[type='radio'][name='format_export_data']:checked");
    var $label_of_radio_input = $checked_radio_formats_exported_data.parent();

    // applying styles
    $label_of_radio_input.css('background-color', active_background_color);
    $label_of_radio_input.css('color', active_text_color);
  });

  // activate default format output data
  django.jQuery('[name=format_export_data]').first().click();
  django.jQuery('[name=format_export_data]').first().click();
});
