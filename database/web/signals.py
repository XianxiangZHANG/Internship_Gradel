# web/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from web import models
from django.db.models import ForeignKey
from django.utils.timezone import now, localtime
import pytz

@receiver(pre_save)
def store_old_instance(sender, instance, **kwargs):
    if sender == models.Log:
        return  # Avoid handling saving of models.Log
    try:
        instance._old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._old_instance = None

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender == models.Log:
        return  # Avoid saving records in models.Log

    if not hasattr(instance, 'user'):
        return  # Only log models that have a user property

    user = instance.user
    model_name = sender.__name__
    object_id = instance.pk
    # object_id = str(instance)
    if created:
        action = "Created"
        changes = "Created - "+str(instance)
    else:
        action = "Updated"
        changes = get_changes(instance)  # Get more detailed change information

    timezone = pytz.timezone('Europe/Luxembourg')
    timestamp = now().astimezone(timezone)

    models.Log.objects.create(
        user=user,
        action=action,
        model=model_name,
        object_id=object_id,
        changes=changes,
        timestamp=timestamp  # Setting Timestamp
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender == models.Log:
        return 

    if not hasattr(instance, 'user'):
        return  
    
    timezone = pytz.timezone('Europe/Luxembourg')
    timestamp = now().astimezone(timezone)

    # Print for debugging
    # print("Local Time: ", timestamp)
    # print("UTC Time: ", now())

    user = instance.user
    model_name = sender.__name__
    object_id = instance.pk
    # object_id = str(instance)
    action = "Deleted"
    changes = "Deleted - "+str(instance)  

    models.Log.objects.create(
        user=user,
        action=action,
        model=model_name,
        object_id=object_id,
        changes=changes,
        timestamp=timestamp  
    )

def get_changes(instance):
    """ Get detail """
    # old_instance = instance.__class__.objects.get(pk=instance.pk)

    old_instance = instance._old_instance
    if old_instance is None:
        return "No previous data available"
    
    old_values = model_to_dict(old_instance)
    new_values = model_to_dict(instance)
    title = "Updated - "+str(instance)
    changes = [title,]

  
    for field in old_values:
        old_value = old_values[field]
        new_value = new_values[field]
        
       
        field_object = instance._meta.get_field(field)

        # If it is a foreign key field, get the string representation of the foreign key object
        if isinstance(field_object, ForeignKey):
            old_value = str(field_object.related_model.objects.get(pk=old_value)) if old_value else None
            new_value = str(field_object.related_model.objects.get(pk=new_value)) if new_value else None
        
        if old_value != new_value:
            field_name = field_object.verbose_name
            changes.append(f"{field_name}: '{old_value}' -> '{new_value}'")


    return "; \n".join(changes)