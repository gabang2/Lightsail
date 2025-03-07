from django.contrib import admin

# Register your models here.

from .models import Category, Review, FirstLabeledData, Result, SecondLabeledData


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category_product", "category_middle", "category_color"]

    def delete_model(self, request, obj):
        obj.category_product = None
        obj.save()

    actions = ["delete_selected"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['category_product']
    list_filter = ['category_product']

    def delete_selected_reviews(modeladmin, request, queryset):
        # Define the chunk size
        chunk_size = 1000
        selected_reviews = list(queryset)  # Convert the QuerySet to a list
        total_reviews = len(selected_reviews)

        for i in range(0, total_reviews, chunk_size):
            chunk = selected_reviews[i:i + chunk_size]
            # Delete reviews in chunks of 1000 or less
            Review.objects.filter(pk__in=[review.pk for review in chunk]).delete()

        modeladmin.message_user(
            request,
            f"Selected {total_reviews} reviews have been deleted in chunks of 1000 or less."
        )

    delete_selected_reviews.short_description = "Delete selected reviews in chunks of 1000 or less"



admin.site.register(Category, CategoryAdmin)
admin.site.register(Review,  ReviewAdmin)
admin.site.register(FirstLabeledData)
admin.site.register(SecondLabeledData)
admin.site.register(Result)
