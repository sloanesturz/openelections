import random
from django import forms
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from openelections import constants as oe_constants
from openelections.ballot.models import Vote
from openelections.issues.models import Issue, SenateCandidate

class CandidatesField(forms.ModelMultipleChoiceField):
    # def label_from_instance(self, obj):
    #     s = ['<ul class="issues">']
    #     for cand in self.queryset:
    #         s.append(self.widget_for_candidate(cand))
    #     s.append('</ul>')
    #     return mark_safe(''.join(s))
        
    # def widget_for_candidate(self, cand):
    #     attrs = dict(issue_pk=cand.pk, html_id="issue_%d" % cand.pk, 
    #                  html_name="candidates_us", label=cand.title)
    #     return '''<li class="issue">
    #                 <input type="checkbox" name="%(html_name)s" id="%(html_id)s" value="%(issue_pk)d">
    #                 <label for="%(html_id)s">%(label)s</label>
    #               </li>''' % attrs
        
    def __unicode__(self):
        return self.label_from_instance(None)

class SenateCandidatesField(CandidatesField):
    pass
    
# 
# class CandidatesGSCField(CandidatesField):
#     pass
#     
# class SlatesIRVField(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, obj):        
#         self.num_slates = len(self.queryset)
#         rank_choices = [(i,i) for i in range(1,self.num_slates+1)]
#         rank_choices.insert(0, (0, '----'))
#         self.rank_select = forms.Select(choices=rank_choices)
#         
#         s = ['<ul class="issues">']
#         for slate in self.queryset:
#             s.append(self.widget_for_slate(slate))
#         s.append('</ul>')
#         return mark_safe(''.join(s))
# 
#         
#     def widget_for_slate(self, slate):
#         html_id = "issue_%d" % slate.pk
#         attrs = dict(html_id=html_id, html_name=html_id,
#                      label=slate.display_title(),
#                      select=self.rank_select.render(html_id, None))
#         return '''<li class="issue">
#                     <label for="%(html_id)s">%(label)s</label>
#                     %(select)s
#                   </li>''' % attrs
#                   
#     def __unicode__(self):
#         return self.label_from_instance(None)
#     
# class SlatesExecField(SlatesIRVField):
#     pass
#     
# class SlatesClassPresField(SlatesIRVField):
#     pass
#     
# class SpecialFeeRequestField(forms.ChoiceField):
#     choices = oe_constants.VOTES_YNA
#     specialfeerequest = None
#     
#     def __unicode__(self):
#         return super(SpecialFeeRequestField, self).__unicode__()
# 
#

def ballot_form_factory(_electorate):
    if not _electorate:
        raise Exception
    
    class _BallotForm(forms.Form):
        electorate = _electorate
        voter_id = forms.CharField()
        
        votes_us = SenateCandidatesField(widget=forms.CheckboxSelectMultiple, queryset=Issue.objects.filter(kind='US').all())
        
        def save(self):
            # TODO: transactions
            voter_id = self.cleaned_data['voter_id']
            for issue in self.cleaned_data['votes_us']:
                v = Vote(voter_id=voter_id, issue=issue, electorate=self.electorate)
                v.save()
                
        def clean(self):
            return self.cleaned_data
        
    
    #_BallotForm.electorate = electorate
    
    #_BallotForm.votes_gsc = CandidatesGSCField(queryset=CandidateGSC.objects.all())
    #_BallotForm.votes_exec = SlatesExecField(queryset=SlateExec.objects.all()) # verify that this maintains order
    #_BallotForm.votes_classpres = SlatesClassPresField(queryset=SlateClassPresident.objects.all())
    
    # _BallotForm.fields_specfees = []
    # for fee in SpecialFeeRequest.objects.all():
    #     field_name = "specfee_%d" % fee.pk
    #     field = SpecialFeeRequestField()
    #     field.specialfeerequest = fee
    #     _BallotForm.base_fields[field_name] = field
    #     _BallotForm.fields_specfees.append(field)
    
    return _BallotForm
