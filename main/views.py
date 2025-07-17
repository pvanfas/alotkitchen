from collections import defaultdict
from datetime import datetime
from itertools import groupby

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from main.choices import LANGUAGE_CHOICES
from main.mixins import HybridDetailView, HybridListView, HybridUpdateView
from users.models import CustomUser as User
from users.tables import UserTable

from .forms import SubscriptionAddressForm, SubscriptionRequestApprovalForm
from .mixins import HybridTemplateView, HybridView
from .models import Area, DeliveryAddress, ItemMaster, MealOrder, MealPlan, Preference, Subscription, SubscriptionRequest
from .tables import (
    CustomerMealOrderTable,
    DeliveryMealOrderTable,
    ItemMasterTable,
    MealOrderDataTable,
    MealOrderTable,
    StandardMealOrderTable,
    StandardSubscriptionTable,
    SubscriptionRequestTable,
    SubscriptionTable,
)
from .utils import bulk_create_orders_with_fallback, create_subscription_from_preference,bulk_create_meal_orders

# permissions = ("Administrator","Manager", "Manager", "KitchenManager", "Delivery", "Customer", "Accountant")


def get_week_of_month():
    today = timezone.localdate()
    day_of_month = today.day
    week_number = (day_of_month - 1) // 7 + 1
    return week_number


def get_day_name():
    today = timezone.localdate()
    day_name = today.strftime("%A")
    return day_name


def get_week_value(n):
    return 2 if n % 2 == 0 else 1

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
class DashboardView(HybridListView):
    template_name = "app/main/home.html"
    permissions = ("Administrator", "Manager", "KitchenManager", "Delivery", "Customer", "Accountant")
    model = MealOrder
    context_object_name = "orders"
    
    def get_table_class(self):
        if self.request.user.usertype == "KitchenManager":
            return StandardMealOrderTable
        elif self.request.user.usertype == "Delivery":
            return DeliveryMealOrderTable
        elif self.request.user.usertype == "Customer":
            return CustomerMealOrderTable
        return MealOrderTable
    
    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return MealOrder.objects.filter(date=datetime.today(), user=self.request.user, is_active=True)
        elif self.request.user.usertype == "Delivery":
            return MealOrder.objects.filter(date=datetime.today(), is_active=True)
        else:
            return MealOrder.objects.filter(date=datetime.today(), is_active=True)
    
    def get_context_data(self, **kwargs):
        from users.models import CustomUser  # Import your user model
        
        context = super().get_context_data(**kwargs)
        
        # Existing meal order data
        qs = self.get_queryset().values("item__mealtype", "item__name").annotate(total_quantity=Sum("quantity"))
        data = defaultdict(list)
        for entry in qs:
            mealtype = entry["item__mealtype"]
            item_name = entry["item__name"]
            total_quantity = entry["total_quantity"]
            data[mealtype].append((item_name, total_quantity))
        context["datas"] = dict(data)
        
        # Add preference data
        preferences = Preference.objects.filter(session_id=self.request.session.session_key).values(
            "id", "first_name", "last_name", "start_date", "status", "mobile"
        )
        context["preferences"] = preferences
        
        # Add data for the approval modal
        # context["areas"] = Area.objects.filter(is_active=True).order_by('name')
        context["delivery_staff"] = CustomUser.objects.filter(
            usertype="Delivery", 
            is_active=True
        ).order_by('first_name', 'last_name')
        
        return context

