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
            capteurTableBody.innerHTML = '<tr><td colspan="5">Erreur de chargement des capteurs/actionneurs</td></tr>';
        }
    }

    // Update the Capteur/Actionneur Table in the UI
    function updateCapteurTable(capteuractionneurs) {
        capteurTableBody.innerHTML = '';  // Clear the existing table
        if (capteuractionneurs.length === 0) {
            capteurTableBody.innerHTML = '<tr><td colspan="5">Aucun capteur/actionneur disponible</td></tr>';
        } else {
            capteuractionneurs.forEach(capteuractionneur => {
                const lastMesureDisplay = capteuractionneur.unite_mesure === 'bool'
                    ? (capteuractionneur.last_mesure === 1 ? 'ON' : 'OFF')
                    : `${capteuractionneur.last_mesure} ${capteuractionneur.unite_mesure}`;
                
                const capteurRow = document.createElement('tr');
                capteurRow.innerHTML = `
                    <td>${capteuractionneur.reference_commerciale}</td>
                    <td>${capteuractionneur.nom_type}</td>
                    <td>${capteuractionneur.port_communication}</td>
                    <td>${capteuractionneur.last_mesure !== null ? lastMesureDisplay : 'N/A'}</td>
                    <td>
                        ${capteuractionneur.unite_mesure === 'bool' ? `
                        <label class="switch">
                            <input type="checkbox" class="etat-switch" data-id="${capteuractionneur.id_capAct}" ${capteuractionneur.last_mesure_value === 1 ? 'checked' : ''}>
                            <span class="slider round"></span>
                        </label>` : ''}
                    </td>
                `;
                capteurTableBody.appendChild(capteurRow);
            });

            // Add event listeners to the switches
            const switches = document.querySelectorAll('.etat-switch');
            switches.forEach(switchElement => {
                switchElement.addEventListener('change', async function() {
                    const capteuractionneurId = switchElement.getAttribute('data-id');
                    const newState = switchElement.checked ? 1 : 0;
                    await addMesure(capteuractionneurId, newState);
                    await updateLastMesure(capteuractionneurId, newState);
                });
            });
        }
    }

    // Add a new measure to the database
    async function addMesure(capteuractionneurId, valeur) {
        const response = await fetch('/mesure/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_capAct: capteuractionneurId,
                valeur: valeur,
                date_mesure: new Date().toISOString()
            })
        });
        if (response.ok) {
            console.log(`Mesure added for CapteurActionneur ${capteuractionneurId} with value ${valeur}`);
        } else {
            console.error('Error adding mesure');
        }
    }

    // Update the last measure in the UI
    async function updateLastMesure(capteuractionneurId, valeur) {
        const capteurRow = document.querySelector(`.etat-switch[data-id="${capteuractionneurId}"]`).closest('tr');
        const lastMesureCell = capteurRow.querySelector('td:nth-child(4)');
        lastMesureCell.textContent = valeur === 1 ? 'ON' : 'OFF';
    }

    // Update the measure in the table
    function updateMesureInTable(mesure) {
        const capteurRow = document.querySelector(`.etat-switch[data-id="${mesure.id_capAct}"]`).closest('tr');
        if (capteurRow) {
            const lastMesureCell = capteurRow.querySelector('td:nth-child(4)');
            const lastMesureDisplay = mesure.unite_mesure === 'bool'
                ? (mesure.valeur === 1 ? 'ON' : 'OFF')
                : `${mesure.valeur} ${mesure.unite_mesure}`;
            lastMesureCell.textContent = lastMesureDisplay;
        }
    }
});