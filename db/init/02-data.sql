INSERT INTO kunde (nachname, vorname, email, geburtsdatum) VALUES
    ('Mustermann', 'Max', 'max@acme.de', '1990-01-31'),
    ('Musterfrau', 'Erika', 'erika@acme.de', '1985-06-15'),
    ('Schmidt', 'Anna', 'anna@acme.de', '2000-12-01');

INSERT INTO adresse (strasse, hausnummer, plz, ort, kunde_id) VALUES
    ('Moltkestrasse', '30', '76133', 'Karlsruhe', 1),
    ('Kaiserstrasse', '12a', '76131', 'Karlsruhe', 2),
    ('Hauptstrasse', '5', '69117', 'Heidelberg', 3);

INSERT INTO bestellung (produktname, menge, preis, bestelldatum, kunde_id) VALUES
    ('Tastatur', 1, 49.99, '2026-09-01', 1),
    ('Maus', 2, 19.90, '2026-09-01', 1),
    ('Monitor', 1, 229.00, '2026-09-20', 2),
    ('USB-Kabel', 3, 7.50, '2026-10-02', 3);
