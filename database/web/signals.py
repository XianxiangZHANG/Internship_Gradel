# web/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from web import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User
from django.apps import apps
from django.utils.timezone import now
import pytz


@receiver(pre_save)
def store_old_instance(sender, instance, **kwargs):
    if sender == models.Log:
        return  # 避免处理 models.Log 的保存
    try:
        instance._old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._old_instance = None

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender == models.Log:
        return  # 避免记录 models.Log 的保存

    if not hasattr(instance, 'user'):
        return  # 仅记录具有 user 属性的模型

    user = instance.user
    model_name = sender.__name__
    object_id = instance.pk
    # object_id = str(instance)
    if created:
        action = "Created"
        changes = "Created - "+str(instance)
    else:
        action = "Updated"
        changes = get_changes(instance)  # 获取更详细的变更信息

    timezone = pytz.timezone('Europe/Luxembourg')
    timestamp = now().astimezone(timezone)  # 获取当前时间并转换为 CET

    models.Log.objects.create(
        user=user,
        action=action,
        model=model_name,
        object_id=object_id,
        changes=changes,
        timestamp=timestamp  # 设置 CET 时间戳
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender == models.Log:
        return  # 避免记录 models.Log 的删除

    if not hasattr(instance, 'user'):
        return  # 仅记录具有 user 属性的模型
    
    timezone = pytz.timezone('Europe/Luxembourg')
    timestamp = now().astimezone(timezone)  # 获取当前时间并转换为 CET

    user = instance.user
    model_name = sender.__name__
    object_id = instance.pk
    # object_id = str(instance)
    action = "Deleted"
    changes = "Deleted - "+str(instance)  # 捕获删除前的状态

    models.Log.objects.create(
        user=user,
        action=action,
        model=model_name,
        object_id=object_id,
        changes=changes,
        timestamp=timestamp  # 设置 CET 时间戳
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

    # for field, old_value in old_values.items():
    #     new_value = new_values[field]

    #     if old_value != new_value:
    #         field_name = instance._meta.get_field(field).verbose_name
    #         changes.append(f"{field_name}: '{old_value}' -> '{new_value}'")

    for field in old_values:
        old_value = old_values[field]
        new_value = new_values[field]
        
        # 获取字段对象
        field_object = instance._meta.get_field(field)

        # 如果是外键字段，获取外键对象的字符串表示
        if isinstance(field_object, ForeignKey):
            old_value = str(field_object.related_model.objects.get(pk=old_value)) if old_value else None
            new_value = str(field_object.related_model.objects.get(pk=new_value)) if new_value else None
        
        if old_value != new_value:
            field_name = field_object.verbose_name
            changes.append(f"{field_name}: '{old_value}' -> '{new_value}'")


    return "; \n".join(changes)