document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('price-comparison-form');
  var loader = document.querySelector('.custom-loader');

  form.addEventListener('submit', function(event) {
    event.preventDefault();
    loader.classList.remove('hidden');
    form.style.display = 'none';
    document.querySelector('pre').style.display = 'none';
    form.submit();
  });
});
