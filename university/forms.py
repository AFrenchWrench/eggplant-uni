from django import forms
from .models import Semester


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        course_selection_start_time = cleaned_data.get('course_selection_start_time')
        semester_end_date = cleaned_data.get('semester_end_date')

        overlapping_semesters = Semester.objects.filter(
            course_selection_start_time__lt=semester_end_date,
            semester_end_date__gt=course_selection_start_time
        ).exclude(id=self.instance.id)

        if overlapping_semesters.exists():
            raise forms.ValidationError('Semester overlaps with another semester')

        for field_name in ['course_selection_end_time', 'class_start_time', 'class_end_time',
                           'course_addition_drop_start',
                           'course_addition_drop_end', 'last_day_for_emergency_withdrawal',
                           'exam_start_time']:
            field_value = cleaned_data.get(field_name)
            if field_value and not (course_selection_start_time <= field_value <= semester_end_date):
                raise forms.ValidationError(
                    f'{field_name} should be between course selection start and semester end dates')

        field_pairs = [
            ('course_selection_start_time', 'course_selection_end_time'),
            ('course_selection_end_time', 'course_addition_drop_start'),
            ('course_addition_drop_start', 'course_addition_drop_end'),
            ('course_addition_drop_end', 'last_day_for_emergency_withdrawal'),
            ('last_day_for_emergency_withdrawal', 'class_start_time'),
            ('class_start_time', 'class_end_time'),
            ('class_end_time', 'exam_start_time'),
            ('exam_start_time', 'semester_end_date'),
        ]
        for start_field, end_field in field_pairs:
            start_value = cleaned_data.get(start_field)
            end_value = cleaned_data.get(end_field)
            if start_value and end_value and start_value >= end_value:
                raise forms.ValidationError(f'{end_field} should be later than {start_field}')

        return cleaned_data


class UpdateSemesterForm(SemesterForm):
    def __init__(self, *args, **kwargs):
        super(UpdateSemesterForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False
