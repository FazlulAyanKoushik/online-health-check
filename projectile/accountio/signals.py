import logging


logger = logging.getLogger(__name__)


def post_save_descendant(sender, instance, created, *args, **kwargs):
    pass


def post_save_organization(sender, instance, created, *args, **kwargs):
    pass


def post_save_organization_user(sender, instance, created, *args, **kwargs):
    if created:
        logger.debug(instance)
        pass


def post_delete_organization(sender, instance, *args, **kwargs):
    pass


def post_save_organization_doctor(sender, instance, created, *args, **kwargs):
    if created:
        logger.debug(instance)
        pass
