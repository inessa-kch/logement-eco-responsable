document.addEventListener('DOMContentLoaded', function() {
    const logementButtons = document.querySelectorAll('.custom-button');
    const capteurTableBody = document.getElementById('capteurTableBody');
    let selectedLogementId = null;  // Track the currently selected logement

    // Fetch and Update Capteurs/Actionneurs on Logement Selection
    logementButtons.forEach(button => {
        button.addEventListener('click', async function() {
            selectedLogementId = button.getAttribute('data-logement-id');
            fetchAndUpdateCapteurs(selectedLogementId);
        });
    });

    // Fetch Capteurs/Actionneurs for the selected Logement
    async function fetchAndUpdateCapteurs(logementId) {
        const response = await fetch(`/capteuractionneurs?logement_id=${logementId}&json=true`);
        if (response.ok) {
            const capteuractionneurs = await response.json();
            updateCapteurTable(capteuractionneurs);
        } else {
            console.error('Error fetching capteuractionneurs');
            capteurTableBody.innerHTML = '<tr><td colspan="3">Erreur de chargement des capteurs/actionneurs</td></tr>';
        }
    }

    // Update the Capteur/Actionneur Table in the UI
    function updateCapteurTable(capteuractionneurs) {
        capteurTableBody.innerHTML = '';  // Clear the existing table
        if (capteuractionneurs.length === 0) {
            capteurTableBody.innerHTML = '<tr><td colspan="4">Aucun capteur/actionneur disponible</td></tr>';
        } else {
            capteuractionneurs.forEach(capteuractionneur => {
                const capteurRow = document.createElement('tr');
                capteurRow.innerHTML = `
                    <td>${capteuractionneur.reference_commerciale}</td>
                    <td>${capteuractionneur.nom_type}</td>
                    <td>${capteuractionneur.port_communication}</td>
                    <td>
                        <label class="switch">
                            <input type="checkbox" class="etat-switch" data-id="${capteuractionneur.id_capAct}" ${capteuractionneur.etat ? 'checked' : ''}>
                            <span class="slider round"></span>
                        </label>
                    </td>
                `;
                capteurTableBody.appendChild(capteurRow);
            });

            // Add event listeners to the switches
            const switches = document.querySelectorAll('.etat-switch');
            switches.forEach(switchElement => {
                switchElement.addEventListener('change', function() {
                    const capteuractionneurId = switchElement.getAttribute('data-id');
                    const newState = switchElement.checked;
                    console.log(`CapteurActionneur ${capteuractionneurId} state changed to ${newState}`);
                });
            });
        }
    }
});