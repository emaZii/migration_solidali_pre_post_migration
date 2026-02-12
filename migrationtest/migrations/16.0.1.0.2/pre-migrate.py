import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info("PRE-MIGRATION: Salvataggio dati per creazione hr.version")
    
    # Creiamo la tabella temporanea per trasportare i dati tra le fasi
    cr.execute("""
        CREATE TABLE IF NOT EXISTS temp_hr_version_data AS
        SELECT 
            id as contract_id, 
            subscription_id
        FROM hr_contract
        WHERE subscription_id IS NOT NULL
    """)
    _logger.info("PRE-MIGRATION: Dati pronti in temp_hr_version_data")
