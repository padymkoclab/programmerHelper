django.jQuery(function($) {

    // Wrapper contains input-ranges
    var $div_input_ranges_durationfield = $('.div_input_ranges_durationfield');

    // Field for timedelta`s value
    var $input_timedelta = $('.div_input_ranges_durationfield').parent().children().filter(':first-child');

    /*
    Add CSS class to input timedelta
    since pure CSS does not have feature for keep previous element
     */
    $input_timedelta.addClass('correct_possition_input_with_ranges_inputs');

    /*
    Determinate timedelta by four input-range
     */
    $div_input_ranges_durationfield.find('input[type="range"]').change(function(e){

        var days = $div_input_ranges_durationfield.find('input[name="days"]').val();
        var hours = $div_input_ranges_durationfield.find('input[name="hours"]').val();
        var minutes = $div_input_ranges_durationfield.find('input[name="minutes"]').val();
        var seconds = $div_input_ranges_durationfield.find('input[name="seconds"]').val();

        if (hours < 10){
            hours = '0' + hours;
        }

        if (minutes < 10){
            minutes = '0' + minutes;
        }

        if (seconds < 10){
            seconds = '0' + seconds;
        }

        var timedelta = hours + ':' + minutes + ':' + seconds;

        if (Number.parseInt(days) !== 0) {
            timedelta = days + ' ' + timedelta;
        }

        $input_timedelta.val(timedelta);
    });
});
