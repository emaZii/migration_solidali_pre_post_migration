### Migration Test

PS: Non e tutto il modulo di base_solidali e stato preso solo quello necessario per far vedere se la migrazione funziona 
salto di versione -> 6.0.1.1 -> 16.0.1.2.

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
# migrations/16.0.1.1/pre-migrate.py
```
def migrate(cr, version):
    # Salviamo i dati esistenti in una tabella temporanea
    cr.execute("""
        CREATE TABLE IF NOT EXISTS temp_subscription_move AS
        SELECT id AS old_contract_id, subscription_id
        FROM hr_contract
        WHERE subscription_id IS NOT NULL
    """)
```
Step 3: Preparazione dello Script di Post-Migration
Crea il file post-migrate.py nella stessa cartella. Questo sposterà i dati dalla tabella temporanea alla nuova tabella delle versioni.

Scopo: Riassociare l'ID dell'abbonamento al record corretto in hr.version.

Python
# migrations/16.0.1.1/post-migrate.py
```
def migrate(cr, version):
    # Aggiorniamo hr_version usando i dati salvati nella tabella temporanea
    cr.execute("""
        UPDATE hr_version v
        SET subscription_id = t.subscription_id
        FROM temp_subscription_move t
        WHERE v.contract_id = t.old_contract_id
    """)
    # Pulizia: eliminiamo la tabella temporanea
    cr.execute("DROP TABLE IF EXISTS temp_subscription_move")
```
Step 4: Aggiornamento del Manifest
Odoo eseguirà gli script di migrazione solo se il numero di versione aumenta.

Apri __manifest__.py.

Se la versione era 16.0.1.0, modificala in 16.0.1.1.

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
