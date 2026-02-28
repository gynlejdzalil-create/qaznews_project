// Бургер меню
var burgerBtn = document.getElementById('burgerBtn');
var mainNav = document.getElementById('mainNav');

if (burgerBtn) {
    burgerBtn.addEventListener('click', function() {
        mainNav.classList.toggle('open');
    });
}

// Закрыть меню при клике вне
document.addEventListener('click', function(e) {
    if (mainNav && burgerBtn) {
        if (!mainNav.contains(e.target) && !burgerBtn.contains(e.target)) {
            mainNav.classList.remove('open');
        }
    }
});