class TomorrowOrdersView(HybridListView):
    template_name = "app/main/home.html"
    permissions = ("Administrator", "Manager", "KitchenManager", "Delivery", "Customer", "Accountant")
    model = MealOrder
    table_class = MealOrderTable
    context_object_name = "orders"
    title = "Tomorrow's Orders"

    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return MealOrder.objects.filter(date=datetime.today() + timezone.timedelta(days=1), user=self.request.user, is_active=True)
        else:
            return MealOrder.objects.filter(date=datetime.today() + timezone.timedelta(days=1), is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset().values("item__mealtype", "item__name").annotate(total_quantity=Sum("quantity"))
        data = defaultdict(list)
        for entry in qs:
            mealtype = entry["item__mealtype"]
            item_name = entry["item__name"]
            total_quantity = entry["total_quantity"]
            data[mealtype].append((item_name, total_quantity))
        context["datas"] = dict(data)
        return context


class MealOrderListView(HybridListView):
    permissions = ("Administrator", "Manager", "Accountant")
    model = MealOrder
    title = "Order Master"
    table_class = MealOrderTable
    filterset_fields = ("user", "item", "subscription_plan", "date", "status")

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class MealOrderDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Administrator", "Manager", "Accountant")


class MealOrderListData(HybridListView):
    model = MealOrder
    permissions = ("Administrator", "Manager", "Accountant")
    title = "Order Master Excel"
    table_class = MealOrderDataTable
    template_name = "app/main/mealorder_list_data.html"

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class ItemMasterListView(HybridListView):
    filterset_fields = ("mealtype", "is_veg")
    search_fields = ("name",)
    permissions = ("Administrator", "Manager", "Accountant", "KitchenManager")
    model = ItemMaster
    title = "Item Master"
    table_class = ItemMasterTable


class ItemMasterDetailView(HybridDetailView):
    model = ItemMaster
    permissions = ("Administrator", "Manager", "Accountant", "KitchenManager")


class CustomerListView(HybridListView):
    filterset_fields = ("username", "email")
    search_fields = ("username", "email", "mobile")
    permissions = ("Administrator", "Manager")
    model = User
    title = "Customers"
    table_class = UserTable

    def get_queryset(self):
        return User.objects.filter(usertype="Customer", is_active=True)


class CustomerDetailView(HybridDetailView):
    model = User
    permissions = ("Administrator", "Manager")


class SubscriptionRequestListView(HybridListView):
    metadata = {"expand": "newpage"}
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager")
    title = "Subscription Requests"
    table_class = SubscriptionRequestTable
    filterset_fields = ("user", "plan", "start_date", "status")
    template_name = "app/main/subscriptionrequest_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_requests_count"] = SubscriptionRequest.objects.filter(is_active=True).count()
        context["pending_requests_count"] = SubscriptionRequest.objects.filter(is_active=True, status="PENDING").count()
        context["approved_requests_count"] = SubscriptionRequest.objects.filter(is_active=True, status="APPROVED").count()
        context["rejected_requests_count"] = SubscriptionRequest.objects.filter(is_active=True, status="REJECTED").count()
        return context


class SubscriptionRequestDetailView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager")
    template_name = "app/main/request_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubscriptionRequestApprovalForm(self.request.POST or None, instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = SubscriptionRequestApprovalForm(request.POST, instance=instance)
        subscription, _ = Subscription.objects.get_or_create(
            request=instance,
            user=instance.user,
            plan=instance.plan,
            start_date=instance.start_date,
            end_date=instance.start_date + timezone.timedelta(days=instance.plan.validity),
        )
        instance.status = "APPROVED"
        instance.save()
        if form.is_valid():
            form.save()
            return redirect("main:subscriptionrequest_list")
        return self.get(request, *args, **kwargs)


class SubscriptionRequestUpdateView(HybridUpdateView):
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager", "Customer")
    exclude = ("status", "is_active", "user")

    def get_form_class(self):
        if self.request.user.usertype == "Customer":
            return SubscriptionAddressForm
        return super().get_form_class()

    def get_template_names(self):
        if self.request.user.usertype == "Customer":
            return "web/select_address.html"
        return super().get_template_names()

    def get_success_url(self):
        if self.request.user.usertype == "Customer":
            return reverse("main:subscription_list")
        return reverse("main:subscriptionrequest_list")


class SubscriptionRequestApproveView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager")

    # def get(self, request, *args, **kwargs):
    #     data = self.get_object()
    #     subscription, _ = Subscription.objects.get_or_create(
    #         request=data,
    #         user=data.user,
    #         plan=data.plan,
    #         start_date=data.start_date,
    #         end_date=data.start_date + timezone.timedelta(days=data.plan.validity),
    #     )
    #     data.status = "APPROVED"
    #     data.save()
    #     return redirect("main:subscription_detail", pk=subscription.pk)


