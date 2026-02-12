### Migration Test

PS: Non e tutto il modulo di base_solidali e stato preso solo quello necessario per far vedere se la migrazione funziona 
salto di versione -> 6.0.1.0 -> 16.0.1.2.

Step 1: Modifica del Codice Python (I Modelli)
Prima di tutto, devi aggiornare la struttura dei tuoi modelli. Il campo deve "sparire" dal vecchio posto e "apparire" nel nuovo.

In hr.contract: Rimuovi la riga subscription_id = fields.Many2one(...).

In hr.version: Aggiungi il campo subscription_id. Assicurati che ci sia un campo (es. contract_id) che colleghi la versione al contratto.

Python
# models/hr_version.py
```
class HrVersion(models.Model):
    _name = 'hr.version'
    
    contract_id = fields.Many2one('hr.contract', string="Contratto")
    subscription_id = fields.Many2one('sale.order', string="Abbonamento")
```
Step 2: Preparazione dello Script di Pre-Migration
Crea la cartella migrations/16.0.1.1/ nel tuo modulo. Il file pre-migrate.py serve a salvare i dati prima che Odoo aggiorni il database.

Scopo: Se Odoo vede che il campo è stato rimosso dal Python, potrebbe eliminare la colonna SQL. Noi la salviamo in una tabella temporanea.

Python
# migrations/16.0.1.2/pre-migrate.py
```
def migrate(cr, version):
    _logger.info("##################################################################################")
    _logger.info("PRE-MIGRATION: Salvataggio dati per creazione hr.version")
    _logger.info("##################################################################################")
    
    # Creiamo la tabella temporanea per trasportare i dati tra le fasi
    cr.execute("""
        CREATE TABLE IF NOT EXISTS temp_hr_version_data AS
        SELECT id AS contract_id, subscription_id
        FROM hr_contract
        WHERE subscription_id IS NOT NULL
    """)
    _logger.info("##################################################################################")
    _logger.info("PRE-MIGRATION: Dati pronti in temp_hr_version_data")
    _logger.info("##################################################################################")
    
```
Step 3: Preparazione dello Script di Post-Migration
Crea il file post-migrate.py nella stessa cartella. Questo sposterà i dati dalla tabella temporanea alla nuova tabella delle versioni.

Scopo: Riassociare l'ID dell'abbonamento al record corretto in hr.version.

Python
# migrations/16.0.1.2/post-migrate.py
```
def migrate(cr, version):
    _logger.info("##################################################################################")    
    _logger.info("POST-MIGRATION: Generazione record in hr_version")
    _logger.info("##################################################################################")
    
    # 1. Verifichiamo se la tabella hr_version è stata creata dall'ORM
    #cr.execute("SELECT to_regclass('hr_version')")
    #if not cr.fetchone()[0]:
    #    _logger.error("POST-MIGRATION: Tabella hr_version non trovata! Verifica i tuoi modelli Python.")
    #    return
    
    cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name='temp_hr_version_data'")
    # 2. Inserimento massivo dei record
    if cr.fetchone():
        cr.execute("""
            INSERT INTO hr_version (contract_id, subscription_id, create_date, write_date)
            SELECT contract_id, subscription_id, NOW(), NOW()
            FROM temp_hr_version_data
            WHERE contract_id NOT IN (SELECT contract_id FROM hr_version)
        """)
        
    
    # 3. Pulizia
    _logger.info("##################################################################################")
    
    cr.execute("DROP TABLE IF EXISTS temp_hr_version_data")
    _logger.info("POST-MIGRATION: Pulizia tabella temporanea completata.")
    _logger.info("##################################################################################")
    
```
Step 4: Aggiornamento del Manifest
Odoo eseguirà gli script di migrazione solo se il numero di versione aumenta.

Apri __manifest__.py.

Se la versione era 16.0.1.0, modificala in 16.0.1.2

Step 5: Aggiornamento delle Viste XML
Non dimenticare di spostare il campo anche nell'interfaccia!

Rimuovi dalla vista ereditata di hr.contract.

```
<field name="subscription_id"/>
```
 
Aggiungilo nella vista di hr.version.

Step 6: Esecuzione
Riavvia il server Odoo per caricare le modifiche ai file Python.

Aggiorna il modulo dal menu "App" (cliccando sul pulsante "Aggiorna").
