import logging
_logger = logging.getLogger(__name__)

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
    
