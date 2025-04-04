from django.views.generic import DetailView
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.db.models.functions import ExtractYear
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objects as go
from .models import Voter
from django.views.generic import ListView
from django.db.models import Count
from django.db.models.functions import ExtractYear
from plotly.offline import plot
import plotly.graph_objects as go
from datetime import datetime
from .models import Voter
from django.views.generic import TemplateView


class HomeView(TemplateView):
    "Displays the homepage with navigation links to the voter list and graphs."
    template_name = 'voter_analytics/home.html'

class VoterListView(ListView):
    "Lists all voters with filter options"
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()

        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        score = self.request.GET.get('score')

        if party:
            queryset = queryset.filter(party=party.strip())
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)
        if score:
            queryset = queryset.filter(voter_score=score)

        election_fields = {
            'v20state': 'voted_2020_state',
            'v21town': 'voted_2021_town',
            'v21primary': 'voted_2021_primary',
            'v22general': 'voted_2022_general',
            'v23town': 'voted_2023_town',
        }

        for param, model_field in election_fields.items():
            if self.request.GET.get(param) == 'on':
                queryset = queryset.filter(**{model_field: True})

        return queryset.order_by('last_name', 'first_name')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parties'] = sorted(set(v.party.strip() for v in Voter.objects.all() if v.party.strip()))
        context['years'] = list(range(1900, datetime.now().year + 1))
        context['scores'] = list(range(0, 6))
        return context


class VoterDetailView(DetailView):
    "Displays details for a single voter."
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    " Displays graphs summarizing voter data (birth year, party, participation)."
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # Birth Year Histogram
        birth_years = voters.annotate(year=ExtractYear('date_of_birth')).values('year').annotate(count=Count('id')).order_by('year')
        years = [item['year'] for item in birth_years if item['year']]
        counts = [item['count'] for item in birth_years if item['year']]

        birth_fig = go.Figure(data=[go.Bar(x=years, y=counts)])
        birth_fig.update_layout(title='Voter Birth Year Distribution', xaxis_title='Year', yaxis_title='Number of Voters')
        context['birth_year_graph'] = plot(birth_fig, output_type='div')

        # Party Affiliation Pie Chart
        party_counts = voters.values('party').annotate(count=Count('id')).order_by('-count')
        labels = [p['party'].strip() for p in party_counts]
        values = [p['count'] for p in party_counts]

        party_fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])
        party_fig.update_layout(title='Party Affiliation Distribution')
        context['party_graph'] = plot(party_fig, output_type='div')

        # Election Participation
        elections = [
            ('2020 State', voters.filter(voted_2020_state=True).count()),
            ('2021 Town', voters.filter(voted_2021_town=True).count()),
            ('2021 Primary', voters.filter(voted_2021_primary=True).count()),
            ('2022 General', voters.filter(voted_2022_general=True).count()),
            ('2023 Town', voters.filter(voted_2023_town=True).count()),
        ]

        election_fig = go.Figure(data=[go.Bar(
            x=[e[0] for e in elections],
            y=[e[1] for e in elections]
        )])
        election_fig.update_layout(title='Participation in Past Elections', xaxis_title='Election', yaxis_title='Number of Voters')
        context['election_graph'] = plot(election_fig, output_type='div')

        return context