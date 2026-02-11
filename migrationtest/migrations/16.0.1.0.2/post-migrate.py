import logging

_logger = logging.getLogger(__name__)

# migrations/16.0.1.1/post-migrate.py
def migrate(cr, version):
    _logger.info("#######################################################")
    _logger.info("Sta Effettuando MIGRAZIONE")
    _logger.info("#######################################################")
    
    # Aggiorniamo hr_version usando i dati salvati nella tabella temporanea
    cr.execute("""
        UPDATE hr_version v
        SET subscription_id = t.subscription_id
        FROM temp_subscription_move t
        WHERE v.contract_id = t.old_contract_id
    """)
    # Pulizia: eliminiamo la tabella temporanea
    cr.execute("DROP TABLE IF EXISTS temp_subscription_move")

    _logger.info("#######################################################")
    _logger.info("FINITA MIGRAZIONE")
    _logger.info("#######################################################")
