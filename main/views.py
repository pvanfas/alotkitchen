from collections import defaultdict
from datetime import datetime

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
from .models import DeliveryAddress, ItemMaster, MealOrder, MealPlan, Preference, Subscription, SubscriptionRequest
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
from .utils import create_subscription_from_preference,bulk_create_meal_orders

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
        context = super().get_context_data(**kwargs)
        
        
        qs = self.get_queryset().values("item__mealtype", "item__name").annotate(total_quantity=Sum("quantity"))
        data = defaultdict(list)
        for entry in qs:
            mealtype = entry["item__mealtype"]
            item_name = entry["item__name"]
            total_quantity = entry["total_quantity"]
            data[mealtype].append((item_name, total_quantity))
        context["datas"] = dict(data)

        # Add preference data

        preferences = Preference.objects.filter().values("id", "first_name", "last_name", "start_date", "status", "mobile")
        context["preferences"] = preferences
        # print(context)
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
    
    # Get related data for form dropdowns
    context = {
        'preference': preference,
        'language_choices': LANGUAGE_CHOICES,
        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'delivery_addresses': preference.get_addresses(),
    }
    
    # Get meal plans for each meal type
    if preference.subscription_subplan and preference.subscription_subplan.plan.meal_category:
        meal_category = preference.subscription_subplan.plan.meal_category
        context.update({
            'early_breakfast_meals': MealPlan.objects.filter(
                meal_category=meal_category,
                menu_item__mealtype='EARLY_BREAKFAST'
            ),
            'breakfast_meals': MealPlan.objects.filter(
                meal_category=meal_category,
                menu_item__mealtype='BREAKFAST'
            ),
            'tiffin_lunch_meals': MealPlan.objects.filter(
                meal_category=meal_category,
                menu_item__mealtype='TIFFIN_LUNCH'
            ),
            'lunch_meals': MealPlan.objects.filter(
                meal_category=meal_category,
                menu_item__mealtype='LUNCH'
            ),
            'dinner_meals': MealPlan.objects.filter(
                meal_category=meal_category,
                menu_item__mealtype='DINNER'
            ),
        })
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                
                preference.first_name = request.POST.get('first_name', '')
                preference.last_name = request.POST.get('last_name', '')
                preference.email = request.POST.get('email', '')
                preference.preferred_language = request.POST.get('preferred_language', '')
                preference.mobile = request.POST.get('mobile', '')
                preference.alternate_mobile = request.POST.get('alternate_mobile', '')
                preference.whatsapp_number = request.POST.get('whatsapp_number', '')
                preference.notes = request.POST.get('notes', '')
                preference.remarks = request.POST.get('remarks', '')
                preference.status = request.POST.get('status', 'PENDING')
                
                # Update start date
                start_date = request.POST.get('start_date')
                if start_date:
                    from datetime import datetime
                    preference.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                
                # Update meal preferences for each day
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                meal_types = ['early_breakfast', 'breakfast', 'tiffin_lunch', 'lunch', 'dinner']
                
                for day in days:
                    for meal_type in meal_types:
                        field_name = f"{day}_{meal_type}"
                        meal_plan_id = request.POST.get(field_name)
                        
                        if meal_plan_id:
                            try:
                                meal_plan = MealPlan.objects.get(id=meal_plan_id)
                                setattr(preference, field_name, meal_plan)
                            except MealPlan.DoesNotExist:
                                pass
                        else:
                            setattr(preference, field_name, None)
                
                # Update delivery addresses
                address_types = ['early_breakfast_address', 'breakfast_address', 'tiffin_lunch_address', 'lunch_address', 'dinner_address']
                for address_type in address_types:
                    address_id = request.POST.get(address_type)
                    if address_id:
                        try:
                            address = DeliveryAddress.objects.get(id=address_id)
                            setattr(preference, address_type, address)
                        except DeliveryAddress.DoesNotExist:
                            pass
                    else:
                        setattr(preference, address_type, None)
                
                # Save the preference
                preference.save()
                
                messages.success(request, 'Preference updated successfully!')
                return redirect('main:preference_detail', pk=preference.pk)
                
        except Exception as e:
            messages.error(request, f'Error updating preference: {str(e)}')
    
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
    
    try:
        with transaction.atomic():
            # Approve the preference
            preference.status = 'APPROVED'
            preference.completed_at = timezone.now()
            preference.save()
            
            # Create subscription from preference
            subscription = create_subscription_from_preference(preference)
            
            # Bulk create meal orders
            orders_created = bulk_create_meal_orders(preference, subscription)
            print(f"Orders created: {orders_created}")
            messages.success(
                request, 
                f'Preference approved successfully! {orders_created} meal orders created.'
            )
            
    except Exception as e:
        
        print(e)
        return redirect('main:home_view')
    
    return redirect('main:home_view')


@csrf_exempt
@require_POST
def update_preference_ajax(request, pk):
    """AJAX endpoint for updating preference fields"""
    preference = get_object_or_404(Preference, pk=pk)
    
    field_name = request.POST.get('field_name')
    field_value = request.POST.get('field_value')
    
    if hasattr(preference, field_name):
        try:
            with transaction.atomic():
                # Handle different field types
                if field_name.endswith('_address'):
                    if field_value:
                        address = DeliveryAddress.objects.get(id=field_value)
                        setattr(preference, field_name, address)
                    else:
                        setattr(preference, field_name, None)
                elif any(meal_type in field_name for meal_type in ['early_breakfast', 'breakfast', 'tiffin_lunch', 'lunch', 'dinner']):
                    # Handle meal fields
                    if field_value:
                        meal_plan = MealPlan.objects.get(id=field_value)
                        setattr(preference, field_name, meal_plan)
                    else:
                        setattr(preference, field_name, None)
                else:
                    # Handle regular fields
                    setattr(preference, field_name, field_value)
                
                preference.save()
                return JsonResponse({'success': True, 'message': 'Field updated successfully'})
                
        except (DeliveryAddress.DoesNotExist, MealPlan.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Related object not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid field name'})