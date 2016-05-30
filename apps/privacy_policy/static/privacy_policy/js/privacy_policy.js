$(function() {

    $('#tabs_privacy_policy li').on('click', function() {
        $('#tabs_privacy_policy li').removeClass('active');
        $(this).addClass('active');
    });

    $('#top_navbar_panel').removeClass('navbar-fixed-top').addClass('navbar-static-top')
});
