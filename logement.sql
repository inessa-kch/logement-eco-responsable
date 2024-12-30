DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS CapteurActionneur;
DROP TABLE IF EXISTS TypeCapteurActionneur;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Facture;

CREATE TABLE Logement (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,
    numero_telephone TEXT,
    adresse_ip TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    position_x INTEGER,
    position_y INTEGER,
    position_z INTEGER,
    logement_id INTEGER,
    FOREIGN KEY (logement_id) REFERENCES Logement(id_logement)
);

CREATE TABLE TypeCapteurActionneur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_type TEXT NOT NULL,
    unite_mesure TEXT,
    precision_min INTEGER,
    precision_max INTEGER
);

CREATE TABLE CapteurActionneur(
    id_capAct INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_commerciale TEXT NOT NULL,
    id_piece INTEGER,
    port_communication INTEGER,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_type INTEGER,
    FOREIGN KEY (id_piece) REFERENCES Piece(id_piece),
    FOREIGN KEY (id_type) REFERENCES TypeCapteurActionneur(id_type) 
);


CREATE TABLE Mesure(
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    valeur INTEGER,
    date_mesure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_capAct INTEGER,
    FOREIGN KEY (id_capAct) REFERENCES CapteurActionneur(id_capAct)
);

CREATE TABLE Facture(
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    type_facture TEXT NOT NULL,
    date_facture DATE,
    montant INTEGER,
    valeur_consommation FLOAT,
    unite_consommation TEXT,
    id_logement INTEGER,
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement)
);


INSERT INTO Logement (adresse, numero_telephone, adresse_ip)
VALUES ('124 boulevard de la madeleine', '0644439027', '91.198.174.192');

INSERT INTO Piece (nom, position_x, position_y, position_z, logement_id)
VALUES 
('Cuisine', 2, 1, 2, (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Salon',2, 4, 2,(SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Chambre', 7, 3, 2, (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Salle de bain', 7, 1, 2, (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine'));


INSERT INTO TypeCapteurActionneur (nom_type, unite_mesure, precision_min, precision_max)
VALUES
('Temperature', '°C', -50, 50),
('Fermeture rideaux', 'bool', 0, 1),
('Humidite', '%', 0, 100),
('Ouverture fenetre', 'bool', 0, 1);


INSERT INTO CapteurActionneur (reference_commerciale, id_piece, port_communication, id_type)
VALUES
('Capteur temperature chambre', (SELECT id_piece FROM Piece WHERE nom = 'Chambre'), 5001, (SELECT id_type FROM TypeCapteurActionneur WHERE nom_type = 'Temperature')),
('Actionneur fermeture rideaux chambre', (SELECT id_piece FROM Piece WHERE nom = 'Chambre'), 5004, (SELECT id_type FROM TypeCapteurActionneur WHERE nom_type = 'Fermeture rideaux')),
('Capteur Humidite cuisine', (SELECT id_piece FROM Piece WHERE nom = 'Cuisine'),5002, (SELECT id_type FROM TypeCapteurActionneur WHERE nom_type = 'Humidite')),
('Actionneur Ouverture fenetre salon', (SELECT id_piece FROM Piece WHERE nom = 'Salon'),5003, (SELECT id_type FROM TypeCapteurActionneur WHERE nom_type = 'Ouverture fenetre')),
('Capteur temperature salle de bain', (SELECT id_piece FROM Piece WHERE nom = 'Salle de bain'),5001, (SELECT id_type FROM TypeCapteurActionneur WHERE nom_type = 'Temperature'));


INSERT INTO Mesure (valeur, id_capAct)
VALUES
(21, (SELECT id_capAct FROM CapteurActionneur WHERE reference_commerciale = 'Capteur temperature chambre')),
(1, (SELECT id_capAct FROM CapteurActionneur WHERE reference_commerciale = 'Actionneur fermeture rideaux chambre')),
(50, (SELECT id_capAct FROM CapteurActionneur WHERE reference_commerciale = 'Capteur Humidite cuisine')),
(0, (SELECT id_capAct FROM CapteurActionneur WHERE reference_commerciale = 'Actionneur Ouverture fenetre salon')),
(23, (SELECT id_capAct FROM CapteurActionneur WHERE reference_commerciale = 'Capteur temperature salle de bain'));

INSERT INTO Facture (type_facture, date_facture, montant, valeur_consommation,unite_consommation, id_logement)
VALUES
('Eau', '2024-11-12', 47, 296.2,'L', (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Electricite', '2024-11-12', 52, 650.8 ,'kWh', (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Internet', '2024-11-12', 25, 15.4, 'Go', (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Eau', '2024-10-12', 43, 254.1,'L', (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Electricite', '2024-10-12', 48, 478.4 ,'kWh', (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine')),
('Internet', '2024-10-12', 25, 21.6, 'Go', (SELECT id_logement FROM Logement WHERE adresse = '124 boulevard de la madeleine'));

