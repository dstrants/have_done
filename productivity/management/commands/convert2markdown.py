from django.core.management.base import BaseCommand

from productivity.models import Task


class Command(BaseCommand):
    help = "Converts old backups format  to markdown"

    def info(self, message: str):
        return self.stdout.write(self.style.HTTP_INFO(message))

    def success(self, message: str):
        return self.stdout.write(self.style.SUCCESS(message))

    def handle(self, *args, **options) -> None:
        tasks = Task.objects.all()

        self.info(f"Total Tasks located: {tasks.count()}")

        for task in tasks:
            words = task.task.split()
            converted_words = []
            for word in words:
                if word.startswith("$"):
                    converted_words.append(f"`{word.replace('$', '')}`")
                elif word.istitle():
                    converted_words.append(f"**{word}**")
                else:
                    converted_words.append(word)
            if words != converted_words:
                old_task = task.task
                new_task = " ".join(converted_words)
                task.task = new_task
                task.save(update_fields=['task'])
                self.info(f"Coverted: {old_task} -> {task.task}")
        self.success("Coversion finished!")
