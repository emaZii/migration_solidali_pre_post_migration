import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info("POST-MIGRATION: Generazione record in hr_version")

    # 1. Verifichiamo se la tabella hr_version è stata creata dall'ORM
    cr.execute("SELECT to_regclass('hr_version')")
    if not cr.fetchone()[0]:
        _logger.error("POST-MIGRATION: Tabella hr_version non trovata! Verifica i tuoi modelli Python.")
        return

    # 2. Inserimento massivo dei record
    # Usiamo '1' per create_uid e write_uid (utente admin)
    # NOW() per le date di creazione
    cr.execute("""
        INSERT INTO hr_version (
            contract_id, 
            subscription_id, 
            create_uid, 
            write_uid, 
            create_date, 
            write_date
        )
        SELECT 
            contract_id, 
            subscription_id, 
            1, 
            1, 
            NOW(), 
            NOW()
        FROM temp_hr_version_data
        WHERE contract_id NOT IN (SELECT contract_id FROM hr_version)
    """)
    
    count = cr.rowcount
    _logger.info(f"POST-MIGRATION: Creati {count} nuovi record in hr_version")

    # 3. Pulizia
    cr.execute("DROP TABLE IF EXISTS temp_hr_version_data")
    _logger.info("POST-MIGRATION: Pulizia tabella temporanea completata.")