class SubscriptionRequestRejectView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager")

    def get(self, request, *args, **kwargs):
        data = self.get_object()
        data.status = "REJECTED"
        data.save()
        return redirect("main:subscriptionrequest_detail", pk=data.pk)


class SubscriptionRequestPrintView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager")
    template_name = "app/main/request_print.html"


class SubscriptionListView(HybridListView):
    model = Subscription
    filterset_fields = ("user", "plan", "start_date", "end_date")
    search_fields = ("user",)
    permissions = ("Administrator", "Manager", "Customer")
    table_class = SubscriptionTable

    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return Subscription.objects.filter(user=self.request.user)
        return Subscription.objects.filter(is_active=True)

    def get_table_class(self):
        if self.request.user.usertype == "Customer":
            return StandardSubscriptionTable
        return SubscriptionTable


class SubscriptionDetailView(HybridDetailView):
    model = Subscription
    permissions = ("Administrator", "Manager", "Customer")


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"
    permissions = ("Administrator", "Manager", "KitchenManager", "Delivery", "Customer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HistoryDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Customer",)


class HistoryView(HybridListView):
    template_name = "app/main/history.html"
    model = MealOrder
    filterset_fields = ()
    table_class = MealOrderTable
    search_fields = ("item__name",)
    permissions = ("Customer",)

    def get_queryset(self):
        return MealOrder.objects.filter(user=self.request.user, is_active=True, date__lt=datetime.today())


class DonateMealOrderView(HybridView):
    model = MealOrder
    permissions = ("Customer",)

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_donated = True
        order.save()
        return redirect("main:dashboard_view")


class UpdateMealOrderStatusView(HybridView):
    model = MealOrder
    permissions = ("Delivery",)

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        delivery_status = request.POST.get("delivery_status")
        order.status = delivery_status
        order.save()
        return redirect("main:dashboard_view")


class ChangeMenuView(HybridListView):
    model = MealOrder
    permissions = ("Administrator", "Manager", "KitchenManager")
    table_class = MealOrderTable

    def get_queryset(self):
        return MealOrder.objects.filter(date=datetime.today(), is_active=True)
    
def edit_preference(request, pk):
    preference = get_object_or_404(Preference, pk=pk)
    
    if request.method == 'POST':
        # Update basic fields
        preference.first_name = request.POST.get('first_name', '')
        preference.last_name = request.POST.get('last_name', '')
        preference.email = request.POST.get('email', '')
        preference.preferred_language = request.POST.get('preferred_language', '')
        preference.mobile = request.POST.get('mobile', '')
        preference.alternate_mobile = request.POST.get('alternate_mobile', '')
        preference.whatsapp_number = request.POST.get('whatsapp_number', '')
        preference.notes = request.POST.get('notes', '')
        preference.remarks = request.POST.get('remarks', '')
        
        # Handle start_date
        start_date = request.POST.get('start_date')
        if start_date:
            preference.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        # Handle delivery addresses
        # for meal_type in ['early_breakfast', 'breakfast', 'tiffin_lunch', 'lunch', 'dinner']:
        #     address_id = request.POST.get(f'{meal_type}_address')
        #     if address_id:
        #         try:
        #             address = DeliveryAddress.objects.get(id=address_id)
        #             setattr(preference, f'{meal_type}_address', address)
        #         except DeliveryAddress.DoesNotExist:
        #             pass
        
        # Handle meal plan selections
        # days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        # meal_types = ['early_breakfast', 'breakfast', 'tiffin_lunch', 'lunch', 'dinner']
        
        # for day in days:
        #     for meal_type in meal_types:
        #         field_name = f'{day}_{meal_type}'
        #         meal_id = request.POST.get(field_name)
        #         if meal_id:
        #             try:
        #                 meal_plan = MealPlan.objects.get(id=meal_id)
        #                 setattr(preference, field_name, meal_plan)
        #             except MealPlan.DoesNotExist:
        #                 pass
        #         else:
        #             # Set to None if no meal selected
        #             setattr(preference, field_name, None)
        
        # try:
        #     preference.save()
        #     messages.success(request, 'Preference updated successfully!')
        #     return redirect('preference_detail', pk=preference.pk)  # Adjust URL name as needed
        # except Exception as e:
        #     messages.error(request, f'Error updating preference: {str(e)}')
    
    # Group meal plans by day and meal category for easier template access
    # meal_plans_by_day = {}
    # for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
    #     meal_plans_by_day[day] = {}
    #     for meal_type in ['Early Breakfast', 'Breakfast', 'Tiffin Lunch', 'Lunch', 'Dinner']:
    #         meal_plans_by_day[day][meal_type] = MealPlan.objects.filter(
    #             day=day,
    #             meal_category__name=meal_type,
    #             is_active=True
    #         ).select_related('meal_category', 'menu_item')
    
    context = {
        'preference': preference,
        'languages': LANGUAGE_CHOICES,
        'delivery_addresses': DeliveryAddress.objects.filter(user=request.user),
        'meal_plans': MealPlan.objects.filter(is_active=True).select_related('meal_category', 'menu_item'),
        # 'meal_plans_by_day': meal_plans_by_day,
    }
    context["days"] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    
    return render(request, 'app/main/edit_preference.html', context)


