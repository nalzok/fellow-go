// Initialize all tooltips
$(function () {
    $('[data-toggle="popover"]').popover();
});

// ADD SLIDEDOWN ANIMATION TO DROPDOWN //
$('.dropdown').on('show.bs.dropdown', function(e){
  $(this).find('.dropdown-menu').first().stop(true, true).slideDown(300);
});

// ADD SLIDEUP ANIMATION TO DROPDOWN //
$('.dropdown').on('hide.bs.dropdown', function(e){
  e.preventDefault();
  $(this).find('.dropdown-menu').first().stop(true, true).slideUp(300, function(){
    $(this).parent().removeClass('open');
  });
});