document.addEventListener('DOMContentLoaded', function() {
    const logementForm = document.getElementById('logementForm');
    const pieceForm = document.getElementById('pieceForm');
    const capteurForm = document.getElementById('capteurForm');
    const logementSelectForPiece = document.getElementById('logement_id');
    const pieceSelect = document.getElementById('piece_id');
    const logementSelectForCapteur = document.getElementById('logement_id_capteur');
    const pieceSelectForCapteur = document.getElementById('piece_id');

    logementForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        if (!logementForm.checkValidity()) {
            alert('Veuillez remplir tous les champs.');
            return;
        }
        const formData = new FormData(logementForm);
        const response = await fetch('/logement', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const newLogement = await response.json();
            
            updateLogementDropdowns(newLogement);
            logementForm.reset();
        } else {
            //alert('Erreur lors de l\'ajout du logement');
        }
    });

    pieceForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        if (!pieceForm.checkValidity()) {
            alert('Veuillez remplir tous les champs.');
            return;
        }
        const formData = new FormData(pieceForm);
        const response = await fetch('/piece', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            pieceForm.reset();
        } else {
           // alert('Erreur lors de l\'ajout de la pièce');
        }
    });

    capteurForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        if (!capteurForm.checkValidity()) {
            alert('Veuillez remplir tous les champs.');
            return;
        }
        const formData = new FormData(capteurForm);
        const response = await fetch('/capteuractionneur', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            capteurForm.reset();
        } else {
            //alert('Erreur lors de l\'ajout du capteur/actionneur');
        }
    });

    logementSelectForPiece.addEventListener('change', async function() {
        const logementId = logementSelectForPiece.value;
        const response = await fetch(`/logement/${logementId}/pieces`);
        if (response.ok) {
            const pieces = await response.json();
            pieceSelect.innerHTML = '<option value="" disabled selected>Select Piece</option>';
            pieces.forEach(piece => {
                const option = document.createElement('option');
                option.value = piece.id_piece;
                option.textContent = piece.nom;
                pieceSelect.appendChild(option);
            });
        } else {
            alert('Erreur lors de la récupération des pièces');
        }
    });

    logementSelectForCapteur.addEventListener('change', async function() {
        const logementId = logementSelectForCapteur.value;
        const response = await fetch(`/logement/${logementId}/pieces`);
        if (response.ok) {
            const pieces = await response.json();
            pieceSelectForCapteur.innerHTML = '<option value="" disabled selected>Select Piece</option>';
            pieces.forEach(piece => {
                const option = document.createElement('option');
                option.value = piece.id_piece;
                option.textContent = piece.nom;
                pieceSelectForCapteur.appendChild(option);
            });
        } else {
            alert('Erreur lors de la récupération des pièces');
        }
    });

    async function updateLogementDropdowns(newLogement) {
        const logementOption = document.createElement('option');
        logementOption.value = newLogement.id_logement;
        logementOption.textContent = newLogement.adresse;

        const logementDropdowns = document.querySelectorAll('#logement_id, #logement_id_capteur');
        logementDropdowns.forEach(dropdown => {
            dropdown.appendChild(logementOption.cloneNode(true));
        });
    }
});