def approve_preference(request, pk):
    preference = get_object_or_404(Preference, pk=pk)
    
    # Check if already approved
    if preference.status == 'APPROVED':
        messages.warning(request, 'Preference is already approved.')
        return redirect('main:home_view')
    
    if not preference.start_date:
        messages.error(request, 'Start date is required.')
        return redirect('main:home_view')
    
    # Handle POST request (form submission from modal)
    if request.method == 'POST':
        try:
            # Extract modal data
            area_id = request.POST.get('area')
            delivery_staff_id = request.POST.get('delivery_staff')
            meal_fee = request.POST.get('meal_fee', '0.00')
            no_of_meals = request.POST.get('no_of_meals', '0')
            
            # Validate required fields
            if not area_id:
                messages.error(request, 'Zone is required.')
                return redirect('main:home_view')
            
            if not delivery_staff_id:
                messages.error(request, 'Delivery staff is required.')
                return redirect('main:home_view')
            
            # Get the related objects
            try:
                # area = Area.objects.get(id=area_id)
                delivery_staff = User.objects.get(id=delivery_staff_id, usertype="Delivery")
            except (Area.DoesNotExist, User.DoesNotExist):
                messages.error(request, 'Invalid zone or delivery staff selected.')
                return redirect('main:home_view')
            
            with transaction.atomic():
                # Approve the preference
                preference.status = 'APPROVED'
                preference.completed_at = timezone.now()
                preference.save()
                
                # Create subscription from preference
                subscription = create_subscription_from_preference(preference)
                
                # Update the subscription request with modal data
                subscription_request = subscription.request
                # subscription_request.area = area
                subscription_request.delivery_staff = delivery_staff
                subscription_request.meal_fee = float(meal_fee)
                subscription_request.no_of_meals = int(no_of_meals)
                subscription_request.approved_by = request.user
                subscription_request.approved_at = timezone.now()
                subscription_request.save()
                
                # Bulk create meal orders with fallback
                orders_created = bulk_create_orders_with_fallback(preference, subscription)
                
                messages.success(
                    request,
                    f'Preference approved successfully! {orders_created} meal orders created.'
                )
                
        except ValueError as ve:
            messages.error(request, f'Invalid data provided: {str(ve)}')
            return redirect('main:home_view')
        except Exception as e:
            messages.error(request, f'Error approving preference: {str(e)}')
            return redirect('main:home_view')
    
    else:
        # Handle GET request (shouldn't happen with modal, but for safety)
        messages.error(request, 'Invalid request method.')
    
    return redirect('main:home_view')


