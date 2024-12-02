document.addEventListener('DOMContentLoaded', function() {
    const cardTitles = document.querySelectorAll('.card-title');
    cardTitles.forEach(title => {
        const date = new Date(title.textContent);
        const options = { weekday: 'long', day: 'numeric', month: 'numeric' };
        title.textContent = date.toLocaleDateString('fr-FR', options);
    });
});