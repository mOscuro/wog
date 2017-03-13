from django.contrib import admin
from workout.models import Workout, Step

# Register your models here.
admin.site.register(Workout)
#admin.site.register(Step)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):

#    def admin_document_creator_link(self, document):
#        return '<a href="%s">%s</a>' % (reverse("admin:bb_user_user_change", args=(document.created_by.id,)),
#                                        escape(document.created_by.email))
#    admin_document_creator_link.allow_tags = True
#    admin_document_creator_link.short_description = "Creator"

    list_display = ('round', 'numero', 'exercise', 'nb_rep')
    #list_filter = ('workout',)
