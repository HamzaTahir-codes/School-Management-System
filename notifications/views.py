from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.db import models
from .models import NotificationLog, Broadcast, BroadcastReadStatus, BroadcastDeleteStatus, CommunicationResponse

class UnreadCountView(LoginRequiredMixin, ListView):
    """Returns just the unread count badge for HTMX polling."""
    def get_queryset(self):
        user = self.request.user
        # Unread individual logs
        unread_logs = NotificationLog.objects.filter(recipient=user, is_read=False, is_deleted=False).count()
        
        # Unread broadcasts (those NOT in BroadcastReadStatus for this user)
        # And NOT in BroadcastDeleteStatus
        role = user.role
        total_active_broadcasts = Broadcast.objects.filter(
            models.Q(target_role='ALL') | models.Q(target_role=role),
            is_active=True
        ).exclude(
            broadcastdeletestatus__user=user
        )
        
        read_broadcast_ids = BroadcastReadStatus.objects.filter(user=user).values_list('broadcast_id', flat=True)
        unread_broadcasts = total_active_broadcasts.exclude(id__in=read_broadcast_ids).count()
        
        return unread_logs + unread_broadcasts

    def render_to_response(self, context, **response_kwargs):
        count = self.get_queryset()
        if count > 0:
            return render(self.request, 'notifications/partials/unread_badge.html', {'count': count})
        return HttpResponse('')

class NotificationListView(LoginRequiredMixin, ListView):
    model = NotificationLog
    template_name = 'notifications/inbox.html'
    context_object_name = 'notifications'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        tab = self.request.GET.get('tab', 'all')
        
        if tab == 'sent':
            # Only relevant for users who can send (Admins)
            return [] # Logic moved to context for custom sorting
            
        qs = NotificationLog.objects.filter(recipient=user, is_deleted=False)
        if tab == 'unread':
            qs = qs.filter(is_read=False)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tab = self.request.GET.get('tab', 'all')
        role = user.role

        # Broadcasts filtering
        broadcast_qs = Broadcast.objects.filter(
            models.Q(target_role='ALL') | models.Q(target_role=role),
            is_active=True
        ).exclude(broadcastdeletestatus__user=user)

        if tab == 'unread':
            read_ids = BroadcastReadStatus.objects.filter(user=user).values_list('broadcast_id', flat=True)
            broadcast_qs = broadcast_qs.exclude(id__in=read_ids)
        
        context['broadcasts'] = broadcast_qs.order_by('-created_at')
        context['current_tab'] = tab
        
        # New: Read status for template to style broadcasts
        context['read_broadcast_ids'] = list(BroadcastReadStatus.objects.filter(user=user).values_list('broadcast_id', flat=True))
        
        # If Admin, show sent broadcasts too
        if user.role == 'ADMIN':
            context['sent_broadcasts'] = Broadcast.objects.filter(created_by=user).order_by('-created_at')

        return context

class MarkReadView(LoginRequiredMixin, ListView):
    """HTMX endpoint to mark an item as read."""
    def post(self, request, *args, **kwargs):
        user = request.user
        item_id = request.POST.get('id')
        item_type = request.POST.get('type') # 'broadcast' or 'notification'
        
        if item_type == 'notification':
            NotificationLog.objects.filter(id=item_id, recipient=user).update(is_read=True)
        elif item_type == 'broadcast':
            BroadcastReadStatus.objects.get_or_create(user=user, broadcast_id=item_id)
            
        response = HttpResponse('')
        response['HX-Trigger'] = 'updateBadge'
        return response

class DeleteMessageView(LoginRequiredMixin, ListView):
    """HTMX endpoint to soft-delete an item for the user."""
    def post(self, request, *args, **kwargs):
        user = request.user
        item_id = request.POST.get('id')
        item_type = request.POST.get('type')
        
        if item_type == 'notification':
            NotificationLog.objects.filter(id=item_id, recipient=user).update(is_deleted=True)
        elif item_type == 'broadcast':
            BroadcastDeleteStatus.objects.get_or_create(user=user, broadcast_id=item_id)
            
        response = HttpResponse('')
        response['HX-Trigger'] = 'updateBadge'
        return response

class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = CommunicationResponse
    fields = ['message']
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        broadcast_id = self.request.POST.get('broadcast_id')
        notification_id = self.request.POST.get('notification_id')
        
        if broadcast_id:
            form.instance.broadcast_id = broadcast_id
        if notification_id:
            form.instance.notification_id = notification_id
            
        form.save()
        messages.success(self.request, "Your reply has been sent.")
        return redirect('notifications:inbox')

class BroadcastCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Broadcast
    fields = ['title', 'message', 'target_role']
    template_name = 'notifications/broadcast_form.html'
    success_url = reverse_lazy('notifications:inbox')

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
