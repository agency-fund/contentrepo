import threading

import django_filters
from django.db.models import Count, F
from django.forms.widgets import NumberInput
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from django.forms import MultiWidget
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import GenericViewSet
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import PageReportView, ReportView
from wagtail.admin.widgets import AdminDateInput
import json
from django.db.models.functions import TruncMonth

from .forms import UploadFileForm
from .models import ContentPage, ContentPageRating, PageView
from .serializers import ContentPageRatingSerializer, PageViewSerializer
from .utils import import_content_csv


class StaleContentReportFilterSet(WagtailFilterSet):
    last_published_at = django_filters.DateTimeFilter(
        label=_("Last published before"), lookup_expr="lte", widget=AdminDateInput
    )
    view_counter = django_filters.NumberFilter(
        label=_("View count"), lookup_expr="lte", widget=NumberInput
    )

    class Meta:
        model = ContentPage
        fields = ["live", "last_published_at"]


class PageViewFilterSet(WagtailFilterSet):
    timestamp = django_filters.DateTimeFromToRangeFilter(
        label=_("Date Range"),
        widget=MultiWidget(widgets=[AdminDateInput, AdminDateInput]),
    )

    class Meta:
        model = PageView
        fields = ["timestamp"]


class StaleContentReportView(ReportView):
    header_icon = "time"
    title = "Stale Content Pages"
    template_name = "reports/stale_content_report.html"
    filterset_class = StaleContentReportFilterSet
    list_export = PageReportView.list_export + ["last_published_at", "view_counter"]
    export_headings = dict(
        last_published_at="Last Published",
        view_counter="View Count",
        **PageReportView.export_headings
    )

    def get_queryset(self):
        return ContentPage.objects.annotate(view_counter=Count("views")).all()


class PageViewReportView(ReportView):
    title = "Page views"
    template_name = "reports/page_view_report.html"
    filterset_class = PageViewFilterSet

    def get_queryset(self):
        return PageView.objects.all()

    def get_filtered_queryset(self):
        return self.filter_queryset(self.get_queryset())

    def get_views_data(self):
        view_per_month = list(
            self.get_filtered_queryset()[1]
            .annotate(month=TruncMonth("timestamp"))
            .values("month")
            .annotate(x=F("month"), y=Count("id"))
            .values("x", "y")
        )
        labels = [item["x"].date() for item in view_per_month]
        return {"data": view_per_month, "labels": labels}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_view_data"] = json.dumps(
            self.get_views_data(), indent=4, sort_keys=True, default=str
        )
        return context


class ContentUploadThread(threading.Thread):
    def __init__(self, file, splitlines, newline, purge, locale, **kwargs):
        self.file = file
        self.splitlines = splitlines
        self.purge = purge
        self.locale = locale
        self.newline = newline
        super(ContentUploadThread, self).__init__(**kwargs)

    def run(self):
        import_content_csv(
            self.file, self.splitlines, self.newline, self.purge, self.locale
        )


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["purge"] == "True":
                ContentPage.objects.all().delete()
            ContentUploadThread(
                request.FILES["file"],
                form.cleaned_data["split_messages"],
                form.cleaned_data["newline"],
                form.cleaned_data["purge"],
                form.cleaned_data["locale"],
            ).start()
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


def CursorPaginationFactory(field):
    """
    Returns a CursorPagination class with the field specified by field
    """

    class CustomCursorPagination(CursorPagination):
        ordering = field
        page_size = 1000

    name = "{}CursorPagination".format(field.capitalize())
    CustomCursorPagination.__name__ = name
    CustomCursorPagination.__qualname__ = name

    return CustomCursorPagination


class PageViewFilter(filters.FilterSet):
    timestamp_gt = filters.IsoDateTimeFilter(field_name="timestamp", lookup_expr="gt")

    class Meta:
        model = PageView
        fields: list = []


class ContentPageRatingFilter(filters.FilterSet):
    timestamp_gt = filters.IsoDateTimeFilter(field_name="timestamp", lookup_expr="gt")

    class Meta:
        model = ContentPageRating
        fields: list = []


class GenericListViewset(GenericViewSet, ListModelMixin):
    page_size = 1000
    pagination_class = CursorPaginationFactory("timestamp")
    filter_backends = [filters.DjangoFilterBackend]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class PageViewViewSet(GenericListViewset):
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer
    filterset_class = PageViewFilter


class ContentPageRatingViewSet(GenericListViewset, CreateModelMixin):
    queryset = ContentPageRating.objects.all()
    serializer_class = ContentPageRatingSerializer
    filterset_class = ContentPageRatingFilter

    def create(self, request, *args, **kwargs):
        if "page" in request.data:
            try:
                page = ContentPage.objects.get(id=request.data["page"])
                request.data["revision"] = page.get_latest_revision().id
            except ContentPage.DoesNotExist:
                raise ValidationError({"page": ["Page matching query does not exist."]})

        return super().create(request, *args, **kwargs)
