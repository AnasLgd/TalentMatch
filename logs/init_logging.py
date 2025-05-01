import json
import logging
import logging.config
import os
from datetime import datetime

def setup_logging(
    default_path='/projects/TalentMatch/logs/logging_config.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Configure le système de journalisation à partir d'un fichier de configuration JSON.
    
    Args:
        default_path (str): Chemin vers le fichier de configuration
        default_level (int): Niveau de journalisation par défaut
        env_key (str): Variable d'environnement qui peut contenir le chemin de configuration
    """
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    
    # Création des loggers principaux
    dev_logger = logging.getLogger('development')
    error_logger = logging.getLogger('error')
    audit_logger = logging.getLogger('audit')
    
    return {
        'dev': dev_logger,
        'error': error_logger,
        'audit': audit_logger
    }

def log_development_activity(logger, component, activity, details=None):
    """
    Journalise une activité de développement
    
    Args:
        logger: Logger à utiliser
        component (str): Composant concerné (frontend, backend, etc.)
        activity (str): Description de l'activité
        details (dict, optional): Détails supplémentaires
    """
    log_data = {
        'component': component,
        'activity': activity
    }
    
    if details:
        log_data.update(details)
    
    log_message = f"{component} - {activity}"
    logger.info(log_message, extra=log_data)

def log_error(logger, component, error_message, exception=None, details=None):
    """
    Journalise une erreur
    
    Args:
        logger: Logger à utiliser
        component (str): Composant concerné
        error_message (str): Description de l'erreur
        exception (Exception, optional): Exception levée
        details (dict, optional): Détails supplémentaires
    """
    log_data = {
        'component': component,
        'error': error_message
    }
    
    if details:
        log_data.update(details)
    
    if exception:
        log_data['exception_type'] = type(exception).__name__
        log_data['exception_msg'] = str(exception)
        log_message = f"{component} - {error_message} - {type(exception).__name__}: {str(exception)}"
    else:
        log_message = f"{component} - {error_message}"
    
    logger.error(log_message, extra=log_data)

def log_audit(logger, user, action, resource, success, details=None):
    """
    Journalise un événement d'audit (sécurité, accès, etc.)
    
    Args:
        logger: Logger à utiliser
        user (str): Utilisateur concerné
        action (str): Action réalisée
        resource (str): Ressource concernée
        success (bool): Succès de l'action
        details (dict, optional): Détails supplémentaires
    """
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'user': user,
        'action': action,
        'resource': resource,
        'success': success
    }
    
    if details:
        log_data.update(details)
    
    log_message = f"{user} - {action} - {resource} - {'Success' if success else 'Failure'}"
    logger.info(log_message, extra=log_data)

# Création d'un fichier de log initial pour marquer le début de l'onboarding
if __name__ == "__main__":
    loggers = setup_logging()
    
    # Log initial
    log_development_activity(
        loggers['dev'],
        'global',
        'Initialisation du système de journalisation',
        {
            'date': datetime.now().isoformat(),
            'environment': os.getenv('ENVIRONMENT', 'development')
        }
    )
    
    log_audit(
        loggers['audit'],
        'system',
        'init',
        'logging_system',
        True,
        {
            'version': '1.0',
            'environment': os.getenv('ENVIRONMENT', 'development')
        }
    )
    
    print("Système de journalisation initialisé avec succès.")
