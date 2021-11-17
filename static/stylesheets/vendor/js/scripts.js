$(document).scroll(function () {
  var isScrolled = $(this).scrollTop() > $(".topbar").height();
  $(".homenav").toggleClass("scrolled", isScrolled);
  $(".homenav").toggleClass("fixed-top", isScrolled);

  // console.log(isScrolled);
  // console.log();
});
