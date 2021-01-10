from django.db.models.signals import m2m_changed, post_delete, pre_delete, post_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category, PriorityCount
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "pre_add" and action != "post_add":
        return
    for cat in instance.category.all():
        slug = cat.slug
        todos_count = cat.todos_count
        if action == "pre_add":
            #перед добавлением категории обнуляем вклад данного экземпляра в общий каунт по категории
            todos_count -= 1
            Category.objects.filter(slug=slug).update(todos_count=todos_count)
        elif action == "post_add":
            # после добавлнения добавляем все имеющиеся категории в экземпляре в старые значения счетчик
            todos_count += 1
            Category.objects.filter(slug=slug).update(todos_count=todos_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    TODOS_COUNT_DEFAULT = 0  #Устанавливаем переменную с дефолтным значением todos_count в модели Категории

    cat_counter = Counter()
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            # print(cat.slug)
            cat_counter[cat.slug] += 1

    check_categories = Category.objects.all()

    for category in check_categories:
        todos_count = category.todos_count #Старый счетчик категории
        # Проверяем, присутствует ли существующая в модели категория в счетчике количества
        if cat_counter[category.slug]:
            #Если да, уменьшаем значение старого счетчика на -1, если значения не совпадают
            if todos_count != cat_counter[category.slug]:
                todos_count -= 1
            Category.objects.filter(slug=category.slug).update(todos_count=todos_count)
        else:
            # Если нет, устанавливаем дефолтное значение todos_count
            Category.objects.filter(slug=category.slug).update(todos_count=TODOS_COUNT_DEFAULT)



@receiver(post_save, sender=TodoItem)
def add_count_of_priorities(sender, instance, **kwargs):
    id = instance.priority
    title = instance.get_priority_display()
    priority, create = PriorityCount.objects.get_or_create(id= id, title=title)
    count = priority.count
    count += 1
    PriorityCount.objects.filter(id=priority.id).update(count=count)
    return

@receiver(pre_delete, sender=TodoItem)
def delete_count_of_priorities(sender, instance, **kwargs):
    id = instance.priority
    priority = PriorityCount.objects.get(id=id)
    print(priority.count)
    count = priority.count
    count -= 1
    PriorityCount.objects.filter(id=id).update(count=count)

#Обработка сигнала pre_delete при удалении экземпляра TodoItem. Callback удаляет значение в строке category перед удалением экземпляра.
#Что приводит к вызову сигнала m2m_changed в экземпляре и callback task_cats_removed для пересчета обновленых значений todos_count
@receiver(pre_delete, sender=TodoItem)
def task_deleted(sender, instance, *args, **kwargs):
    categories = Category.objects.all()
    for category in categories:
        category.todoitem_set.remove(instance)