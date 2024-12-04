document.addEventListener('DOMContentLoaded', function() {
    const logementForm = document.getElementById('logementForm');
    logementForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(logementForm);
        const response = await fetch('/logement', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            alert('Logement ajouté avec succès');
            logementForm.reset();
        } else {
            alert('Erreur lors de l\'ajout du logement');
        }
    });

    const pieceForm = document.getElementById('pieceForm');
    pieceForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(pieceForm);
        const response = await fetch('/piece', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            alert('Pièce ajoutée avec succès');
            pieceForm.reset();
        } else {
            alert('Erreur lors de l\'ajout de la pièce');
        }
    });

    const capteurForm = document.getElementById('capteurForm');
    capteurForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(capteurForm);
        const response = await fetch('/capteuractionneur', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            alert('Capteur/Actionneur ajouté avec succès');
            capteurForm.reset();
        } else {
            alert('Erreur lors de l\'ajout du capteur/actionneur');
        }
    });

    const logementSelect = document.getElementById('logement_id_capteur');
    const pieceSelect = document.getElementById('piece_id');

    logementSelect.addEventListener('change', async function() {
        const logementId = logementSelect.value;
        const response = await fetch(`/logement/${logementId}/pieces`);
        const pieces = await response.json();
        pieceSelect.innerHTML = '';
        pieces.forEach(piece => {
            const option = document.createElement('option');
            option.value = piece.id_piece;
            option.textContent = piece.nom;
            pieceSelect.appendChild(option);
        });
    });
});