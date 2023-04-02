from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет новости из указанной категории.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        category_name = options['category']
        self.stdout.write(f"Вы действительно хотите удалить новости из категории {category_name}? y/n")
        answer = input()

        if answer == 'y':
            posts = Post.objects.filter(categories__name=category_name)
            posts.delete()
            self.stdout.write(self.style.SUCCESS(f"Новости из категории {category_name} удалены!"))
            return

        self.stdout.write(self.style.ERROR(f"Новости категории {category_name} не тронуты."))
