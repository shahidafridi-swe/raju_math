from django.shortcuts import render, redirect
from .forms import ExamForm as ExamUpdateForm, StudentMarksForm
from django.forms import modelformset_factory
from .models import Exam, StudentExamMark

def exam_details(request, pk):
    exam = Exam.objects.get(id=pk)
    students = StudentExamMark.objects.filter(exam=exam)
    
    context = {
        "exam":exam,
        "students" : students
    }
    return render(request, 'exams/exam_details.html', context)


def exam_update(request, pk):
    exam = Exam.objects.get(id=pk)
    students = StudentExamMark.objects.filter(exam=exam)

    ExamForm = ExamUpdateForm(instance=exam)

    StudentMarksFormSet = modelformset_factory(StudentExamMark, form=StudentMarksForm, extra=0)

    if request.method == 'POST':
        ExamForm = ExamUpdateForm(request.POST, instance=exam)
        formset = StudentMarksFormSet(request.POST, queryset=students)
  
        # Check if the form and formset are valid
        if ExamForm.is_valid() and formset.is_valid():
        
            # Save the exam title
            ExamForm.save()

            # Save all student marks
            formset.save()
         
            return redirect('exam_details', pk=exam.id)
        else:
            print(ExamForm.errors)
            print(formset.errors)

    else:
        formset = StudentMarksFormSet(queryset=students)

    context = {
        'exam_form': ExamForm,
        'formset': formset,
        'exam': exam,
    }

    return render(request, 'exams/exam_update.html', context)