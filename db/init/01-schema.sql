-- Kunde 1:1 Adresse, Kunde 1:N Bestellung

CREATE TABLE kunde (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- Versionsnummer fuer optimistische Synchronisation (Vermeidung von Lost Updates)
    version     INTEGER NOT NULL DEFAULT 0,
    nachname    VARCHAR(64) NOT NULL,
    vorname     VARCHAR(64) NOT NULL,
    email       VARCHAR(128) NOT NULL UNIQUE,
    geburtsdatum DATE,
    erzeugt     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    aktualisiert TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 1:1: UNIQUE auf dem Fremdschluessel
CREATE TABLE adresse (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    strasse     VARCHAR(128) NOT NULL,
    hausnummer  VARCHAR(16) NOT NULL,
    plz         CHAR(5) NOT NULL CHECK (plz ~ '^\d{5}$'),
    ort         VARCHAR(64) NOT NULL,
    kunde_id    INTEGER NOT NULL UNIQUE REFERENCES kunde(id) ON DELETE CASCADE
);

-- 1:N
CREATE TABLE bestellung (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    produktname VARCHAR(128) NOT NULL,
    menge       INTEGER NOT NULL CHECK (menge > 0),
    preis       NUMERIC(10, 2) NOT NULL CHECK (preis >= 0),
    bestelldatum DATE NOT NULL DEFAULT CURRENT_DATE,
    kunde_id    INTEGER NOT NULL REFERENCES kunde(id) ON DELETE CASCADE
);

CREATE INDEX bestellung_kunde_id_idx ON bestellung(kunde_id);
