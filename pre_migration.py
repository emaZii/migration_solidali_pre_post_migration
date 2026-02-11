import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    if not version:
        return

    _logger.info(">>> ESECUZIONE MIGRAZIONE SOLIDALI COMPLETA")

    # 1. RINOMINA TABELLE FISICHE (Basato su snippet doc)
    # Se i modelli nel .py sono solidali.titolo_studio e sub.servizio.line
    tables = [
        ('old_titolo_studio', 'solidali_titolo_studio'),
        ('old_servizio_line', 'sub_servizio_line'),
        ('vecchia_tabella_presenze', 'solidali_presenza'),
    ]
    for old, new in tables:
        cr.execute("SELECT count(*) FROM pg_class WHERE relname = %s", (old,))
        if cr.fetchone()[0] > 0:
            cr.execute(f"ALTER TABLE {old} RENAME TO {new}")
            _logger.info(f"Tabella {old} rinominata in {new}")

    # 2. SISTEMAZIONE COLONNE SU MODELLI EREDITATI (hr.contract, account.move)
    # Esempio: se il campo subscription_id deve diventare sale_order_id
    try:
        cr.execute("ALTER TABLE hr_contract RENAME COLUMN subscription_id TO sale_order_id")
        _logger.info("Colonna subscription_id rinominata in hr_contract")
    except Exception:
        _logger.info("Colonna subscription_id già rinominata o inesistente")

    # 3. AGGIORNAMENTO RIFERIMENTI MODELLI (fondamentale per i Many2one)
    # Senza questo, i campi Many2one punteranno a modelli che Odoo non trova più
    model_renames = [
        ('solidali_paghe.paga', 'solidali.paga'),
        ('vecchio.modello', 'solidali.nuovo_modello'),
    ]
    for old_m, new_m in model_renames:
        # Aggiorna definizioni campi
        cr.execute("UPDATE ir_model_fields SET relation = %s WHERE relation = %s", (new_m, old_m))
        # Aggiorna modelli di sistema
        cr.execute("UPDATE ir_model SET model = %s WHERE model = %s", (new_m, old_m))
        cr.execute("UPDATE ir_model_data SET model = %s WHERE model = %s", (new_m, old_m))

    # 4. PULIZIA VINCOLI (Constraints)
    # Odoo 18 fallisce se trova indici con nomi che vuole usare lui
    cr.execute("DROP INDEX IF EXISTS vecchio_modulo_index_name")

    _logger.info(">>> MIGRAZIONE SOLIDALI COMPLETATA CON SUCCESSO")
