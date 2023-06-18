document.addEventListener("DOMContentLoaded", function () {
  var mobileMenuToggle = document.getElementById("mobile-menu-toggle");
  var mobileMenu = document.querySelectorAll("#nav1, #nav2, #nav3, #nav4, #nav5");

  mobileMenuToggle.addEventListener("click", function () {
    mobileMenu.forEach(function (element) {
      element.classList.toggle("mobile-menu-open");
    });
  });
});