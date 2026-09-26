from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = "products"

    def ready(self):
        from django.template.context import BaseContext, Context

        def base_context_copy(self):
            duplicate = self.__class__.__new__(self.__class__)
            duplicate.__dict__.update(self.__dict__)
            duplicate.dicts = self.dicts[:]
            return duplicate

        BaseContext.__copy__ = base_context_copy

        def context_copy(self):
            duplicate = BaseContext.__copy__(self)
            duplicate.render_context = self.render_context.__copy__()
            return duplicate

        Context.__copy__ = context_copy