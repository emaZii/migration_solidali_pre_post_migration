import logging

_logger = logging.getLogger(__name__)

# migrations/16.0.1.1/pre-migrate.py
def migrate(cr, version):
    _logger.info("#######################################################")
    _logger.info("PARTITA MIGRAZIONE")
    _logger.info("#######################################################")

    # Salviamo i dati esistenti in una tabella temporanea
    cr.execute("""
        CREATE TABLE IF NOT EXISTS temp_subscription_move AS
        SELECT id AS old_contract_id, subscription_id
        FROM hr_contract
        WHERE subscription_id IS NOT NULL
    """)
    
    
