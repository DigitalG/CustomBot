from django.contrib import admin
from admin_panel.models import Filter, Channel, Session, TeleBot, AdminChannel

admin.site.register(Filter)
admin.site.register(Channel)
admin.site.register(AdminChannel)
admin.site.register(Session)
admin.site.register(TeleBot)

